import autogen  # type: ignore  the autogen path has been added in the main.py
import prompts
from utils import ai_helper

WORKING_DIR = "run_agi"
USE_DOCKER = False

# Load LLM inference endpoints from an env variable or a file
config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST")
llm_config_dict = {"config_list": config_list}


# ---------------------------------------  Create a consult archive group chat ---------------------------------------
inner_consult_archive_agent = autogen.AssistantAgent(
    name="ConsultArchiveAgent",
    system_message=prompts.consult_archive_expert.CONSULT_ARCHIVE_EXPERT_SYSTEM_PROMPT_V2,
    llm_config=llm_config_dict,
    description="An expert at consulting domain knowledge.",
)

inner_consult_archive_executor = autogen.UserProxyAgent(
    name="ConsultArchiveExecutor",
    system_message=prompts.consult_archive_expert.CONSULT_ARCHIVE_EXECUTOR_SYSTEM_PROMPT_V1,
    llm_config=False,  # disable llm reply, only execute consult archive tools
    human_input_mode="NEVER",
    code_execution_config={"work_dir": f"{WORKING_DIR}", "use_docker": USE_DOCKER},
    is_termination_msg=lambda: False,
    description="An executor angent in executing consult actions",
)

consult_archive_group = autogen.GroupChat(
    agents=[inner_consult_archive_agent, inner_consult_archive_executor],
    messages=[],
    speaker_selection_method="round_robin",  # With two agents, this is equivalent to a 1:1 conversation.
    allow_repeat_speaker=False,
    enable_clear_history=True,
    max_round=2,
    send_introductions=True,
)

consult_archive_group_manager = autogen.GroupChatManager(
    groupchat=consult_archive_group,
    is_termination_msg=lambda: False,
    llm_config=llm_config_dict,
    code_execution_config={
        "work_dir": f"{WORKING_DIR}",
        "use_docker": USE_DOCKER,
    },
)

consult_archive_agent = autogen.AssistantAgent(
    name="ConsultArchiveAgent",  # This is a nested group agent, use the nested group to consult archive
    llm_config=False,
    description="An expert at consulting domain knowledge.",
)

nested_consult_archive_chat_queue = [
    {"recipient": consult_archive_group_manager, "summary_method": "last_msg"},
]

consult_archive_agent.register_nested_chats(chat_queue=nested_consult_archive_chat_queue, trigger=autogen.AssistantAgent)

# ----------------------------------------------------------------------------------------------------------------------

user_proxy = autogen.UserProxyAgent(
    name="UserProxy",
    system_message=prompts.user_proxy.ONLY_WATCH_SYSTEM_PROMPT_V1,
    human_input_mode="TERMINATE",
    is_termination_msg=lambda x: ai_helper.get_end_intent(x) == "end",
    code_execution_config=False,
    llm_config=llm_config_dict,
    description="The user agent determines whether the conversation is ended.",
)

code_execute_agent = autogen.UserProxyAgent(
    name="CodeExecuteAgent",
    system_message=prompts.code_executor.ONLY_EXECUTE_CODE_SYSTEM_PROMPT_V1,
    human_input_mode="NEVER",
    is_termination_msg=lambda: False,
    code_execution_config={"work_dir": f"{WORKING_DIR}", "use_docker": USE_DOCKER},
    llm_config=False,  # disable llm reply, only execute locally
    description="A code and tool executor agent that only executes code and tools.",
)

code_reviewer = autogen.AssistantAgent(
    name="CodeReviewer",
    system_message=prompts.code_reviewer.CODE_REVIEWER_SYSTEM_PROMPT_V2,
    llm_config=llm_config_dict,
    description="A code reviewer that reviews code and provides feedback.",
)

python_expert = autogen.AssistantAgent(
    name="PythonExpert",
    system_message=prompts.python_expert.CODE_COMPLETENESS_PYTHON_EXPERT_SYSTEM_PROMPT_V2.format(
        CodeExecuteAgentName="CodeExecuteAgent",
        ConsultArchiveAgentName="ConsultArchiveAgent"),
    llm_config=llm_config_dict,
    description="A Python expert who provides fully developed, complete Python code but never executes it.",
)

creative_solution_agent = autogen.AssistantAgent(
    name="CreativeSolutionAgent",
    system_message=prompts.creative_solution_expert.CREATIVE_SOLUTION_AGENT_SYSTEM_PROMPT_V1,
    llm_config=llm_config_dict,
    # description="An expert at generating innovative, unconventional solutions, they excel in creative thinking and proposing unique, feasible ideas. Their role involves thinking outside the box, embracing complex challenges, collaborating for refined solutions, and inspiring others to expand their creative thinking.",
    description="An expert in innovative solutions who inspires others with unique, feasible ideas, fostering collaboration and unconventional approaches."
)

first_principles_thinker_agent = autogen.AssistantAgent(
    name="FirstPrinciplesThinkerAgent",
    system_message=prompts.first_principle_thinker.FIRST_PRINCIPLES_THINKER_SYSTEM_PROMPT_V1,
    llm_config=llm_config_dict,
    description="An expert in first principles thinking, adept at dissecting and solving complex problems from the ground up, focusing on fundamental truths and innovative, assumption-free solutions applicable across various domains.",
    # description="An expert in first principles thinking, skilled in simplifying complex problems and creating innovative, versatile solutions."
)

project_manager_agent = autogen.AssistantAgent(
    name="ProjectManagerAgent",
    system_message=prompts.project_manager.PROJECT_MANAGER_SYSTEM_PROMPT_V1,
    llm_config=llm_config_dict,
    description="As a Project Manager Agent, they excel in task coordination, resource allocation, risk management, clear communication, and meeting deadlines to efficiently achieve project goals.",
)

task_history_review_agent = autogen.AssistantAgent(
    name="TaskHistoryReviewAgent",
    system_message=prompts.task_historical_reviewer.TASK_HISTORY_REVIEW_AGENT_SYSTEM_PROMPT_V1,
    llm_config=llm_config_dict,
    description="The Agent specializes in reviewing and succinctly summarizing a team's task history, focusing on key actions and identifying gaps to ensure the team stays on track.",
)

task_comprehension_agent = autogen.AssistantAgent(
    name="TaskComprehensionAgent",
    system_message=prompts.task_comprehension_expert.TASK_COMPREHENSION_AGENT_SYSTEM_PROMPT_V1,
    llm_config=llm_config_dict,
    description="""The Agent expertly guides the team in task comprehension and knowledge limitations, frequently clarifying task goals and consulting "ConsultArchiveAgent" for domain-specific insights when needed.""",
)

AGENT_TEAM = [
    user_proxy,
    consult_archive_agent,
    code_reviewer,
    python_expert,
    code_execute_agent,
    creative_solution_agent,
    first_principles_thinker_agent,
    project_manager_agent,
    task_history_review_agent,
    task_comprehension_agent
]
