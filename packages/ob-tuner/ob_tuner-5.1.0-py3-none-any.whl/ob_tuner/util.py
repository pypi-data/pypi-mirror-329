import datetime
import json
import os
import pathlib
import time
from decimal import Decimal
from logging.handlers import RotatingFileHandler
import boto3
import faker
import gradio as gr
import logging
from io import StringIO
from sys import platform

import requests
from dotenv import load_dotenv, find_dotenv
from importlib.metadata import version
from boto3.dynamodb.conditions import Attr
from leadmo_api.models.contact_endpoint_params import LookupContactParams, CreateContactParams
from leadmo_api.v1.client import LeadmoApiV1
from pydantic import ValidationError
from requests import HTTPError

# Use find_dotenv to locate the .env file
dotenv_path = find_dotenv(usecwd=True)
if dotenv_path:
    load_dotenv(dotenv_path)

os.environ["INFRA_STACK_NAME"] = os.environ.get("INFRA_STACK_NAME", "LOCAL")
# Unfortunate... fix later
from openbrain.orm.model_client import Client

import openbrain.orm
import openbrain.util
from openbrain.orm.model_agent_config import AgentConfig
from openbrain.orm.model_common_base import InMemoryDb
from openbrain.util import config, Defaults
from openbrain.tools import Toolbox


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(CustomJsonEncoder, self).default(obj)

# Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Add a rotating log handler
formatter = logging.Formatter('%(filename)-20s:%(lineno)-4d %(levelname)-8s %(message)s')

current_dir = pathlib.Path(__file__).parent
parent_dir = current_dir.parent
pathlib.Path(parent_dir / "logs").mkdir(parents=True, exist_ok=True)
pathlib.Path(parent_dir / "temp").mkdir(parents=True, exist_ok=True)
LOG_FILE_PATH = parent_dir / "logs" / "ob-tuner.log"
TEMP_DIR_PATH = parent_dir / "temp"


handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=10000, backupCount=5)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Add a stringio handler
log_stream = StringIO()
string_handler = logging.StreamHandler(log_stream)
string_handler.setLevel(logging.DEBUG)
string_handler.setFormatter(formatter)
logger.addHandler(string_handler)
ADMIN_USER = os.environ.get("ADMIN_USER")

if os.environ.get("OB_MODE", "LOCAL") == "LOCAL" and ADMIN_USER:
    logger.info(f"Creating admin user {ADMIN_USER}")
    try:
        ADMIN_LEADMO_LOCATION_ID = os.getenv("ADMIN_LEADMO_LOCATION_ID")
        ADMIN_LEADMO_API_KEY = os.getenv("ADMIN_LEADMO_API_KEY")
        ADMIN_LEADMO_CALENDAR_ID = os.getenv("ADMIN_LEADMO_CALENDAR_ID")
        admin_user = Client(email=ADMIN_USER, leadmo_api_key=ADMIN_LEADMO_API_KEY, leadmo_location_id=ADMIN_LEADMO_LOCATION_ID, leadmo_calendar_id=ADMIN_LEADMO_CALENDAR_ID)
        admin_user.save()
        admin_default_agent_config = AgentConfig(client_id=ADMIN_USER, profile_name=Defaults.DEFAULT_PROFILE_NAME.value)
        admin_default_agent_config.save()
    except Exception as e:
        admin_user = Client(email=ADMIN_USER)
        admin_user.save()
        logger.info(f"Created admin user {ADMIN_USER}")

INFRA_STACK_NAME = os.environ.get("INFRA_STACK_NAME")
OB_MODE = config.OB_MODE
CHAT_ENDPOINT = os.environ.get("OB_API_URL", "") + "/chat"
DEFAULT_ORIGIN = os.environ.get("DEFAULT_ORIGIN", "https://localhost:5173")
OB_PROVIDER_API_KEY = os.environ.get("OB_PROVIDER_API_KEY", "")
DEFAULT_CLIENT_ID: str = openbrain.util.Defaults.DEFAULT_CLIENT_ID.value
DEFAULT_PROFILE_NAME = Defaults.DEFAULT_PROFILE_NAME.value
PORTAL_URL = os.getenv("PORTAL_URL")
COGNITO_DOMAIN = os.getenv("COGNITO_DOMAIN")
CLIENT_ID = os.getenv("CLIENT_ID")
# CALLBACK_URL = os.getenv("CALLBACK_URL")
DEPLOYMENT_URL = os.getenv("DEPLOYMENT_URL")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
GUEST_CLIENT_ID = "guest@openbra.in"
discovered_tools = Toolbox.discovered_tools
model_agent_config = openbrain.orm.model_agent_config
OB_TUNER_VERSION = version("ob-tuner")
CUSTOMER_NAME = os.getenv("CUSTOMER_NAME")
SUPER_SECRET_COGNITO_KEY = os.getenv("SUPER_SECRET_COGNITO_KEY")

