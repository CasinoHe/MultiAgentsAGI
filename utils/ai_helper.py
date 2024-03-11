"""
Small tools that using llm
"""
import autogen  # type: ignore  the autogen path has been added in the main.py
import json

# Load LLM inference endpoints from an env variable or a file
config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST")


def fix_broken_json(potential_json: str, max_attempts: int = 10) -> str:
    """
    """
    FIX_JSON_PROMPT = f"""You are a helpful assistant. A user will ask a question, and you should provide an answer.
    ONLY return the answer, and nothing more.

    Given the following potential JSON text, please fix any broken JSON syntax. Do NOT change the text itself. ONLY respond with the fixed JSON.

    Potential JSON:
    ---
    {potential_json}
    ---

    Response:
    """

    attempts = 0
    error = None
    while attempts < max_attempts:
        try:
            attempts += 1
            print("Trying to use AIGC to fix broken JSON...")
            client = autogen.OpenAIWrapper(config_list=config_list)
            response = client.create(
                response_format={"type": "json_object"},
                messages=[{"role": "user", "content": FIX_JSON_PROMPT}],
            )
            response = autogen.ConversableAgent._format_json_str(response.choices[0].message.content)
            response = json.loads(response)
            return response
        except Exception as error:
            print("FIX ATTEMPT FAILED, TRYING AGAIN...", attempts)
            error = error

    print("Cannot fix broken JSON after max attempts..., returning error")
    raise error


def get_end_intent(message):

    IS_TERMINATE_SYSTEM_PROMPT = """You are an expert in text and sentiment analysis. Based on the provided text, please respond with whether the intent is to end/pause the conversation or contintue the conversation. If the text provides all-caps statements such as "TERMINATE" or "CONTINUE", prioritize these when assesing intent. Your response MUST be in JSON format, with the following format:
    {{
        "analysis": <your analysis of the text>,
        "intent": "end" or "continue"
    }}

    NOTE: If the intent is to get feedback from the User or UserProxy, the intent should be "end".

    IMPORTANT: ONLY respond with the JSON object, and nothing else. If you respond with anything else, the system will not be able to understand your response.

    """

    client = autogen.OpenAIWrapper(config_list=config_list)
    response = client.create(
        messages=[
            {"role": "system", "content": IS_TERMINATE_SYSTEM_PROMPT},
            {"role": "user", "content": message["content"]},
        ]
    )
    response = autogen.ConversableAgent._format_json_str(response.choices[0].message.content)
    try:
        json_response = json.loads(response)
    except Exception:
        json_fix_response = fix_broken_json(json_response)
        # if cannot fix the json, return end
        if isinstance(json_fix_response, Exception):
            print("Cannot fix the end intent of the message, RETURN end...")
            return "end"
        else:
            json_response = json_fix_response
    return json_response.get("intent", "end")
