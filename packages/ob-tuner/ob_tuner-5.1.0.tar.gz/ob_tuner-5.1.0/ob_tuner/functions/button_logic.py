import json
import re
from decimal import Decimal
from json import JSONDecodeError

import faker
import gradio
from botocore.exceptions import NoCredentialsError
from gtts import gTTS
from requests import Session

from ob_tuner.util import *
from openbrain.orm.model_client import Client
import openbrain.orm
import openbrain.util
from openbrain.agents.gpt_agent import GptAgent
from openbrain.orm.model_agent_config import AgentConfig
from openbrain.orm.model_chat_message import ChatMessage
from openbrain.orm.model_chat_session import ChatSession
from openbrain.util import config, Defaults

def get_aws_cloudwatch_logs(_session_state=None):
    """Get cloudwatch logs for the agent we are interacting with"""

    logger.debug("Getting AWS Cloudwatch logs...")
    if not OB_PROVIDER_API_KEY:
        return "Local mode... no API to monitor."
    try:
        cloudwatch = boto3.client("logs")
        target_log_group_name_prefix = f"/aws/lambda/{INFRA_STACK_NAME}-APIHandler"
        log_groups = cloudwatch.describe_log_groups(logGroupNamePrefix=target_log_group_name_prefix)

        target_log_group = log_groups["logGroups"][0]["logGroupName"]

        if not target_log_group:
            logger.warning("No log group found")
            return "No log group found"

        # get the log streams for the log group
        log_streams = cloudwatch.describe_log_streams(logGroupName=target_log_group, orderBy="LastEventTime", descending=True)

        # get the latest log stream
        latest_log_stream = log_streams["logStreams"][0]["logStreamName"]

        # get the log events
        log_events = cloudwatch.get_log_events(logGroupName=target_log_group, logStreamName=latest_log_stream)

        events_string = ""
        # match_prefix = '{"level":"'

        # target_xray_trace_id = _session_state['last_response'].headers['x-amzn-trace-id']
        # target_xray_trace_id = re.sub(r';.*', '', target_xray_trace_id.replace("Root=", ""))
        max_events = 10
        counter = 0
        for event in log_events["events"]:
            message = event["message"]
            # if target_xray_trace_id in message:
            try:
                message_dict = json.loads(message, parse_float=Decimal)

                new_dict = {
                    "level": message_dict.get("level", None),
                    "location": message_dict.get("location", None),
                    "message": message_dict.get("message", None),
                    "timestamp": message_dict.get("timestamp", None),
                    "function_name": message_dict.get("function_name", None),
                    "request_path": message_dict.get("request_path", None),
                    "xray_trace_id": message_dict.get("xray_trace_id", None),
                }
            except JSONDecodeError:
                continue
            except KeyError:
                continue

            message = json.dumps(new_dict, indent=2)

            events_string += message + ",\n"
            counter += 1
            if counter > max_events:
                break

        # remove the last comma
        try:
            events_string = events_string[:-2]
        except Exception:
            events_string = json.dumps({"Idle": "No events found"})
        # formatted_message = '''```python\n''' + events_string + '''\n```'''
        formatted_message = "[\n" + events_string + "\n]"
        return formatted_message
    except Exception as e:
        return json.dumps({"exception": e.__str__()})