NOAUTH_DEMO_PAGE_STR = os.getenv("NOAUTH_DEMO_PAGE", "False")
LEADMO_INTEGRATION_STR = os.getenv("LEADMO_INTEGRATION", "False")
LLS_INTEGRATION_STR = os.getenv("LLS_INTEGRATION", "False")
NOAUTH_DEMO_PAGE = NOAUTH_DEMO_PAGE_STR.casefold() == "true"
LEADMO_INTEGRATION = LEADMO_INTEGRATION_STR.casefold() == "true"
LLS_INTEGRATION = LLS_INTEGRATION_STR.casefold() == "true"

logger.info(f"************************************ GRADIO CONFIG ************************************")
logger.info(f"DEFAULT_ORIGIN: {DEFAULT_ORIGIN}")
logger.info("OB_API_URL: " + os.environ.get("OB_API_URL", ""))
logger.info(f"({type(NOAUTH_DEMO_PAGE)}): {NOAUTH_DEMO_PAGE=}")
logger.info(f"({type(LEADMO_INTEGRATION)}): {LEADMO_INTEGRATION=}")
logger.info(f"({type(LLS_INTEGRATION)}): {LLS_INTEGRATION=}")
logger.info(f"{CUSTOMER_NAME=}")
logger.info(f"{LEADMO_INTEGRATION=}")
logger.info(f"{NOAUTH_DEMO_PAGE=}")
logger.info(f"{LLS_INTEGRATION=}")
logger.info(f"{OB_TUNER_VERSION=}")
logger.info(f"LOGGING PATH: {LOG_FILE_PATH}")
logger.info(f"************************************ AUTH ************************************")
logger.info(f'COGNITO_DOMAIN: {COGNITO_DOMAIN}')
logger.info(f'CLIENT_ID: {CLIENT_ID}')
# logger.info(f'CALLBACK_URL: {CALLBACK_URL}')
logger.info(f'{PORTAL_URL=}')
logger.info(f'DEPLOYMENT_URL: {DEPLOYMENT_URL}')
logger.info("DEFAULT_ORIGIN: " + os.environ.get("DEFAULT_ORIGIN", "https://localhost:5173"))

logger.info(f"************************************ OPENBRAIN CONFIG ************************************")
logger.info(f"OB_MODE: {OB_MODE}")
logger.info(f"SESSION_TABLE_NAME: {config.SESSION_TABLE_NAME}")
logger.info(f"AGENT_CONFIG_TABLE_NAME: {config.AGENT_CONFIG_TABLE_NAME}")
logger.info(f"ACTION_TABLE_NAME: {config.ACTION_TABLE_NAME}")
logger.info(f"{INFRA_STACK_NAME=}")

logger.info(f"************************************ SECRETS ************************************")
OBFUSCATED_CLIENT_SECRET = CLIENT_SECRET[:2] + "-" * (len(CLIENT_SECRET) - 2)
OBFUSCATED_OB_PROVIDER_API_KEY = os.environ.get("OB_PROVIDER_API_KEY", "")[:2] + "-" * (len(os.environ.get("OB_PROVIDER_API_KEY", "")) - 2)
logger.info(f'CLIENT_SECRET: {OBFUSCATED_CLIENT_SECRET}')
logger.info("OB_PROVIDER_API_KEY: " + OBFUSCATED_OB_PROVIDER_API_KEY)

string_handler.flush()
tool_names = [tool.name for tool in Toolbox.discovered_tools if not tool.name.startswith("leadmo_")]
leadmo_tool_names = [tool.name for tool in Toolbox.discovered_tools if tool.name.startswith("leadmo_")]

