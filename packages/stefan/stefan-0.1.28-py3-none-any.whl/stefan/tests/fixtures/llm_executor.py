from typing import List

from openai import BaseModel
from sympy import Dict

from stefan.code_search.llm.llm_executor import LLMExecutorResult, LLMSuccessResult
from stefan.code_search.llm.llm_tag import LLMTag

class _FakeResponse(BaseModel):
    tag: LLMTag
    response: str

class _FixedResponse(BaseModel):
    response: str
    include_last_message: bool

class FakeLLMExecutor:

    def __init__(self):
        self.responses: Dict[LLMTag, List[_FakeResponse]] = {}
        self.fixed_response: Dict[LLMTag, _FixedResponse] = {}
        self.records = []

    # Region mock methods
    def add_response(self, tag: LLMTag, response: str):    
        if tag in self.fixed_response:
            raise ValueError("Cannot set response when fixed response is already set")
        
        if tag not in self.responses:
            self.responses[tag] = []
        self.responses[tag].append(_FakeResponse(tag=tag, response=response))

    def add_responses(self, tag: LLMTag, responses: List[str]):
        if tag in self.fixed_response:
            raise ValueError("Cannot set response when fixed response is already set")
    
        for response in responses:
            self.add_response(tag, response)

    def set_fixed_response(self, tag: LLMTag, response: str, include_last_message: bool = False):
        if tag in self.responses:
            raise ValueError("Cannot set fixed response when responses are already set")
        
        self.fixed_response[tag] = _FixedResponse(response=response, include_last_message=include_last_message)

    def assert_records_count_for_tag(self, tag: LLMTag, count: int):
        records_for_tag = [record for record in self.records if record["tag"] == tag]
        if len(records_for_tag) != count:
            raise ValueError(f"Expected {count} records, but got {len(records_for_tag)} {records_for_tag}")

    def assert_records_count_total(self, count: int):
        if len(self.records) != count:
            raise ValueError("Expected " + str(count) + " records, but got " + str(len(self.records)))
    # Endregion

    # Region generate method
    def generate(self, tag: LLMTag, model, messages: List[dict], execution_context, **kwargs) -> LLMExecutorResult:
        response = self._get_mocked_response(tag, messages)

        self.records.append({
            "tag": tag,
            "model": model,
            "messages": messages,
            "response": response,
        })

        return LLMExecutorResult(success_result=LLMSuccessResult(response=response, token_usage_input=0, token_usage_output=0, cost=0), error=None)
        
    def get_cost_report(self) -> str:
        return "Fake cost report"
    # Endregion
    
    def _get_mocked_response(self, tag: LLMTag, messages: List[dict]) -> str:
        fixed_response = self.fixed_response.get(tag, None)
        if fixed_response is not None:
            if fixed_response.include_last_message:
                return f"LAST MESSAGE:\n\n{messages[-1]['content']}\n\nRESPONSE MOCK:\n\n{fixed_response.response}"
            return fixed_response.response
        
        responses_for_tag = self.responses.get(tag, None)
        if responses_for_tag is None:
            raise ValueError(f"No responses set for tag: {tag}")
        if len(responses_for_tag) == 0:
            raise ValueError(f"No responses left for tag: {tag}")
        
        response = responses_for_tag.pop(0)
        return response.response
    