def chat(message, chat_history, _profile_name, _session_state, _client_id, _context):
    _session_state["message_count"] += 1

    # if _session_state.get("initial_reset"):
    #     gr.Info("Please start a new session.")
    #     return [message, chat_history, _session_state, _context]

    # Make a POST request to the chat endpoint
    session_id = _session_state["session_id"]
    chat_message = ChatMessage(
        agent_config=_profile_name, client_id=_client_id, reset=False, message=message, session_id=session_id, **_context
    )

    if not OB_PROVIDER_API_KEY:
        logger.warning("No API key found, trying to use local mode for agent interactions...")
        try:
            chat_session = ChatSession.get(session_id=session_id, client_id=_client_id)
        except Exception:
            logger.info("No chat session found, resetting instead...")
            return reset(_client_id, _profile_name, chat_history, _session_state, _context)

        agent_state = {
            "frozen_agent_memory": chat_session.frozen_agent_memory,
            "frozen_agent_config": chat_session.frozen_agent_config,
        }
        gpt_agent = GptAgent.deserialize(state=agent_state, context=_context)

        response_message = gpt_agent.handle_user_message(message)

        frozen_agent_memory = gpt_agent.serialize()["frozen_agent_memory"]
        frozen_agent_config = gpt_agent.serialize()["frozen_agent_config"]

        chat_session = ChatSession(
            session_id=session_id,
            client_id=_client_id,
            frozen_agent_memory=frozen_agent_memory,
            frozen_agent_config=frozen_agent_config,
        )
        chat_session.save()
        new_context = _context

    else:
        session = _session_state["session"]
        session.headers.update(
            {
                "x-api-key": OB_PROVIDER_API_KEY,
                "origin": DEFAULT_ORIGIN,
            }
        )
        chat_message_dump = chat_message.model_dump()
        chat_message_dump["session_id"] = session_id

        response = session.post(CHAT_ENDPOINT, json=chat_message_dump)
        logger.debug(f"Response: {response.json()}")
        response_message = response.json()["message"]
        _session_state["session"] = session

        response_dict = response.json()
        response_dict.pop("message")
        response_dict.pop("session_id")
        original_context = _context
        # original_context = _context
        # response_dict.update(original_context)
        original_context.update(response_dict)
        new_context = original_context
        _session_state["last_response"] = response

    # session_state["last_response"] = response_message

    chat_history.append([message, response_message])

    # Return the response from the API
    return ["", chat_history, _session_state, new_context]


def reset(_client_id, _profile_name, chat_history, _session_state, _context):
    _session_state["message_count"] = 0
    context_dict = dict(_context)

    chat_message = ChatMessage(client_id=_client_id, reset=True, agent_config=_profile_name, message="Hi", **context_dict)

    chat_message_dump = chat_message.model_dump()
    chat_message_dump.pop("message")

    response = None
    if not OB_PROVIDER_API_KEY:
        logger.info("No API key found, trying to use local mode for agent interactions...")
        # Get a new agent with the specified settings
        agent_config = AgentConfig.get(profile_name=_profile_name, client_id=_client_id)
        gpt_agent = GptAgent(agent_config=agent_config, context=context_dict)

        frozen_agent_memory = gpt_agent.serialize()["frozen_agent_memory"]
        frozen_agent_config = gpt_agent.serialize()["frozen_agent_config"]
        chat_session = ChatSession(
            client_id=_client_id,
            frozen_agent_memory=frozen_agent_memory,
            frozen_agent_config=frozen_agent_config,
        )
        session_id = chat_session.session_id
        _session_state["session_id"] = session_id
        chat_session.save()
        response_message = gpt_agent.agent_config.icebreaker
        response_dict = {}
    else:
        # Make a POST request to the reset endpoint
        session = Session()
        headers = {
            "x-api-key": OB_PROVIDER_API_KEY,
            "origin": DEFAULT_ORIGIN,
        }
        session.headers.update(headers)
        response = session.post(url=CHAT_ENDPOINT, json=chat_message_dump)
        if response.status_code != 200:
            logger.error(f"Failed to reset session: {response.json()}")
            gr.Error(f"Failed to communicate with OpenBra.in, contact your administrator and tell them to check the site's API key.")
            raise Exception(f"Failed to reset session: {response.json()}")

        logger.debug(f"Response: {response.json()}")
        session_id = response.cookies["Session"]
        logger.info("New session ID: " + session_id)
        _session_state["session_id"] = session_id
        _session_state["session"] = session
        _session_state["last_response"] = response
        response_message = response.json()["message"]
        response_dict = response.json()
        response_dict.pop("message")
        response_dict.pop("session_id")

    message = "Please wait, fetching new agent..."
    chat_history.append([message, response_message])

    # original_context = context_dict
    # original_context = _context

    # new_context = json.dumps(response_dict, indent=4)
    context_dict.update(response_dict)
    # context_dict["random_word"] = "Hamburger"

    # Return the response from the API
    return ["", chat_history, _session_state, context_dict]