tool_names.sort()
leadmo_tool_names.sort()
# TOOL_NAMES = tool_names + leadmo_tool_names if LEADMO_INTEGRATION else tool_names
TOOL_NAMES = tool_names + leadmo_tool_names
logger.info(f"Tools ({len(TOOL_NAMES)}): {TOOL_NAMES}")

REGISTERED_CLIENT_IDS = {
    "WoxomAI": [DEFAULT_CLIENT_ID, "woxom", "leadmo"],
    "OpenBra.in": [DEFAULT_CLIENT_ID, 'openbrain', 'leadmo'],
    "OBTest": [DEFAULT_CLIENT_ID, 'openbrain', 'woxom', 'leadmo'],
}


def get_debug_text(_debug_text=None) -> str:
    try:
        ret = log_stream.getvalue()
    except Exception as e:
        ret = e.__str__()

    if _debug_text:
        _debug_text = ret

    return ret


def get_aws_xray_trace_summaries(id=None):
    """Get x-ray logs from AWS"""
    client = boto3.client("xray")
    this_year = datetime.datetime.now().year
    this_month = datetime.datetime.now().month
    this_day = datetime.datetime.now().day
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).day

    if id:
        response = client.get_trace_summaries(
            StartTime=datetime.datetime(this_year, this_month, yesterday),
            EndTime=datetime.datetime(this_year, this_month, this_day),
            Sampling=False,
            FilterExpression=f"traceId = {id}",
        )
    else:
        response = client.get_trace_summaries(
            StartTime=datetime.datetime(this_year, this_month, yesterday),
            EndTime=datetime.datetime(this_year, this_month, this_day),
            Sampling=False,
        )

    return response


def is_settings_set():
    return True


def get_tool_description(tool_name):
    for tool in Toolbox.discovered_tools:
        if tool_name == tool.name:
            tool_instance = tool.tool()
            tool_description = tool_instance.description
            fields = tool_instance.args_schema.model_fields
            args_string = ""
            if not fields:
                args_string = "'No args'"
            for field in fields:
                field_str = fields[field].__str__()
                args_string += f"{field}: {field_str}\n"
            tool_description = f"""#### Description
{tool_description}

#### Args
```python
{args_string}
```"""
            return tool_description


def get_available_tool_descriptions():
    tool_descriptions = []

    for tool in Toolbox.discovered_tools:
        tool_name = tool.name
        tool_instance = tool.tool()
        tool_description = tool_instance.description
        fields = tool_instance.args_schema.model_fields
        args_string = ""
        if not fields:
            args_string = "'No args'"
        for field in fields:
            field_str = fields[field].__str__()
            args_string += f"{field}: {field_str}\n"
        tool_description = f"""
## Tool: {tool_name}

#### Description
{tool_description}

#### Args
```python
{args_string}
```
---"""

        tool_descriptions.append(tool_description)

    tool_descriptions_string = "\n".join(tool_descriptions)
    return tool_descriptions_string


def get_available_profile_names(_client_id) -> list:
    logger.debug(f"Getting available profile names for {_client_id}")
    # logger.warning("get_available_profile_names() is not implemented")
    # Get AgentConfig table

    if OB_MODE == Defaults.OB_MODE_LOCAL.value:
        try:
            logger.debug(f"Checking InMemoryDb for available profile names...")
            lst = list(InMemoryDb.instance[config.AGENT_CONFIG_TABLE_NAME][_client_id].keys())
            return lst
        except Exception:
            logger.warning(f"Not found, initializing default profile name...")
            _client_id = _client_id or GUEST_CLIENT_ID
            default_config = AgentConfig(client_id=_client_id, profile_name=DEFAULT_PROFILE_NAME)
            logger.info(f"Saving default profile name: {default_config}")
            default_config.save()
            logger.debug(f"Saved default profile name: {default_config}")
            lst = list(InMemoryDb.instance['agent_config_table'][_client_id].keys())
            logger.debug(f"Available profile names: {lst}")
            return lst
    else:
        table = boto3.resource("dynamodb").Table(config.AGENT_CONFIG_TABLE_NAME)
        # get all items in the table
        try:
            items = table.scan()["Items"]
            available_profile_names = [item["profile_name"] for item in items if item["client_id"] == _client_id]
            # response = table.query(
            #     KeyConditionExpression=boto3.dynamodb.conditions.Key('client_id').eq(_client_id)
            # )
            # available_profile_names = [profile["profile_name"] for profile in response]

        except Exception as e:
            logger.error(f"Error getting available profile names: {e}")
            available_profile_names = []

        return available_profile_names


