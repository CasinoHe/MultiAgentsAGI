import autogen  # type: ignore  the autogen path has been added in the main.py
import prompts
from utils import ai_helper

# Load LLM inference endpoints from an env variable or a file
config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST")
llm_config_dict = {"config_list": config_list}


user_proxy = autogen.UserProxyAgent(
    name="UserProxy",
    system_message=prompts.user_proxy.ONLY_WATCH_SYSTEM_PROMPT_V1,
    human_input_mode="TERMINATE",
    is_termination_msg=lambda x: ai_helper.get_end_intent(x) == "end",
    code_execution_config=False,
    llm_config=llm_config_dict
)

code_reviewer = autogen.AssistantAgent(
    name="CodeReviewer",
    system_message=prompts.code_reviewer.CODE_REVIEWER_SYSTEM_PROMPT_V1,
    llm_config=llm_config_dict,
)

agent_awareness_expert = autogen.AssistantAgent(
    name="AgentAwarenessExpert",
    system_message=prompts.agent_awareness_expert.LLM_FUNCTIONALITY_SYSTEM_PROMPT_V1,
    llm_config=llm_config_dict,
)

python_expert = autogen.AssistantAgent(
    name="PythonExpert",
    system_message=prompts.python_expert.CODE_COMPLETENESS_PYTHON_EXPERT_SYSTEM_PROMPT_V1,
    llm_config=llm_config_dict,
)

function_calling_agent = autogen.AssistantAgent(
    name="FunctionCallingAgent",
    system_message=prompts.function_calling_expert.ONLY_CALL_FUNCTION_SYSTEM_PROMPT_V1,
    llm_config=llm_config_dict,
)

code_execute_agent = autogen.AssistantAgent(
    name="CodeExecuteAgent",
    system_message=prompts.code_executor.ONLY_EXECUTE_CODE_SYSTEM_PROMPT_V1,
    llm_config=llm_config_dict,
)

creative_solution_agent = autogen.AssistantAgent(
    name="CreativeSolutionAgent",
    system_message=prompts.creative_solution_expert.CREATIVE_SOLUTION_AGENT_SYSTEM_PROMPT_V1,
    llm_config=llm_config_dict,
)

first_principles_thinker_agent = autogen.AssistantAgent(
    name="FirstPrinciplesThinkerAgent",
    system_message=prompts.first_principle_thinker.FIRST_PRINCIPLES_THINKER_SYSTEM_PROMPT_V1,
    llm_config=llm_config_dict,
)

project_manager_agent = autogen.AssistantAgent(
    name="ProjectManagerAgent",
    system_message=prompts.project_manager.PROJECT_MANAGER_SYSTEM_PROMPT_V1,
    llm_config=llm_config_dict,
)

task_history_review_agent = autogen.AssistantAgent(
    name="TaskHistoryReviewAgent",
    system_message=prompts.task_historical_reviewer.TASK_HISTORY_REVIEW_AGENT_SYSTEM_PROMPT_V1,
    llm_config=llm_config_dict,
)

task_comprehension_agent = autogen.AssistantAgent(
    name="TaskComprehensionAgent",
    system_message=prompts.task_comprehension_expert.TASK_COMPREHENSION_AGENT_SYSTEM_PROMPT_V1,
    llm_config=llm_config_dict,
)

AGENT_TEAM = [
    user_proxy,
    code_reviewer,
    agent_awareness_expert,
    python_expert,
    function_calling_agent,
    creative_solution_agent,
    first_principles_thinker_agent,
    project_manager_agent,
    task_history_review_agent,
    task_comprehension_agent
]