def save(
    _icebreaker,
    # _chat_model,
    _system_message,
    _llm,
    # _prompt_layer_tags,
    _max_iterations,
    _max_execution_time,
    _executor_temp,
    _profile_name,
    # _executor_model_type,
    # _openai_api_key,
    # _promptlayer_api_key,
    _client_id,
    # _outgoing_webhook_url,
    _record_tool_actions,
    _record_conversations,
    _tools,
):
    if _profile_name.strip() == "":
        gr.Error("This agent config must have a name (profile_name).")
        return []

    agent_config = AgentConfig(
        icebreaker=str(_icebreaker),
        # executor_chat_model=str(_chat_model),
        system_message=str(_system_message),
        llm=str(_llm),
        # prompt_layer_tags=str(_prompt_layer_tags),
        executor_max_iterations=str(_max_iterations),
        executor_max_execution_time=str(_max_execution_time),
        executor_temp=str(_executor_temp),
        profile_name=str(_profile_name),
        # executor_model_type=str(_executor_model_type),
        # openai_api_key=str(_openai_api_key),
        # promptlayer_api_key=str(_promptlayer_api_key),
        client_id=str(_client_id),
        # outgoing_webhook_url=str(_outgoing_webhook_url),
        record_tool_actions=str(_record_tool_actions),
        record_conversations=str(_record_conversations),
        tools=_tools,
    )

    # Upload the preferences to the DynamoDB database
    agent_config.save()
    logger.debug(f"AgentConfig saved: {agent_config.to_json()}")
    gradio.Info("AgentConfig saved successfully.")

    # Return a success message
    return "Preferences saved successfully."


def load(_profile_name: str, _client_id: str):
    if _profile_name.strip() == "":
        raise gr.Error("client_id can't be blank.")
    # Upload the preferences to the DynamoDB database
    if not _client_id:
        _client_id = DEFAULT_CLIENT_ID
    try:
        logger.debug(f"Loading agent config for profile_name: {_profile_name}, client_id: {_client_id}")
        retrieved_agent_config = AgentConfig.get(profile_name=_profile_name, client_id=_client_id)
        logger.debug(f"AgentConfig loaded: {retrieved_agent_config.to_json()}")
    except Exception as e:
        new_default_agent_config = AgentConfig(client_id=_client_id, profile_name=_profile_name)
        new_default_agent_config.save()
        retrieved_agent_config = AgentConfig.get(profile_name=_profile_name, client_id=_client_id)
        logger.warning(f"AgentConfig created: {retrieved_agent_config.to_json()}")

    _tools = retrieved_agent_config.tools
    supported_tools = TOOL_NAMES

    for _tool in _tools:
        if _tool not in supported_tools:
            _tools.remove(_tool)

    _agent_config = [
        str(retrieved_agent_config.icebreaker),
        # str(retrieved_agent_config.executor_chat_model),
        str(retrieved_agent_config.system_message),
        str(retrieved_agent_config.llm),
        # str(retrieved_agent_config.prompt_layer_tags),
        str(retrieved_agent_config.executor_max_iterations),
        str(retrieved_agent_config.executor_max_execution_time),
        str(retrieved_agent_config.executor_temp),
        str(retrieved_agent_config.profile_name),
        # str(retrieved_agent_config.executor_model_type),
        # str(retrieved_agent_config.openai_api_key),
        # str(retrieved_agent_config.promptlayer_api_key),
        str(retrieved_agent_config.client_id),
        # str(retrieved_agent_config.outgoing_webhook_url),
        bool(retrieved_agent_config.record_tool_actions),
        bool(retrieved_agent_config.record_conversations),
        _tools,
    ]
    llm_name = retrieved_agent_config.llm
    if llm_name in openbrain.orm.model_agent_config.FUNCTION_LANGUAGE_MODELS:
        llm_type = "function"
    elif llm_name in openbrain.orm.model_agent_config.CHAT_LANGUAGE_MODELS:
        llm_type = "chat"
    elif llm_name in openbrain.orm.model_agent_config.COMPLETION_LANGUAGE_MODELS:
        llm_type = "completion"

    else:
        raise ValueError(f"Language model {llm_name} not found in any of the language model lists")

    ret = [*_agent_config, llm_type]
    # Return a success message
    return ret




