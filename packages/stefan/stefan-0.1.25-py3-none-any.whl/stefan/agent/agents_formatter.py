import inspect
from stefan.agent.agent_definition import AgentDefinition

class AgentFormatter:

    def format_agent(self, agent: AgentDefinition) -> str:
        """
        Formats the agent information for display.
        
        Returns:
            str: Formatted agent information.
        """

        agent_params = "\n".join([f"- {key}: {value}" for key, value in agent.parameters.items()])

        return inspect.cleandoc(f"""
            ## {agent.name}
            
            # Description:
            {agent.description}
                               
            # Parameters:
            {agent_params}
                               
            # Usage:
            {agent.usage}
        """)