from stefan.agent.agent_search_code import SearchCodeAgent
from stefan.agent.agent_coder import CoderAgent
from stefan.agent.agent_planner import PlannerAgent

class AgentsFactory:

    def create_planner_agent(allow_self_use: bool) -> PlannerAgent:
        return PlannerAgent.create_instance(allow_self_use)

    def create_coder_agent() -> CoderAgent:
        return CoderAgent()
    
    def create_search_code_agent() -> SearchCodeAgent:
        return SearchCodeAgent()