def get_bottom_text(_session_state=None, _client_id=None, _profile_name=None):
    # Get recorded conversation link if it exists
    logger.debug("Getting bottom text...")
    logger.debug(f"Session state: {_session_state}")
    logger.debug(f"Client ID: {_client_id}")
    logger.debug(f"Profile Name: {_profile_name}")

    try:
        bucket_name = get_bucket_name()
        _session_id = _session_state.get("session_id").lower()
        dl_url = f"https://{bucket_name}.s3.amazonaws.com/conversations/{_profile_name}/{_client_id}/{_session_id}.json"
        link_text_md = f"| [{_session_id}]({dl_url}) "

    except (NoCredentialsError, AttributeError) as e:
        logger.debug(f"Error: {e}")
        link_text_md = ""
        _session_id = "`session-recording-disabled`"

    try:
        xray_trace_id = _session_state["last_response"].headers["x-amzn-trace-id"]
        xray_trace_id = re.sub(r";.*", "", xray_trace_id.replace("Root=", ""))

        xray_trace_id_md = f"| [X-Ray](https://console.aws.amazon.com/xray/home?region=us-east-1#/traces/{xray_trace_id}) "
    except (TypeError, AttributeError):
        xray_trace_id_md = ""

    if config.OB_MODE == Defaults.OB_MODE_LOCAL.value:
        orm_mode = "Ephemeral"
    else:
        orm_mode = "Persistent"
    orm_mode_md = f"| ORM: `{orm_mode}` "

    api = f"{CHAT_ENDPOINT}" if OB_PROVIDER_API_KEY else "LOCAL"
    api_md = f"| API: `{api}` "

    infra_stack_name = os.environ["INFRA_STACK_NAME"]
    infra_stack_name_md = f"| Stack: `{infra_stack_name}` "

    # user_api_key_link = f"{PORTAL_URL}/dashboard"
    # user_api_key_link_md = f"| [API Key]({user_api_key_link}) "

    ob_version = openbrain.__version__
    ob_tuner_version = OB_TUNER_VERSION

    versions_md = f"| Versions: OB=`{ob_version}` OB-Tuner=`{ob_tuner_version}` "

    formatted_text = (
        xray_trace_id_md
        # + user_api_key_link_md
        + link_text_md
        + versions_md
        + infra_stack_name_md
        + orm_mode_md
        + api_md
    )
    return formatted_text


def get_gpt_agent_logs():
    if OB_PROVIDER_API_KEY:
        return "This function is only available when running on-tuner with local openbrain code."
    else:
        agent_logger = openbrain.util.get_logger()
        for stream in agent_logger.handlers:
            if isinstance(stream.stream, StringIO):
                return stream.stream.getvalue().replace("\\n", "\n")


