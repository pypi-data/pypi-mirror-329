import gradio
import requests
from ob_tuner.functions.button_logic import *
from ob_tuner.functions.client_functions import *
from ob_tuner.util import *

# with gr.Blocks(theme="JohnSmith9982/small_and_pretty", analytics_enabled=False, ) as main_block:
with gr.Blocks(analytics_enabled=False, theme='freddyaboulton/dracula_revamped') as main_block:
    # m = gr.Markdown(f"Welcome to Gradio! {greet(Request)}")
    # gr.Button("Logout", link="/logout")
    username = gr.Textbox(label="username", visible=False)

    session_state = gr.State(value={
        "session_id": "",
        "session": requests.Session(),
        "agent": None,
        "last_response": None,
        "username": "",
        "events": [],
        "audio_warning_triggered": False,
        "message_count": 0,
        "events_initialized": False,
    })

    session_apikey = gr.State(value="")

    with gr.Accordion("My Resources") as submit_accordion:
        with gr.Tab("Selected Agent Configuration") as submit_tab:
            with gr.Row() as submit_row:
                with gr.Column(scale=3) as key_text_column:
                    with gr.Row() as key_text_row:
                        # available_client_ids = get_registered_client_ids()
                        client_id = gr.Dropdown(
                            label="Client ID",
                            filterable=True,
                            info="Develop your own AI agents or use a community agent.",
                            choices=[DEFAULT_CLIENT_ID],
                            value=DEFAULT_CLIENT_ID,
                            elem_id="client_id",
                            elem_classes=["agent_config"],
                        )
                        # initial_profiles = get_available_profile_names(client_id.value)
                        # initial_profile_names = [profile["profile_name"] for profile in initial_profiles]

                        profile_name = gr.Dropdown(
                            allow_custom_value=True,
                            filterable=True,
                            label="Profile Name",
                            info="The name of your AgentConfig. Defaults to 'default'",
                            choices=[],
                            value=DEFAULT_PROFILE_NAME,
                            elem_id="profile_name",
                            elem_classes=["agent_config"],
                        )

                with gr.Column(scale=1) as submit_column:
                    load_agent_profile_button = gr.Button(value="Reload Agent", variant="primary", elem_id="load_agent_config_button", elem_classes=["agent_config"])
                    save_agent_profile_button = gr.Button(value="Save Agent", variant="secondary", elem_id="save_agent_config_button", elem_classes=["agent_config"])

        with gr.Tab("User Profile") as user_profile_tab:
            with gr.Column():
                gr.Markdown("Information about you. When the AI agent uses tools, it will do so as you. For this reason, it will need your API keys and other identifying information.")
                with gr.Accordion("Lead Momentum Integration") as leadmo_box:
                    with gr.Row():
                        with gr.Column():
                            gradio.Markdown("These values are required for tools")
                            leadmo_api_key = gr.Textbox(info="Lead Momentum API Key",
                                                        label="Lead Momentum API Key", type="password",
                                                        placeholder="REQUIRED",
                                                        elem_id="leadmo_api_key",
                                                        elem_classes=["user_profile"])
                            leadmo_location_id = gr.Textbox(info="Lead Momentum 'Location ID'",
                                                            label="Lead Momentum Location ID",
                                                            placeholder="REQUIRED",
                                                            elem_id="leadmo_location_id",
                                                            elem_classes=["user_profile"])
                            user_leadmo_details = [leadmo_api_key, leadmo_location_id]
                            gr.Markdown(f"[API Key]({PORTAL_URL}/dashboard)")

                        with gr.Column():
                            gradio.Markdown("Optional values, used for testing", label="Optional Information")
                            leadmo_calendar_id = gr.Textbox(info="*Required", label="Lead Momentum Calendar ID", placeholder="OPTIONAL", elem_id="leadmo_calendar_id", elem_classes=["user_profile"])
                            first_name = gr.Textbox(info="Optional", label="First Name", placeholder="John", elem_id="first_name", elem_classes=["user_profile"])

                            last_name = gr.Textbox(info="Optional", label="Last Name", placeholder="Smith", elem_id="last_name", elem_classes=["user_profile"])
                            date_of_birth = gr.Textbox(info="Optional", label="Date of Birth", placeholder="1970-04-01", elem_id="date_of_birth", elem_classes=["user_profile"])
                            phone = gr.Textbox(info="*Required", label="Phone", placeholder="+16198675309", elem_id="phone", elem_classes=["user_profile"])
                            address1 = gr.Textbox(info="Optional", label="Address 1", placeholder="123 4th St.", elem_id="address1", elem_classes=["user_profile"])
                        with gr.Column():
                            gradio.Markdown("Optional values, used for testing", label="Optional Information")

                            address2 = gr.Textbox(info="Optional", label="Address 2", placeholder="Apt 123", elem_id="address2", elem_classes=["user_profile"])

                            city = gr.Textbox(info="Optional", label="City", placeholder="San Diego", elem_id="city", elem_classes=["user_profile"])
                            state = gr.Textbox(info="Optional", label="State", placeholder="CA", elem_id="state", elem_classes=["user_profile"])
                            country = gr.Textbox(info="*Required", label="Country", placeholder="US", elem_id="country", elem_classes=["user_profile"])
                            postal_code = gr.Textbox(info="Optional Code", label="Postal Code", placeholder="92108", elem_id="postal_code", elem_classes=["user_profile"])
                            website = gr.Textbox(info="Optional", label="Website", placeholder="openbra.in", elem_id="website", elem_classes=["user_profile"])

                            user_personal_details = [leadmo_calendar_id, first_name, last_name, date_of_birth, phone, address1, address2, city, state, country, postal_code, website]

                    with gr.Accordion("Landline Scrubber Integration", render=False) as lls_box:
                        lls_api_key = gr.Textbox(info="Landline Scrubber API Key", label="Landline Scrubber API Key", type="password", placeholder="YourLeadMoAPIKey", elem_id="lls_api_key", elem_classes=["user_profile"])
            with gr.Row():
                user_profile_save_button = gr.Button("Save", size="sm", variant="primary", elem_id="save_user_profile_button", elem_classes=["user_profile"])
                user_profile_load_button = gr.Button("reload", size="sm", variant="secondary", elem_id="load_user_profile_button", elem_classes=["user_profile"])

            user_profile_tab.select(load_client_details, inputs=[username],
                                           outputs=user_leadmo_details + user_personal_details)

        with gr.Tab("Stats for Nerds") as stats_tab:
            with gr.Column():
                with gr.Row():
                    with gr.Column():
                        agent_stats = gr.Image(label="Agents", elem_id="agent_stats", type="filepath", interactive=False)
                    with gr.Column():
                        review_stats = gr.Image(label="Reviews", elem_id="review_stats", type="filepath", interactive=False)

                    with gr.Column():
                        tool_stats = gr.Image(label="Tools", elem_id="tool_stats", type="filepath", interactive=False)


                    stats_tab.select(get_agent_stats, inputs=[username], outputs=[agent_stats])

                    stats_tab.select(get_review_stats, inputs=[username], outputs=[review_stats])

                    stats_tab.select(get_tool_stats, inputs=[username], outputs=[tool_stats])


    with gr.Accordion("AI Agent Configuration and Tuning", elem_classes="accordion", visible=is_settings_set(), open=False) as prompts_box:

        with gr.Tab("LLM Parameters") as tuning_tab:
            gr.Markdown(
                "Changes to these settings are used to set up a conversation using the Reset button and will not "
                "be reflected until the next 'Reset'"
            )

            with gr.Row() as preferences_row1:
                options = model_agent_config.EXECUTOR_MODEL_TYPES
                default_llm_types = ["function"]
                llm_types = gr.CheckboxGroup(
                    choices=options,
                    label="LLM Types",
                    info="List only the types of agents you are interested in.",
                    value=default_llm_types,
                    elem_id="llm_types",
                    elem_classes=["agent_config"],
                )
                original_choices = model_agent_config.FUNCTION_LANGUAGE_MODELS
                # original_value = openbrain.orm.model_agent_config.FUNCTION_LANGUAGE_MODELS[0]
                llm = gr.Dropdown(
                    choices=original_choices,
                    filterable=True,
                    # value=original_value,
                    label="LLM",
                    info="The language model to use for completion",
                    elem_id="llm",
                    elem_classes=["agent_config"],
                )

                with gr.Column() as extra_options_column:
                    record_tool_actions = gr.Checkbox(
                        label="Record Tool Actions", info="Record tool actions (use 'Actions' box).", elem_id="record_tool_actions", elem_classes=["agent_config"]
                    )
                    record_conversations = gr.Checkbox(label="Record Conversations", info="Record conversations.", elem_id="record_conversations", elem_classes=["agent_config"])

                # executor_completion_model = gr.Dropdown( choices=["text-davinci-003", "text-davinci-002",
                # "text-curie-001", "text-babbage-001", "text-ada-001"], label="Executor Completion Model",
                # info="This is the model used when Executor Model Type is set to 'completion'" )

            with gr.Row() as preferences_row2:
                executor_temp = gr.Slider(
                    minimum=0,
                    maximum=2,
                    label="Temperature",
                    step=0.1,
                    info="Higher temperature for 'spicy' agents.",
                    elem_id="executor_temp",
                    elem_classes=["agent_config"],
                )
                max_execution_time = gr.Slider(
                    minimum=0,
                    maximum=120,
                    label="Max Execution Time",
                    step=0.5,
                    info="Maximum agent response time before termination.",
                    elem_id="max_execution_time",
                    elem_classes=["agent_config"],
                )
                max_iterations = gr.Number(
                    label="Max Iterations",
                    info="Number of steps an agent can take for a response before termination.",
                    elem_id="max_iterations",
                    elem_classes=["agent_config"],
                )
        info_message = "Select tools to enable for the agent" #if LEADMO_INTEGRATION else "Select tools to enable for the agent. Lead Momentum integration is currently disabled in this environment."
        with gr.Tab("Tools") as preferences_row3:
            tools = gr.CheckboxGroup(choices=TOOL_NAMES, value=[], label="Tools", info=info_message, elem_id="tools", elem_classes=["agent_config"])

            tools.change(warn_if_missing_tool_info, inputs=[username, tools])

            gr.Markdown(
                value="Tool descriptions as presented to the AI. Confusing text here could lead to inconsistent use of tools."
            )
            _tools = discovered_tools
            with gr.Column() as tool_accordion:
                for _tool in _tools:
                    with gr.Tab(_tool.name):
                        gr.Markdown(value=get_tool_description(_tool.name), elem_id=f"{_tool.name}_description", elem_classes=["tool_description"])

        with gr.Tab("System Message") as long_text_row1:
            system_message = gr.TextArea(
                lines=10,
                label="System Message",
                placeholder="Enter your system message here",
                info="The System Message. This message is a part of every context with "
                "ChatGPT, and is therefore the most influential, and expensive place to "
                "add text",
                show_label=False,
                elem_id="system_message",
                elem_classes=["agent_config"],
            )

        with gr.Tab("Icebreaker") as long_text_row2:
            icebreaker = gr.TextArea(
                lines=10,
                label="Icebreaker",
                placeholder="Enter your icebreaker here",
                show_label=False,
                info="The first message to be sent to the user.",
                elem_id="icebreaker",
                elem_classes=["agent_config"],
            )



        with gr.Tab("Documentation") as help_tab:
            gr.Markdown(value=get_help_text())

        with gr.Tab("Conversation Analysis") as conversation_analysis_tab:
            gr.Markdown(value="NOT IMPLEMENTED")

    with gr.Accordion("Interact with Agent") as chat_accordian:
        with gr.Row() as chat_row:
            with gr.Column(scale=2) as chat_container:
                with gr.Column(scale=2) as chat_column:
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    resources_path = os.path.join(current_dir, "resources")
                    avatars_path = os.path.join(resources_path, "avatars")
                    ai_avatar_path = os.path.join(avatars_path, "icons8-ai-64.png")
                    # human_avatar_path = os.path.join(avatars_path, "icons8-human-64.png")
                    human_avatar_path = os.path.join(avatars_path, "emotional-intelligence.png")
                    chatbot = gr.Chatbot(
                        show_share_button=False,
                        show_copy_button=True,
                        likeable=True,
                        avatar_images=(human_avatar_path, ai_avatar_path),
                        layout="bubble",
                        elem_id="chatbot",
                        elem_classes=["chatbot"],
                    )
                    with gradio.Row():
                        msg = gr.Textbox(placeholder="Type a message...", label="Message", elem_id="msg", elem_classes=["chatbot"], show_label=False, scale=20)

            with gr.Column(scale=1) as context_container:

                with gr.Row():

                    always_update_leadmo_contact = gr.Checkbox(value=True, visible=False, interactive=False)

                    update_leadmo_contact = gr.Checkbox(label="Track Contact", info="Auto create/refresh user", show_label=True, elem_id="update_leadmo_contact", elem_classes=["context"], value=False)
                    voice_enabled = gr.Checkbox(label="Speak", info="Incoming messages are spoken", show_label=True, value=False)


                with gr.Tab("Context") as context_tab:
                    fetch_user_from_leadmo_button = gr.Button("Fetch or create Leadmo user", size="sm",
                                                              variant="secondary", elem_id="fetch_user_button",
                                                              elem_classes=["context"], scale=10)

                    context = gr.JSON(
                        label="Context",
                        show_label=False,
                        value={},
                    )

                with gr.Tab("Appointments") as appointments_tab:
                    fetch_appointments_from_leadmo_button = gr.Button("Fetch Leadmo Appointments", size="sm",
                                                              variant="secondary", elem_id="fetch_appointments_button",
                                                              elem_classes=["context"], scale=10)

                    appointments = gr.JSON(
                        label="Appointments",
                        show_label=False,
                        value={},
                    )

                with gr.Tab("Audio") as audio_tab:
                    audio = gr.Audio()

                chat_button = gr.Button("Chat", variant="primary", elem_id="chat_button", elem_classes=["chatbot"], interactive=False)
                reset_agent = gr.Button("Reset", variant="secondary", elem_id="reset_button", elem_classes=["chatbot"])


    with gr.Accordion("Debugging", open=False) as debug_box:
        with gr.Tab("Bug reports and feature requests") as feedback_tab:
            feedback_input = gr.MultimodalTextbox(
                label="Feedback",
                placeholder="Report a bug, or request a feature, attach screenshots or other helpful files.",
                show_label=False,
                lines=5,
                file_count="single",
                elem_id="feedback",
                elem_classes=["feedback"],
                file_types=["image", "video", "text"]
            )

        with gr.Tab("Gradio logs") as debug_tab:
            debug_text = gr.Textbox(
                label="Debug",
                info="Debugging information",
                show_label=False,
                lines=20,
                value=get_debug_text,
                interactive=False,
                autoscroll=True,
                show_copy_button=True,
                every=1.0,
                elem_id="debug_text",
                elem_classes=["debug"],
            )

        with gr.Tab("API Logs") as agent_debug_tab:
            api_debug_text = gr.TextArea(
                label="Debug",
                # info="Debugging information",
                show_label=False,
                lines=20,
                value=get_aws_cloudwatch_logs,
                interactive=False,
                autoscroll=True,
                show_copy_button=True,
                elem_id="api_debug_text",
                elem_classes=["debug"],
            )
            refresh_api_logs_button = gr.Button("Refresh", size="sm", variant="secondary", elem_id="refresh_api_logs_button", elem_classes=["debug"])

        with gr.Tab("Agent Logs") as agent_logs:
            agent_debug_text = gr.Textbox(
                value=get_gpt_agent_logs,
                label="Debug",
                info="GptAgent logs",
                show_label=False,
                lines=20,
                interactive=False,
                autoscroll=True,
                show_copy_button=True,
                every=3.0,
                elem_id="agent_debug_text",
                elem_classes=["debug"],
            )
            refresh_agent_logs_button = gr.Button("Refresh", size="sm", variant="secondary")

        with gr.Tab("Action Event Logs"):
            # events_str = get_action_events()
            # events = gr.Json(value=events_str, label="Latest action event recorded.")
            events = gr.Json(
                value={},
                # every=15.0,
                label="Latest action recorded.",
                elem_id="events",
                elem_classes=["debug"],
            )


    with gr.Row() as bottom_text_row:
        logout_button = gr.Button("Logout", link="/logout", variant="secondary", size="sm", scale=1, elem_id="logout_button", elem_classes=["auth"])

        with gr.Column(scale=20):
            bottom_text = gr.Markdown(value=get_bottom_text(), rtl=True, elem_id="bottom_text", elem_classes=["bottom_text"])

    preferences = [
        icebreaker,
        system_message,
        llm,
        max_iterations,
        max_execution_time,
        executor_temp,
        profile_name,
        client_id,
        record_tool_actions,
        record_conversations,
        tools,
        llm_types,
    ]
    fetch_user_from_leadmo_button.click(fetch_user_from_leadmo,
                                        inputs=[always_update_leadmo_contact, context, username],
                                        outputs=[context])

    user_profile_save_button.click(fill_context, inputs=[username] + user_leadmo_details + user_personal_details,
                                   outputs=[context])
    for context_item in user_personal_details + user_leadmo_details:
        context_item.change(fill_context, inputs=[username] + user_leadmo_details + user_personal_details, outputs=[context])

    # Refresh Buttons
    refresh_api_logs_button.click(get_aws_cloudwatch_logs, inputs=[session_state], outputs=[api_debug_text])
    refresh_agent_logs_button.click(get_gpt_agent_logs, outputs=[agent_debug_text])
    # refresh_events_button.click(get_action_events, inputs=[events, session_state], outputs=[events])
    user_profile_load_button.click(load_client_details, inputs=[username], outputs=user_leadmo_details + user_personal_details)

    # Save Buttons
    user_profile_save_button.click(save_client_details, inputs=[username] + user_leadmo_details + user_personal_details, outputs=[])


    # Save Agent Button
    save_agent_profile_button.click(
        save,
        inputs=[
            icebreaker,
            system_message,
            llm,
            max_iterations,
            max_execution_time,
            executor_temp,
            profile_name,
            client_id,
            record_tool_actions,
            record_conversations,
            tools,
        ],
    )
    # main_block.load(update_client_id, [username, session_state], [client_id])
    # Load Agent Button
    load_agent_profile_button.click(load, inputs=[profile_name, client_id], outputs=preferences)

    # Chat Button
    chat_button.click(fn=chat, inputs=[msg, chatbot, profile_name, session_state, client_id, context], outputs=[msg, chatbot, session_state, context]).then(alert_on_actions, inputs=[session_state], outputs=[session_state, events]).then(fetch_user_from_leadmo, inputs=[update_leadmo_contact, context, username], outputs=[context])
    chat_button.click(get_aws_cloudwatch_logs, inputs=[session_state], outputs=[agent_debug_text])
    chat_button.click(get_bottom_text, inputs=[session_state, client_id, profile_name], outputs=[bottom_text])

    msg.submit(chat, [msg, chatbot, profile_name, session_state, client_id, context], [msg, chatbot, session_state, context]).then(alert_on_actions, inputs=[session_state], outputs=[session_state, events]).then(fetch_user_from_leadmo, inputs=[update_leadmo_contact, context, username], outputs=[context])
    msg.submit(get_aws_cloudwatch_logs, inputs=[session_state], outputs=[agent_debug_text])
    msg.submit(get_bottom_text, inputs=[session_state, client_id, profile_name], outputs=[bottom_text])

    # Chat Reset Button
    reset_agent.click(
        fn=reset,
        inputs=[client_id, profile_name, chatbot, session_state, context],
        outputs=[msg, chatbot, session_state, context],
    )
    reset_agent.click(get_bottom_text, inputs=[session_state, client_id, profile_name], outputs=[bottom_text])
    # reset_agent.click(get_bottom_text, inputs=[session_state, profile_name, client_id], outputs=[context])
    reset_agent.click(get_aws_cloudwatch_logs, inputs=[session_state], outputs=[agent_debug_text])
    # reset_agent.click(get_action_events, inputs=[events, session_state], outputs=[events])
    reset_agent.click(enable_chat_button, outputs=[chat_button])
    feedback_input.submit(submit_feedback, inputs=[feedback_input, username], outputs=[])
    reset_agent.click(alert_on_actions, inputs=[session_state], outputs=[session_state, events]).then(fetch_user_from_leadmo, inputs=[update_leadmo_contact, context, username], outputs=[context])

    fetch_appointments_from_leadmo_button.click(fetch_appointments_from_leadmo, inputs=[username, context], outputs=[appointments])
    # On Change Events
    llm_types.change(get_llm_choices, inputs=[llm_types], outputs=[llm])
    client_id.change(update_available_profile_names, inputs=[client_id], outputs=[profile_name])
    client_id.change(enable_or_disable_save, inputs=[client_id, profile_name], outputs=[save_agent_profile_button])
    profile_name.change(enable_or_disable_save, inputs=[client_id, profile_name], outputs=[save_agent_profile_button])

    # profile_name.change(load, inputs=[profile_name, client_id], outputs=preferences)
    main_block.load(initialize_username, [], [username, client_id])

    username.change(load, inputs=[profile_name, username], outputs=preferences)
    username.change(set_client_id, inputs=[username], outputs=[client_id])
    # username.change(generate_context, [username], [context])
    username.change(fill_context_from_username, inputs=[username], outputs=[context])

    chatbot.change(speak, inputs=[voice_enabled, chatbot, session_state], outputs=[audio])
    chatbot.like(react_to_message, [chatbot, session_state, profile_name, client_id], [])

    update_leadmo_contact.change(fetch_user_from_leadmo, inputs=[update_leadmo_contact, context, username], outputs=[context])

if __name__ == "__main__":
    if os.getenv("GRADIO_PORT"):
        gradio_host = os.getenv("GRADIO_HOST", '0.0.0.0')
        gradio_port = int(os.getenv("GRADIO_PORT", 7861))
        main_block.launch(
            debug=True,
            share=False,
            server_name=gradio_host,
            server_port=gradio_port,
        )
