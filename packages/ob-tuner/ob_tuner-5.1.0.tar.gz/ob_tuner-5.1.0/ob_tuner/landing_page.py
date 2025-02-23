import requests

from ob_tuner.functions.button_logic import *
from ob_tuner.util import *

WELCOME_MESSAGE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenBra.in Demo</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <h1>Welcome to OpenBra.in</h1>
        <p>OpenBra.in is a comprehensive platform designed to streamline the process of creating, testing, and deploying AI agents...</p>
    </header>

    <section id="features">
        <h2>Features</h2>
        <ul>
            <li>Interactive GUI: User-friendly Gradio interface for easy configuration and testing of AI agents.</li>
            <li>Real-time Testing: Immediate feedback on agent configurations and tool use.</li>
            <li>Flexible Configuration: Save, load, and manage various agent configurations.</li>
            <li>AWS Integration: Scalable, reliable infrastructure.</li>
            <li>Event-Driven Architecture: Efficient handling of actions and information retrieval through an event bus.</li>
            <li>Comprehensive Toolset: Includes tools for CRM integration, time management, and more.</li>
        </ul>
    </section>

    <section id="how-it-works">
        <h2>How It Works</h2>
        <p>OpenBra.in is built on a robust technical foundation that includes...</p>
        
        <h3>AI Tuning App</h3>
        <p>OB-Tuner is a user-friendly interface built on Gradio for creating, testing, and managing AI agent configurations...</p>
        
        <h3>OpenBrain API</h3>
        <p>The OpenBrain API provides a single chat endpoint for interacting with AI agents. Provide your `api_key`, your `client_id`, and the name of your saved agent.</p>
        
        <h3>Event-Driven Architecture</h3>
        <p>OpenBra.in uses an event bus to manage actions and information retrieval. This allows for recovery of failed tool runs using a DLQ.</p>
        
        <h3>Toolset</h3>
        <p>OpenBra.in includes a comprehensive set of tools for CRM integration with Lead Momentum. Tools can be enabled or disabled as needed on a per-agent basis.</p>
        
        <h3>RAG Infrastructure</h3>
        <p>Record agent tool use, and enable recording on a per agent basis. Use the `like` and `dislike` buttons to help fill the vector store with good example responses.</p>
                
    </section>

    <section id="getting-started">
        <h2>Getting Started</h2>
        <p>Steps to start using OpenBra.in...</p>
        <p>Installation and setup instructions...</p>
    </section>

    <section id="contact-support">
        <h2>Visit us on GitHub</h2>
        <a href="https://github.com/svange/openbrain/">OpenBra.in on GitHub</a>
    </section>

    <footer>
        <p>&copy; 2024 OpenBra.in</p>
    </footer>
