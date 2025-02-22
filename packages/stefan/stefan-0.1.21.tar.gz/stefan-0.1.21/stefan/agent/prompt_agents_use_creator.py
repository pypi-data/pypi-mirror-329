from stefan.agent.agents_formatter import AgentFormatter
from stefan.agent.agent_definition import AgentDefinition

def create_agents_use_prompt(agents: list[AgentDefinition]) -> str:
    available_agents_description = "\n".join([AgentFormatter().format_agent(agent) for agent in agents])

    return _AGENTS_PROMPT.format(
        available_agents_description=available_agents_description,
    )

_AGENTS_PROMPT = """
# AGENTS USE

Agents are more sophisticated than tools. While tools perform specific, straightforward tasks like file manipulation or command execution, agents are capable of handling complex tasks by leveraging their own set of tools and decision-making processes. Agents can be thought of as autonomous entities that can receive tasks, process them using their unique capabilities, and produce results.

## When to use an agent

Agents are most effective when you need to perform a task that requires a combination of different tools and decision-making processes. Tools on the other hand are most effective when you need to perform a specific, straightforward task like reading a file or executing a command.

## Agent Use Formatting

Agent use is formatted using XML-style tags, similar to tools. Here's the structure:

<agent_name>
<task_description>Describe the task or action for the agent to perform</task_description>
<parameter1_name>value1</parameter1_name>
<parameter2_name>value2</parameter2_name>
</agent_name>

For example:

<agent_name>
<parameter1_name>Review the code for potential improvements and optimizations</parameter1_name>
<parameter2_name>src/main.py</parameter2_name>
</agent_name>

## Available agents

{available_agents_description}

## Agent Use Guidelines

1. In <thinking> tags, assess the task at hand and determine if it requires the capabilities of another agent.
2. Choose the most appropriate agent based on the task and the agent descriptions provided. Consider the agent's unique tools and style of thinking.
3. Formulate your agent use using the XML format specified for each agent.
4. After assigning a task to an agent, wait for the agent's response. This response will provide you with the necessary information to continue your task or make further decisions.

By leveraging agents, you can delegate complex tasks to specialized entities, allowing for more efficient and effective problem-solving. This approach enables you to focus on higher-level strategy while agents handle the detailed execution of tasks.
"""