def update_available_profile_names(client_id):
    if not client_id:
        return gr.Dropdown(choices=[DEFAULT_PROFILE_NAME], value=DEFAULT_PROFILE_NAME)

    available_profile_names = get_available_profile_names(client_id)
    # available_profile_names = [profile["profile_name"] for profile in available_profiles]
    try:
        selected_profile = DEFAULT_PROFILE_NAME
    except IndexError:
        default_config = AgentConfig(client_id=client_id, profile_name=DEFAULT_PROFILE_NAME)
        default_config.save()
        selected_profile = DEFAULT_PROFILE_NAME
        available_profile_names = [DEFAULT_PROFILE_NAME]
    return gr.Dropdown(choices=available_profile_names, value=selected_profile)


def get_llm_choices(llm_types=None):
    """Get the available LLM choices based on the selected types"""
    if not llm_types:
        llm_types = ["function"]
    available_llms = []
    known_llm_types = openbrain.orm.model_agent_config.EXECUTOR_MODEL_TYPES
    for llm_type in llm_types:
        if llm_type == "function":
            available_llms += openbrain.orm.model_agent_config.FUNCTION_LANGUAGE_MODELS
        elif llm_type == "chat":
            available_llms += openbrain.orm.model_agent_config.CHAT_LANGUAGE_MODELS
        elif llm_type == "completion":
            available_llms += openbrain.orm.model_agent_config.COMPLETION_LANGUAGE_MODELS
        else:
            logger.error(f"Unknown LLM type: {llm_type}, must be one of {known_llm_types}")
            continue
    return gr.Dropdown(choices=available_llms)


def greet(request: gr.Request):
    try:
        return f"Welcome to Gradio, {request.username}"
    except Exception:
        return "OH NO!"


def initialize_username(request: gr.Request):
    _username = request.username or GUEST_CLIENT_ID
    logger.debug(f"Initializing username: {_username}")
    registered_client_ids = get_registered_client_ids()
    # Copying the dict so we don't update it
    registered_client_ids_copy = registered_client_ids.copy()
    registered_client_ids_copy.append(_username)
    client_id_dropdown = gr.Dropdown(choices=registered_client_ids_copy, value=_username)

    try:
        AgentConfig.get(client_id=_username, profile_name=DEFAULT_PROFILE_NAME)
    except Exception as e:
        logger.info(f"No default AgentConfig found for {_username}, creating default agent config for {_username}")
        new_default_agent_config = AgentConfig(client_id=_username, profile_name=DEFAULT_PROFILE_NAME)
        new_default_agent_config.save()
    return [_username, client_id_dropdown]
    # return [_username]

def update_client_id(_username, _session_state):
    _username = _session_state["username"]
    _username_from_session_state = _session_state["username"]

    if _username != _username_from_session_state:
        _session_state["username"] = _username
        logger.debug(f"Updating session state (MISMATCH): {_username=}")

    logger.debug(f"Updating client_id: {_username=}")
    logger.debug(f"Updating client_id: {DEFAULT_CLIENT_ID=}")
    registered_client_ids = get_registered_client_ids()
    registered_client_ids_copy = registered_client_ids.copy()
    registered_client_ids_copy.append(_username)

    return gr.Dropdown(choices=registered_client_ids_copy, value=_username)

# def get_session_username(_session_state=None):
#     username = _session_state["username"]
#     _choices = [DEFAULT_CLIENT_ID, username]
#     return gr.Dropdown(choices=_choices, value=username)


def get_help_text() -> str:
    current_dir = pathlib.Path(__file__).parent
    help_text_path = current_dir / "resources" / "help_text.md"
    with open(help_text_path, "r", encoding="utf8") as file:
        # Read line in UTF-8 format
        help_text = file.readlines()
    return ''.join(help_text)

def get_registered_client_ids(customer_name=CUSTOMER_NAME):
    registered_client_ids = REGISTERED_CLIENT_IDS.get(customer_name, [DEFAULT_CLIENT_ID])
    return registered_client_ids








