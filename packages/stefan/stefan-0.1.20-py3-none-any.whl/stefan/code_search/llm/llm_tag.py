from enum import Enum

class LLMTag(Enum):
    # Agents
    AGENT_PLANNER = "agent_planner"
    AGENT_CODER = "agent_coder"
    AGENT_KMP_CODER = "agent_kmp_coder"
    AGENT_SEARCH_CODE = "agent_search_code"
    AGENT_SAMPLES_PROVIDER = "agent_samples_provider"
    AGENT_TEXTS_UPDATER_ADVANCED = "agent_texts_updater_advanced"
    AGENT_TEXTS_UPDATER_SIMPLE = "agent_texts_updater_simple"

    # Code search
    CODE_SEARCH_DIRECTORY_DESCRIPTION = "code_search_directory_description"
    CODE_SEARCH_FILE_DESCRIPTION = "code_search_file_description"
    CODE_SEARCH_FILE_RELEVANCY = "code_search_file_relevancy"

    MONTE_CARLO_SOLUTION_EVALUATION = "monte_carlo_solution_evaluation"
