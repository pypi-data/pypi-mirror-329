def create_answer_format_prompt() -> str:
    return _PROMPT

_PROMPT = """
You should finish your every response with the following format:

<answer>
    <tool_or_agent_name>
        <tool_or_agent_parameters>Example parameter</tool_or_agent_parameters>
    </tool_or_agent_name>
</answer>

tool_or_agent_name and tool_or_agent_parameters are just examples, you should use only the actual tool or agent that are available to you

Example of valid response:

IMPORTANT:
- You should use <answer>...</answer> only once in your response!!!
- The answer should be the last thing in your response!!!
- Each xml tag should be indented by 4 spaces!!!
- It should be valid xml format!!!
- All xml tags must be valid and closed!!!
- The output should be always wrapped with<answer>...</answer> tags.

"""