import random
from typing import List, Tuple
from datetime import datetime
from litellm import completion
from pydantic import BaseModel
import copy

from stefan.settings import Settings
from stefan.execution_context import ExecutionContext
from stefan.code_search.llm.llm_model import LLM_MODEL
from stefan.code_search.llm.llm_price_reporter import LLMPriceReporter
from stefan.code_search.llm.llm_tag import LLMTag
from stefan.utils.wrap_with_retry import OnRetryParams, wrap_with_retry

class LLMSuccessResult(BaseModel):
    response: str
    token_usage_input: int
    token_usage_output: int 
    cost: float

class LLMExecutorResult(BaseModel):
    success_result: LLMSuccessResult | None = None
    error: Exception | None = None

    class Config:
        arbitrary_types_allowed = True # Allow error to be an Exception

    def unpack(self) -> Tuple[LLMSuccessResult | None, Exception | None]: 
        return (self.success_result, self.error)

class LLMExecutor:

    def __init__(self, llm_price_reporter: LLMPriceReporter):
        self.price_reporter = llm_price_reporter

    def generate(
        self, 
        tag: LLMTag,
        model: LLM_MODEL, 
        messages: List[dict], 
        execution_context: ExecutionContext,
        *,
        force_local_log: bool = False,
        llm_request_id: str | None = None,
    ) -> LLMExecutorResult:    
        # Generate a unique request id if none is provided
        if llm_request_id is None:
            llm_request_id = f"{datetime.now().isoformat()}_{random.randint(1,100)}"

        # Load the API key
        settings = Settings()
        if model.is_openai_model():
            api_key = settings.openai_api_key
        elif model.is_anthropic_model():
            api_key = settings.anthropic_api_key
        elif model.is_deepseek_model():
            api_key = settings.deepseek_api_key
        else:
            raise ValueError(f"Unsupported model: {model}")
        
        # Get the model name
        model_name = model.get_model_name()

        # Log input
        execution_context.project_context.service_locator.get_llm_logger().log_input(
            tag=tag.value,
            model_name=model_name,
            messages=messages,
            llm_request_id=llm_request_id,
        )

        # Create a callback function for retries
        def _on_llm_retry(params: OnRetryParams):
            retry_count = params.retry_count
            delay = params.delay
            error = params.exception
            execution_context.project_context.service_locator.get_llm_logger().log_error(
                tag=tag.value,
                model_name=model_name,
                message=f"LLM call failed - attempt {retry_count} with delay {delay}. Error: {str(error)}",
                error=error,
                llm_request_id=llm_request_id,
            )

        # Add cache control in case of anthropic model
        if len(messages) > 2 and model.is_anthropic_model():
            # Create a deep copy of messages to avoid modifying the original
            messages_copy = copy.deepcopy(messages)
            # Add cache control only to the second to last message
            messages_copy[-2]["cache_control"] = {"type": "ephemeral"}
            # Replace the original messages with the modified copy
            messages = messages_copy

        # Make the API call
        try:
            model_response = wrap_with_retry(
                func=self._execute_llm_call,
                on_retry=_on_llm_retry,
                model_name=model_name,
                messages=messages,
                api_key=api_key
            )
        except Exception as error:
            # Log LLM final error
            execution_context.project_context.service_locator.get_llm_logger().log_error(
                tag=tag.value,
                model_name=model_name,
                message=f"LLM call failed - no attempts left. Error: {str(error)}",
                error=error,
                llm_request_id=llm_request_id,
            )
            return LLMExecutorResult(success_result=None, error=error)  
        
        # Get response from model
        response = model_response.choices[0].message.content + "</answer>"

        # Log LLM output
        execution_context.project_context.service_locator.get_llm_logger().log_output(
            tag=tag.value,
            model_name=model_name,
            response=response,
            llm_request_id=llm_request_id,
        )         

        # Report cost using both systems
        input_tokens = model_response.usage.prompt_tokens
        output_tokens = model_response.usage.completion_tokens
        cost = model_response._hidden_params["response_cost"]
        self.price_reporter.add_call(
            tag=tag.value,
            model=model_name,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost=cost,
            execution_context=execution_context
        )

        success_result = LLMSuccessResult(
            response=response,
            token_usage_input=input_tokens,
            token_usage_output=output_tokens,
            cost=cost,
        )
        return LLMExecutorResult(success_result=success_result, error=None)

    def get_cost_report(self) -> str:
        """Get a formatted report of all LLM costs"""
        return self.price_reporter.get_report()

    def _execute_llm_call(self, model_name: str, messages: List[dict], api_key: str):
        """Execute the LLM API call with retry logic"""
        return completion(
            model=model_name,
            temperature=0,
            messages=messages,
            api_key=api_key,
            stop="</answer>"
        )