# EXAMPLE_CONTEXT = """
# {
#     "locationId": "LEADMOMENTUMLOCATIONID",
#     "calendarId": "LEADMOMENTUMCALENDARID",
#     "contactId": "CONTACTID",
#     "random_word": "spatula",
#     "firstName": "Cary",
#     "lastName": "Nutzington",
#     "name": "Cary Nutzington",
#     "dateOfBirth": "1970-04-01",
#     "phone": "+16198675309",
#     "email": "example@email.com",
#     "address1": "1234 5th St N",
#     "city": "San Diego",
#     "state": "CA",
#     "country": "US",
#     "postalCode": "92108",
#     "companyName": "Augmenting Integrations",
#     "website": "openbra.in",
#     "medications": "tylonol"
# }
# """.strip()

EXAMPLE_CONTEXT = {
    "locationId": "LEADMOMENTUMLOCATIONID",
    "calendarId": "LEADMOMENTUMCALENDARID",
    "contactId": "CONTACTID",
    "random_word": "spatula",
}
def set_client_id(_username):
    registered_client_ids = get_registered_client_ids()
    # Copying the dict so we don't update it
    registered_client_ids_copy = registered_client_ids.copy()
    registered_client_ids_copy.append(_username)
    client_id = gr.Dropdown(
        label="Client ID",
        filterable=True,
        info="Develop your own AI agents or use a community agent.",
        choices=registered_client_ids_copy,
        value=_username,
        elem_id="client_id",
        elem_classes=["agent_config"],
    )

    return client_id


def fetch_user_from_leadmo(fetch_user_from_leadmo, context, username):
    """Fetch user from Lead Momentum. If that fails, create a new user."""

    if not fetch_user_from_leadmo:
        return context
    context_dict = dict(context)
    clean_context_dict = {k: v for k, v in context_dict.items() if v != ''}

    # time.sleep(5.0)
    try:
        user = Client.get(email=username)
    except Exception as e:
        gr.Error(f"User not found: {username}")
        return context

    try:
        leadmo_api_key = user.leadmo_api_key
        leadmo_location_id = user.leadmo_location_id
        logger.debug(f"Location ID found: {leadmo_location_id}")
    except Exception as e:
        gr.Error(f"Please save your Lead Momentum Location ID and API key to your profile.")
        return context
    phone = user.phone
    email = user.email
    leadmo_client = LeadmoApiV1(api_key=leadmo_api_key)

    try:
        params = LookupContactParams(email=email,phone=phone).model_dump(exclude_none=True)
        response = leadmo_client.lookup_contact(**params)
        contact = response["contacts"][0]
        contact['locationId'] = user.leadmo_location_id
        contact['calendarId'] = user.leadmo_calendar_id
        contact['contactId'] = contact.get("id", "")
    except (ValidationError, HTTPError) as e:
        logger.warning(f"Failed to fetch user from Lead Momentum: {e}")
        # Create a contact
        create_contact_params = CreateContactParams(**clean_context_dict).model_dump(exclude_none=True)
        response = leadmo_client.create_contact(**create_contact_params)
        contact = response["contact"]

    data = {
        "locationId": user.leadmo_location_id,
        "calendarId": user.leadmo_calendar_id,
        "contactId": contact.get("id", ""),
        "firstName": contact.get("firstName", ""),
        "lastName": contact.get("lastName", ""),
        "name": contact.get("name", ""),
        "dateOfBirth": contact.get("dateOfBirth", ""),
        "phone": contact.get("phone", ""),
        "email": contact.get("email", ""),
        "address1": contact.get("address1", ""),
        "address2": contact.get("address2", ""),
        "city": contact.get("city", ""),
        "state": contact.get("state", ""),
        "country": user.country,
        "postalCode": contact.get("postalCode", ""),
        # "companyName": contact.get("companyName", ""),
        "website": contact.get("website", ""),
        "tags": contact.get("tags", ""),
        "random_word": faker.Faker().word()
    }

    return data