def get_context(
        _location_id,
        _calendar_id,
        _contact_id,
        _context_firstName,
        _context_lastName,
        _context_name,
        _context_dateOfBirth,
        _context_phone,
        _context_email,
        _context_address1,
        _context_city,
        _context_state,
        _context_country,
        _context_postalCode,
        _context_companyName,
        _context_website,
        _context_medications,
        _context_random_word,
):
    context_json = {
        "locationId": _location_id,
        "calendarId": _calendar_id,
        "contactId": _contact_id,
        "firstName": _context_firstName,
        "lastName": _context_lastName,
        "name": _context_name,
        "dateOfBirth": _context_dateOfBirth,
        "phone": _context_phone,
        "email": _context_email,
        "address1": _context_address1,
        "city": _context_city,
        "state": _context_state,
        "country": _context_country,
        "postalCode": _context_postalCode,
        "companyName": _context_companyName,
        "website": _context_website,
        "medications": _context_medications,
        "random_word": _context_random_word,
    }
    ret_dict = {}
    for key in context_json:
        if context_json[key]:
            ret_dict[key] = context_json[key]
    return json.dumps(ret_dict, indent=2)


def save_context(
        _location_id,
        _calendar_id,
        _contact_id,
        _context_firstName,
        _context_lastName,
        _context_name,
        _context_dateOfBirth,
        _context_phone,
        _context_email,
        _context_address1,
        _context_city,
        _context_state,
        _context_country,
        _context_postalCode,
        _context_companyName,
        _context_website,
        _context_medications,
        _context_random_word,
):
    context = get_context(
        _location_id,
        _calendar_id,
        _contact_id,
        _context_firstName,
        _context_lastName,
        _context_name,
        _context_dateOfBirth,
        _context_phone,
        _context_email,
        _context_address1,
        _context_city,
        _context_state,
        _context_country,
        _context_postalCode,
        _context_companyName,
        _context_website,
        _context_medications,
        _context_random_word,
    )
    raise gr.Error("Saving not yet implemented 💥!", duration=5)


def enable_chat_button():
    return gr.Button("Chat", variant="primary", elem_id="chat_button", elem_classes=["chatbot"], interactive=True)


def enable_or_disable_save(_client_id, _profile_name):
    _registered_client_ids = get_registered_client_ids()
    # Remove the default client_id
    # available_client_ids.append(_client_id)

    # If client_id is public, allow saving except to the default profile
    if _client_id == DEFAULT_CLIENT_ID:
        if _profile_name == DEFAULT_PROFILE_NAME:
            return gr.Button(value="Save Agent", variant="secondary", elem_id="save_agent_config_button", elem_classes=["agent_config"], interactive=False)
        else:
            return gr.Button(value="Save Agent", variant="secondary", elem_id="save_agent_config_button", elem_classes=["agent_config"], interactive=True)


    elif _client_id in _registered_client_ids:
        return gr.Button(value="Save Agent", variant="secondary", elem_id="save_agent_config_button", elem_classes=["agent_config"], interactive=False)
    else:
        return gr.Button(value="Save Agent", variant="secondary", elem_id="save_agent_config_button",
                                      elem_classes=["agent_config"], interactive=True)

# def generate_context(_username):
#     client = Client.get(email=_username)
#     leadmo_location_id = client.leadmo_location_id or "UNKNOWN"
#     # leadmo_contact_id_phone = client.leadmo_contact_id_phone or "UNKNOWN"
#     random_word = faker.Faker().word()
#     context = {
#         "locationId": leadmo_location_id,
#         "random_word": random_word,
#     }
#     result = context.update(client.model_dump())
#     return result
def speak(voice_enabled, text, session_state):
    thing_to_say = text[-1][-1]
    # Create audio file
    language = 'en'
    session_id = session_state["session_id"]

    audio_object = gTTS(text=thing_to_say, lang=language, slow=False)

    # delete previous file if exists
    audio_file_path = f'{TEMP_DIR_PATH}/{session_id}.mp3'

    if os.path.exists(audio_file_path):
        os.remove(audio_file_path)

    try:
        audio_object.save(audio_file_path)
        logger.debug(f"Saving audio file {audio_file_path}")
    except Exception as e:
        gr.Error(f"Error saving audio file: {e}")

    if voice_enabled:
        show_warning = not session_state.get("audio_warning_triggered")
        audio = gr.Audio(audio_file_path, autoplay=True, scale=1)
        if show_warning:
            gr.Info(f'See the Audio tab under "Agent Config and Tuning" to download this mp3.')
        session_state["audio_warning_triggered"] = True
        return audio
    else:
        return gr.Audio(scale=1)