</body>
</html>
"""

with gr.Blocks(analytics_enabled=False, theme="freddyaboulton/dracula_revamped") as landing_page:
    # Read the README file content
    with gr.Row():
        with gr.Column(scale=15):
            if NOAUTH_DEMO_PAGE:
                gr.Markdown(
                    value="# Welcome to OpenBra.in!\n Please enjoy the live demo. Load an agent profile, and start chatting with the AI. Explore the tools. If you are interested in trying OpenBra.in, please sign up for an account. Once signed up you can create and save your own agent profiles.\nDeployed agents can be used in your own applications via the OpenBra.in API, the following website is using the `openbrain` `promoter` agent.\n\n[OpenBra.in Demo Website](https://www.openbra.in/) (allow 15 seconds for the agent to initialize).")
            else:
                gr.Markdown(value="# Welcome!\n Please sign up or login. ")

        with gr.Column(scale=1) as login_column:
            gr.Button("Sign up / Login", link="/login", variant="secondary", size="sm")
            # gr.Button("Signup", link="/signup", variant="secondary", size="sm")

    if NOAUTH_DEMO_PAGE:

        with gr.Tab("Demo"):
            session_state = gr.State(value={
                "session_id": "",
                "session": requests.Session(),
                "agent": None,
                "last_response": None,
                "username": "",
                "events": [],
                "audio_warning_triggered": False,
                # "initial_reset": False
            })

            with gr.Tab("Selected Agent Configuration") as submit_tab:
                with gr.Row() as submit_row:
                    with gr.Column(scale=3) as key_text_column:
                        with gr.Row() as key_text_row:
                            client_id = gr.Dropdown(
                                label="Client ID",
                                info="Develop your own AI agents or use a community agent.",
                                choices=["openbrain"],
                                value="openbrain",
                            )

                            profile_name = gr.Dropdown(
                                allow_custom_value=True,
                                label="Profile Name",
                                info="The name of your AgentConfig. Defaults to 'default'",
                                choices=[str(DEFAULT_PROFILE_NAME), 'promoter'],
                                value='promoter',
                                interactive=False,
                            )

                    with gr.Column(scale=1) as submit_column:
                        load_agent_profile_button = gr.Button(value="Reload Agent", variant="secondary")
                        save_agent_profile_button = gr.Button(value="Save Agent", variant="secondary", render=True, interactive=False)

            with gr.Accordion("AI Agent Configuration and Tuning", elem_classes="accordion", visible=is_settings_set(),
                              open=False) as prompts_box:
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
                        )
                        original_choices = model_agent_config.FUNCTION_LANGUAGE_MODELS
                        # original_value = openbrain.orm.model_agent_config.FUNCTION_LANGUAGE_MODELS[0]
                        llm = gr.Dropdown(
                            choices=original_choices,
                            # value=original_value,
                            label="LLM",
                            info="The language model to use for completion",
                        )

                        with gr.Column() as extra_options_column:
                            record_tool_actions = gr.Checkbox(
                                label="Record Tool Actions", info="Record tool actions (use 'Actions' box).",
                                interactive=False
                            )
                            record_conversations = gr.Checkbox(label="Record Conversations",
                                                               info="Record conversations.",
                                                               interactive=False)

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
                        )
                        max_execution_time = gr.Slider(
                            minimum=0,
                            maximum=120,
                            label="Max Execution Time",
                            step=0.5,
                            info="Maximum agent response time before termination.",
                        )
                        max_iterations = gr.Number(
                            label="Max Iterations",
                            info="Number of steps an agent can take for a response before termination.",
                        )

                with gr.Tab("Tools") as preferences_row3:
                    tools = gr.CheckboxGroup(choices=TOOL_NAMES, value=[], label="Tools",
                                             info="Select tools to enable for the agent", interactive=False)

                    gr.Markdown(
                        value="Tool descriptions as presented to the AI. Confusing text here could lead to inconsistent use of tools."
                    )
                    _tools = discovered_tools
                    with gr.Column() as tool_accordion:
                        for _tool in _tools:
                            with gr.Tab(_tool.name):
                                gr.Markdown(value=get_tool_description(_tool.name))

                with gr.Tab("System Message") as long_text_row1:
                    system_message = gr.TextArea(
                        lines=10,
                        label="System Message",
                        placeholder="Enter your system message here",
                        info="The System Message. This message is a part of every context with "
                             "ChatGPT, and is therefore the most influential, and expensive place to "
                             "add text",
                        show_label=False,
                    )

                with gr.Tab("Icebreaker") as long_text_row2:
                    icebreaker = gr.TextArea(
                        lines=10,
                        label="Icebreaker",
                        placeholder="Enter your icebreaker here",
                        show_label=False,
                        info="The first message to be sent to the user.",
                    )

                with gr.Tab("Audio") as audio_tab:
                    audio = gr.Audio()

                with gr.Tab("Documentation") as help_tab:
                    gr.Markdown(value=get_help_text())

            with gr.Accordion("Interact with Agent") as chat_accordian:
                with gr.Row() as chat_row:
                    with gr.Column(scale=2) as chat_container:
                        with gr.Column(scale=2) as chat_column:
                            chatbot = gr.Chatbot(
                                show_share_button=True,
                                show_copy_button=True,
                                # avatar=(user_avatar_path, ai_avatar_path),
                                likeable=True,
                                # layout="panel",
                                layout="bubble",

                            )
                            with gr.Row():
                                msg = gr.Textbox(placeholder="Type a message...", label="Message", elem_id="msg",
                                                 elem_classes=["chatbot"], show_label=False, scale=20)
                                voice_enabled = gr.Checkbox(label="", scale=1, info="Speak", show_label=False )

                    with gr.Column(scale=1) as context_container:
                        initial_value_str = json.loads(json.dumps({
                            "first_name": "John",
                            "last_name": "Doe",
                            "locationId": "loc-123456",
                            "calendarId": "cal-123456",
                            "random_word": "Rambutan"
                        }))

                        gr.Markdown("OpenBra.in's API accepts arbitrary key/value pairs. Tools like book appointment require parameters like `calendarId=23nio2n3nf2oi32`, which cause halucinations. This gets around that by creating tools with values sent in by the API call.")
                        context = gr.JSON(
                            label="Context",
                            value=initial_value_str
                        )
                        landing_page.load(lambda: gr.JSON(label="Context", value=initial_value_str), outputs=[context])

                        chat_button = gr.Button("Chat", variant="primary", interactive=False)
                        reset_agent = gr.Button("Reset", variant="secondary")

                        msg.submit(
                            chat,
                            [msg, chatbot, profile_name, session_state, client_id, context],
                            [msg, chatbot, session_state, context],
                        )

            with gr.Row() as bottom_text_row:
                logout_button = gr.Button("Logout", link="/logout", variant="secondary", size="sm", scale=1, render=False)
                with gr.Column(scale=10):
                    bottom_text = gr.Markdown(value=get_bottom_text(), rtl=True)

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

            # Refresh Buttons

            save_agent_profile_button.click(
                fn=lambda: gr.Warning("Saving disabled in the demo, please sign up for an account."))
            load_agent_profile_button.click(load, inputs=[profile_name, client_id], outputs=preferences)

            profile_name.change(load, inputs=[profile_name, client_id], outputs=preferences)
            landing_page.load(load, inputs=[profile_name, client_id], outputs=preferences)

            # Chat Button
            chat_button.click(
                fn=chat,
                inputs=[msg, chatbot, profile_name, session_state, client_id, context],
                outputs=[msg, chatbot, session_state, context],
            )
            dummy_text = gr.Textbox(visible=False)
            chat_button.click(get_aws_cloudwatch_logs, inputs=[session_state], outputs=[dummy_text])

            # Chat Reset Button
            reset_agent.click(
                fn=reset,
                inputs=[client_id, profile_name, chatbot, session_state, context],
                outputs=[msg, chatbot, session_state, context],
            )
            # reset_agent.click(get_bottom_text, inputs=[session_state, profile_name, client_id], outputs=[context])
            reset_agent.click(get_aws_cloudwatch_logs, inputs=[session_state], outputs=[dummy_text])
            # reset_agent.click(get_action_events, inputs=[dummy_text, session_state], outputs=[dummy_text])
            reset_agent.click(enable_chat_button, outputs=[chat_button])

            # On Change Events
            llm_types.change(get_llm_choices, inputs=[llm_types], outputs=[llm])
            # client_id.change(update_available_profile_names, inputs=[client_id], outputs=[profile_name])
            chatbot.change(speak, inputs=[voice_enabled, chatbot, session_state], outputs=[audio])

    with gr.Tab(f"Welcome to {CUSTOMER_NAME}"):
        gr.HTML(WELCOME_MESSAGE)


if __name__ == "__main__":
    if os.getenv("GRADIO_PORT"):
        gradio_host = os.getenv("GRADIO_HOST", '0.0.0.0')
        gradio_port = int(os.getenv("GRADIO_PORT", 7861))
        landing_page.launch(
            debug=True,
            share=False,
            server_name=gradio_host,
            server_port=gradio_port,
        )