# username.change(fill_context, inputs=[context, username], outputs=user_leadmo_details + user_personal_details)
def fill_context(username, leadmo_api_key, leadmo_location_id, leadmo_calendar_id, first_name, last_name, date_of_birth, phone, address1, address2, city, state, country, postal_code, website):
    """Fill the context with the user's details from Lead Momentum"""
    random_word = faker.Faker().word()
    context = {
        "locationId": leadmo_location_id,
        "calendarId": leadmo_calendar_id,
        "contactId": "",
        "firstName": first_name,
        "lastName": last_name,
        "name": f"{first_name} {last_name}",
        "dateOfBirth": date_of_birth,
        "phone": phone,
        "email": username,
        "address1": address1,
        "address2": address2,
        "city": city,
        "state": state,
        "country": country,
        "postalCode": postal_code,
        "website": website,
        "random_word": random_word
    }
    return context

def fill_context_from_username(username):
    try:
        user = Client.get(email=username)
        context = {
            "locationId": user.leadmo_location_id,
            "calendarId": user.leadmo_calendar_id,
            "contactId": "",
            "firstName": user.first_name,
            "lastName": user.last_name,
            "name": f"{user.first_name} {user.last_name}",
            "dateOfBirth": user.date_of_birth,
            "phone": user.phone,
            "email": username,
            "address1": user.address1,
            "address2": user.address2,
            "city": user.city,
            "state": user.state,
            "country": user.country,
            "postalCode": user.postal_code,
            "website": user.website,
            "random_word": faker.Faker().word()
        }
    except Exception as e:
        logger.warning(f"User not found: {username}")
        context = {
            "locationId": "UNKNOWN",
            "email": username,
        }
    return context

# def get_action_events(_events=None, _session_state=None):
#     try:
#         _session_id = _session_state["session_id"]
#         logger.debug(f"Getting Action Events: session_id {_session_id}")
#     except TypeError:
#         logger.debug(f"Getting Action Events: failed to find session_id")
#
#         return json.dumps({"Idle": "Start a conversation to begin monitoring for events"})
#     logger.debug("Getting latest action...")
#     if not _session_id:
#         return json.dumps({"Idle": "Start a conversation to begin monitoring for events"})
#     try:
#         dynamodb = boto3.resource("dynamodb")
#         table = dynamodb.Table(config.ACTION_TABLE_NAME)
#         # response = table.get_item(Key={"action_id": "latest", "session_id": _session_id})
#         response = table.scan(
#             FilterExpression=Attr('session_id').eq(_session_id)
#         )
#         # ret = response.get("Item", {})
#         ret = response.get("Items", {})
#         logger.debug(f"Action Events: {ret}")
#     except KeyError as e:
#         logger.warning(f"Error finding events: {e}")
#         ret = json.dumps({"exception": "Event not found for this session, perhaps one wasn't sent yet in this conversation"})
#     except Exception as e:
#         logger.error(f"Error finding events: {e}")
#         ret = json.dumps({"exception": e.__str__()})
#
#     if _events:
#         _events = ret
#     return json.dumps(ret, cls=CustomJsonEncoder, indent=4, sort_keys=True)


def alert_on_actions(_session_state):
    """Alert on actions"""
    _events = {}
    for i in range(4):
        time.sleep(5)
        logger.debug(f"Checking for actions({i})...")

        try:
            _session_id = _session_state["session_id"]
            logger.debug("Checking for actions: Found session_id")
        except TypeError:
            logger.warning("No session ID found")
            return [_session_state, _events]

        try:
            dynamodb = boto3.resource("dynamodb")
            table = dynamodb.Table(config.ACTION_TABLE_NAME)
            response = table.scan(
                FilterExpression=Attr('session_id').eq(_session_id)
            )
            logger.debug(f"Checking for actions: {_session_id}")

            event_dict: dict = response.get("Items", {})
            logger.debug(f"found ({len(event_dict)}) actions")

            for item in event_dict:

                tool_name = item.get("tool_name", "")
                action_id = item.get("action_id", "")
                session_id = item.get("session_id", "")
                event = item.get("event", "")
                response = item.get("response", "")
                agent_config = item.get("agent_config", "")


                logger.debug(f"Event: {tool_name}")
                logger.debug(f"Response: {response}")
                if item["action_id"] in _session_state.get("events") or item["action_id"] == 'latest':
                    continue
                logger.info(f"Adding action_id: {item['action_id']} to session state")
                _session_state.get("events").append(item["action_id"])

                if _session_state.get("message_count") == 0:
                    logger.info(f"Message count is 0")
                    # continue
                # pretty_response = json.dumps(eval(response), indent=2)
                gr.Info(f"Tool used: {tool_name}")
            events_json = json.dumps(event_dict[-5:], cls=CustomJsonEncoder, indent=4, sort_keys=True)
            # remove the agent_config property from every item in event_json
            for item in event_dict:
                item.pop("agent_config", None)
            return [_session_state, events_json]

        except Exception as e:
            logger.error(f"Error checking for actions: {e}")
            return [_session_state, _events]

    return [_session_state, _events]

