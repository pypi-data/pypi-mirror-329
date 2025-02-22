
from stefan.code_search.code_search_persistence import CodeSearchPersistence
from stefan.code_search.code_search_tree_creator import CodeSearchTreeCreator
from stefan.code_search.code_search_tree_processor import CodeSearchTreeProcessor
from stefan.code_search.llm.llm_directory_description import DirectoryDescriptionLLMProcessor
from stefan.code_search.llm.llm_executor import LLMExecutor
from stefan.code_search.llm.llm_file_description import FileDescriptionLLMProcessor
from stefan.code_search.llm.llm_file_relevancy import FileRelevancyLLMProcessor
from stefan.project_configuration import ProjectContext


def perform_code_search(project_context: ProjectContext):
    """Create CodeSearch instance with real implementations"""

    
        # Create processors with fake executors
        llm_executor = LLMExecutor()
        file_desc_processor = FileDescriptionLLMProcessor(llm_executor)
        dir_desc_processor = DirectoryDescriptionLLMProcessor(llm_executor)
        file_relevancy_processor = FileRelevancyLLMProcessor(llm_executor)
        
        # Create real implementations
        tree_processor = CodeSearchTreeProcessor(
            llm_file_processor=file_desc_processor,
            llm_directory_processor=dir_desc_processor,
        )
        tree_builder = CodeSearchTreeCreator(
            project_context=project_context,
        )
        persistence = CodeSearchPersistence()
        
        # Create project context
        project_context = ProjectContext(
            root_directory=temp_directory,
            include_patterns=["*.py"],
            exclude_patterns=[".git", "__pycache__"]
        )
        
        return CodeSearch(
            tree_processor=tree_processor,
            tree_builder=tree_builder,
            llm_file_relevancy=file_relevancy_processor,
            persistence=persistence,
            project_context=project_context,
        )

if __name__ == "__main__":
    main()