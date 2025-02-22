from __future__ import annotations

from stefan.code_search.code_search_full_text import CodeSearchFullText
from stefan.code_search.code_search_relevancy import CodeSearchRelevancy
from stefan.code_search.code_search_persistence import CodeSearchPersistence
from stefan.code_search.code_search_tree_creator import CodeSearchTreeCreator
from stefan.code_search.code_search_tree_processor import CodeSearchTreeProcessor
from stefan.code_search.llm.llm_directory_description import DirectoryDescriptionLLMProcessor
from stefan.code_search.llm.llm_file_description import FileDescriptionLLMProcessor
from stefan.code_search.llm.llm_file_relevancy import FileRelevancyLLMProcessor
from stefan.code_search.llm.llm_executor import LLMExecutor
from stefan.code_search.llm.llm_logger import LLMLogger
from stefan.execution_tree.execution_tree_builder import ExecutionTreeBuilder
from stefan.utils.async_execution import AsyncExecution

class ServiceLocator:

    def __init__(self):
        self.services = {}
        self.is_initialized = False
        self.EXECUTION_TREE_BUILDER = "execution_tree_builder"
        self.LLM_LOGGER = "llm_logger"

    def initialize(self):
        self._assert_not_initialized()
        self.is_initialized = True
    
    def set_llm_logger(self, llm_logger: LLMLogger):
        self._assert_initialized()
        self._assert_service_not_initialized(self.LLM_LOGGER)

        self.services[self.LLM_LOGGER] = llm_logger

    def get_llm_logger(self) -> LLMLogger:
        self._assert_initialized()
        self._assert_service_initialized(self.LLM_LOGGER)

        return self.services[self.LLM_LOGGER]

    def set_execution_tree_builder(self, execution_tree_builder: ExecutionTreeBuilder):
        self._assert_initialized()
        self._assert_service_not_initialized(self.EXECUTION_TREE_BUILDER)

        self.services[self.EXECUTION_TREE_BUILDER] = execution_tree_builder
    
    def get_execution_tree_builder(self) -> ExecutionTreeBuilder:
        self._assert_initialized()
        self._assert_service_initialized(self.EXECUTION_TREE_BUILDER)

        return self.services[self.EXECUTION_TREE_BUILDER]

    def create_llm_executor(self):
        self._assert_initialized()

        return LLMExecutor()
    
    def create_async_execution(self):
        self._assert_initialized()

        return AsyncExecution()
    
    def create_code_search(self, project_context):
        self._assert_initialized()

        llm_executor = self.create_llm_executor()
        async_execution = self.create_async_execution()
        file_desc_processor = FileDescriptionLLMProcessor(
            llm_executor=llm_executor,
        )
        dir_desc_processor = DirectoryDescriptionLLMProcessor(
            llm_executor=llm_executor,
        )
        file_relevancy_processor = FileRelevancyLLMProcessor(
            llm_executor=llm_executor,
            async_execution=async_execution,
        )
        tree_processor = CodeSearchTreeProcessor(
            llm_file_processor=file_desc_processor,
            llm_directory_processor=dir_desc_processor,
        )
        tree_builder = CodeSearchTreeCreator(
            project_context=self.project_context,
        )
        persistence = CodeSearchPersistence()
        
        return CodeSearchRelevancy(
            tree_processor=tree_processor,
            tree_builder=tree_builder,
            llm_file_relevancy=file_relevancy_processor,
            persistence=persistence,
            project_context=project_context,
        )
    
    def create_full_text_search(self, project_context):
        self._assert_initialized()

        return CodeSearchFullText(
            tree_builder=CodeSearchTreeCreator(
                project_context=project_context,
            ),
            project_context=project_context,
        )
    
    def _assert_service_initialized(self, service_name: str):
        if service_name not in self.services:
            raise ValueError(f"Service {service_name} is not initialized")
    
    def _assert_service_not_initialized(self, service_name: str):
        if service_name in self.services:
            raise ValueError(f"Service {service_name} is already initialized")

    def _assert_initialized(self):
        if not self.is_initialized:
            raise ValueError("ServiceLocator is not initialized. Call initialize() first.")
        
    def _assert_not_initialized(self):
        if self.is_initialized:
            raise ValueError("ServiceLocator is already initialized. initialize() should not be called again.")