def submit_feedback(_feedback, username):
    bucket_name = get_bucket_name()
    timestamp = datetime.datetime.now().isoformat()

    s3 = boto3.client("s3")
    # s3_key_name = f"feedback/{username}-{timestamp}.json"
    text_box_content = _feedback['text']
    text_box_file = _feedback['files']
    s3_base_key = f"feedback/{username}/{timestamp}"
    s3_content_key = f"{s3_base_key}/content.txt"
    s3_file_key = f"{s3_base_key}/{text_box_file}"

    try:

        s3.put_object(Bucket=bucket_name, Key=s3_content_key, Body=json.dumps(text_box_content))
        gr.Info(f"Feedback text successfully saved. Thank you!")
    except Exception as e:
        logger.error(f"Error uploading feedback text to S3: {e}")
        gr.Warning(f"Something went wrong... feedback text not saved, please reach out to Sam")

    try:
        # problem here
        with open(text_box_file[0], 'r') as f:
            s3.put_object(Bucket=bucket_name, Key=s3_file_key, Body=f.read())
        gr.Info(f"Feedback file successfully saved. Thank you!")
    except Exception as e:
        logger.error(f"Error uploading feedback file to S3: {e}")
        gr.Warning(f"Something went wrong... feedback file not saved, please reach out to Sam")



    # try:
    #     serializable_session_state = _session_state.copy()
    #     serializable_session_state['session_json'] = _session_state['session'].json()
    #     session_state_json = json.dumps(_session_state, indent=2)
    #     s3.put_object(Bucket=bucket_name, Key=s3_file_key, Body=session_state_json)
    #     gr.Info(f"Session state successfully saved. Thank you!")
    # except Exception as e:
    #     logger.error(f"Error uploading session state to S3: {e}")
    #     gr.Warning(f"Something went wrong... feedback session state not saved, please reach out to Sam")

import matplotlib.pyplot as plt
def get_agent_stats(username):
    # creating the dataset
    data = {'leadmo': 20, 'glados': 15, 'bender': 30}
    agents = list(data.keys())
    values = list(data.values())

    fig = plt.figure(figsize=(10, 5))

    # creating the bar plot
    plt.bar(agents, values, color='maroon',
            width=0.4)

    plt.xlabel("Agents")
    plt.ylabel("Conversations")
    plt.title("Top 3 Agents by Conversations")
    plt.savefig(f"{username}-agent_stats.png")

    return f"{username}-agent_stats.png"

def get_review_stats(username):
    data = {'Leader': 20, f'Average': 15, f'{username}': 30}
    agents = list(data.keys())
    values = list(data.values())

    fig = plt.figure(figsize=(10, 5))

    # creating the bar plot
    plt.bar(agents, values, color='maroon',
            width=0.4)

    plt.xlabel("Agents")
    plt.ylabel("Conversations")
    plt.title("Top 3 Agents by Conversations")
    plt.savefig(f"{username}-review_stats.png")

    return f"{username}-review_stats.png"


def get_tool_stats(username):
    data = {'leadmo_book_appointment': 20, 'leadmo_stop_conversation': 15, 'get_current_time': 30}
    agents = list(data.keys())
    values = list(data.values())

    fig = plt.figure(figsize=(10, 5))

    # creating the bar plot
    plt.bar(agents, values, color='maroon',
            width=0.4)

    plt.xlabel("Agents")
    plt.ylabel("Conversations")
    plt.title("Tool stats")
    plt.savefig(f"{username}-tool_stats.png")

    return f"{username}-tool_stats.png"