def warn_if_missing_tool_info(username, tools):
    """Warn if leadmo_location_id and leadmo_api_key are missing from the user's saved profile"""
    try:
        user = Client.get(email=username)
    except Exception as e:
        logger.warning(f"user not found: {username}")
        gr.Warning("Please save your Lead Momentum Location ID and API key to your profile to start using Lead Momentum tools.")
        return
    missing_info = []
    for tool in tools:
        if tool.startswith("leadmo_"):
            if not user.leadmo_location_id:
                missing_info.append("Lead Momentum Location ID")
            if not user.leadmo_api_key:
                missing_info.append("Lead Momentum API Key")
            if not user.leadmo_calendar_id:
                missing_info.append("Lead Momentum Calendar ID")
    if missing_info:
        missing_info_str = ", ".join(missing_info)
        gr.Warning(f"Missing info: {missing_info_str}")

def get_bucket_name():
    try:
        infra_stack_name = config.INFRA_STACK_NAME
        # Get tablename from outputs of INFRA_STACK
        cfn = boto3.client("cloudformation")
        response = cfn.describe_stacks(StackName=infra_stack_name)
        outputs = response["Stacks"][0]["Outputs"]
        for output in outputs:
            if output["OutputKey"] == "ObBucketName":
                bucket = output["OutputValue"]
                break
        else:
            raise Exception("Bucket name not found in outputs")
        return bucket
    except Exception as e:
        raise e

def react_to_message(chatbot, session_state, profile_name, client_id, like_data: gr.LikeData):
    bucket_name = get_bucket_name()
    session_id = session_state.get("session_id").lower()
    agent_config = AgentConfig.get(client_id=client_id, profile_name=profile_name)

    item = {
        "agent_config": agent_config.to_dict(),
        "chatbot_value": chatbot,
        "liked_message": like_data.value,
        "liked_index": like_data.index,
        "liked_or_disliked_as_bool": like_data.liked
    }

    s3 = boto3.client("s3")
    s3_key_name = f"reactions/{profile_name}/{client_id}/{session_id}.json"
    try:
        # get the file so we can append to it
        file = s3.get_object(Bucket=bucket_name, Key=s3_key_name)
        # json_content = json.loads(file["Body"].read())
        jsonl_content_str = file["Body"].read().decode('utf-8')
        jsonl_content = json.loads(jsonl_content_str)

    except Exception as e:
        jsonl_content = []

    jsonl_content.append(item)
    try:

        s3.put_object(Bucket=bucket_name, Key=s3_key_name, Body=json.dumps(jsonl_content))
        gr.Info(f"Feedback successfully saved. Thank you!")
    except Exception as e:
        logger.debug(f"Dumping file on local filesystem...")
        gr.Warning(f"Something went wrong, feedback saved to local filesystem. Please inform your administrator. Thank you!")


def fetch_appointments_from_leadmo(username, context):
    """Fetch appointments from Lead Momentum"""
    try:
        user = Client.get(email=username)
    except Exception as e:
        gr.Error(f"User not found: {username}")
        return {'error': "failed to get appointments"}

    try:
        leadmo_api_key = user.leadmo_api_key
        leadmo_location_id = user.leadmo_location_id
        logger.debug(f"Location ID found: {leadmo_location_id}")
    except Exception as e:
        gr.Error(f"Please save your Lead Momentum Location ID and API key to your profile.")
        return {'error': "failed to get appointments"}

    leadmo_client = LeadmoApiV1(api_key=leadmo_api_key)
    response = leadmo_client.get_contact_appointments(**context)
    events = response.get("events", [])
    return events