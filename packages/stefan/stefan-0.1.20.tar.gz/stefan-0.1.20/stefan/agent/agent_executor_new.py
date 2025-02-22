import traceback
from typing import Any, List, Dict, Tuple
from stefan.agent.agent_definition import AgentDefinition
from stefan.agent.agent_result import AgentResult
from stefan.agent.prompt_agents_use_creator import create_agents_use_prompt
from stefan.agent.prompt_answer import create_answer_format_prompt
from stefan.agent.prompt_file_paths_rules import create_file_paths_rules_prompt
from stefan.agent.prompt_metadata_project_context import create_metadata_project_context_prompt
from stefan.agent.prompt_template import PromptTemplate
from stefan.agent.prompt_tools_use_creator import create_tools_use_prompt
from stefan.code_search.llm.llm_executor import LLMExecutor, LLMSuccessResult
from stefan.code_search.llm.llm_model import LLM_MODEL
from stefan.dependencies.service_locator import ServiceLocator
from stefan.execution_context import ExecutionContext
from stefan.execution_tree.execution_tree_data import AgentInputData, AgentInputDataSource, AgentOutputAction, ExecutionParams, FinishAgentAction, LLMMessage, MessageRole, StartChildAgentAction, StartChildToolAction, TokenUsageData
from stefan.tool.tool_attempt_completion import ATTEMPT_COMPLETITION_TOOL_NAME
from stefan.tool.tool_definition import ToolDefinition
from stefan.tool.tool_executor import ToolExecutor
from stefan.utils.xml_answer_parser import XMLAnswerParser

class AgentExecutorNew:
    def __init__(self, agent: AgentDefinition, service_locator: ServiceLocator, main_agent_model: LLM_MODEL, child_agent_model: LLM_MODEL):
        self.agent = agent
        self.service_locator = service_locator
        self.execution_tree = self.service_locator.get_execution_tree_builder()
        self.main_agent_model = main_agent_model
        self.child_agent_model = child_agent_model

    def start_agent_by_user(self, user_request: str, context: ExecutionContext) -> AgentResult:
        try:
            params_str = f"User request: {user_request}"
            return self._start_agent_internal(params_str=params_str, context=context)
        except Exception as error:
            return self._create_failure_agent_response(self.agent.name, error)
        
    def _start_agent_internal(self, params_str: str, context: ExecutionContext) -> AgentResult:
    
        messages = self._create_initial_agent_messages(params_str=params_str, context=context)
        
        self._on_new_agent_created(params_str=params_str, messages=messages, context=context)

        while True:
            # Get agent response from LLM
            success_result, error = LLMExecutor().generate(
                tag=self.agent.llm_tag,
                model=self.main_agent_model if context.parent_agent is None else self.child_agent_model,
                messages=messages,
                execution_context=context,
                force_local_log=True,
            ).unpack()

            # If there was an error, return the failure response
            if error is not None:
                context.project_context.service_locator.get_llm_logger().log_agent_finished_with_error(error, context)
                self.execution_tree.update_last_agent_node_with_error(error=error)
                return self._create_failure_agent_response(self.agent.name, error)
            
            # Get agent response from LLM
            response = success_result.response

            # Repsonse should be alwasys returned as a xml wrapped with <answer> tags. Parse the answer as xml and map it into dict
            xml_answer = XMLAnswerParser.parse_answer_xml(response, preserve_order=["commands"]) # TODO: Make this configurable, should not be hardcoded
            xml_text = xml_answer.xml_text
            answer_dict = xml_answer.answer_dict

            # Extract the first key from the answer dict (should be either agent or tool name)
            answer_key = self._get_first_answer_key(answer_dict)
            
            # Try to extract the agent or tool from the answer key
            agent, tool = self._get_agent_or_tool_from_answer_key(answer_key)

            # If the tool is the attempt completion tool, finish the agent
            if tool is not None and tool.name == ATTEMPT_COMPLETITION_TOOL_NAME:
                self._on_agent_finished_with_success(
                    success_result=success_result,
                    output_action=FinishAgentAction(
                        params=ExecutionParams(
                            params={
                                "agent_result": xml_text,
                            },
                        ),
                    ),
                    context=context,
                )
                return AgentResult.create_success(xml_text)


            # Execute tool if needed
            tool_output: str | None = None
            if tool is not None:
                tool_params = answer_dict[tool.name]

                # Empty string means that the tool was used but no parameters were provided
                # <answer><tool_name></tool_name></answer>
                if isinstance(tool_params, str) and tool_params == "":
                    tool_params = {}

                # Non empty string means that the tool was used with no-name parameters
                # This should not happen, but we should handle it just in case
                # <answer><tool_name>Something<tool_name></answer>
                elif isinstance(tool_params, str) and tool_params != "":
                    tool_params = {"content": tool_params}
               
                self._on_agent_finished_with_success(
                    success_result=success_result,
                    output_action=StartChildToolAction(
                        child_tool_name=tool.name,
                        params=ExecutionParams(
                            params=tool_params,
                        ),
                    ),
                    context=context,
                )
                
                tool_output = self._execute_tool_and_return_string_result(tool, tool_params, context)

            # Execute agent if needed
            agent_output: str | None = None
            if agent is not None:
                self._on_agent_finished_with_success(
                    success_result=success_result,
                    output_action=StartChildAgentAction(
                        child_agent_name=agent.name,
                        params=ExecutionParams(
                            params={
                                "agent_request": xml_text,
                            },
                        ),
                    ),
                    context=context,
                )
                
                agent_output = self._execute_agent_and_return_string_result(agent, xml_text, context)

            # Add response as new assistant message
            messages.append({
                "role": "assistant", 
                "content": response
            })

            # Add tool or agent result as new user message
            next_agent_node_source: AgentInputDataSource
            next_agent_node_data: str

            if tool_output is not None:
                messages.append({
                    "role": "user",
                    "content": tool_output
                })
                next_agent_node_data = tool_output
                next_agent_node_source = AgentInputDataSource.TOOL_RESULT

            elif agent_output is not None:
                messages.append({
                    "role": "user",
                    "content": agent_output
                })
                next_agent_node_data = agent_output
                next_agent_node_source = AgentInputDataSource.AGENT_RESULT
            else:
                raise ValueError(f"No tool or agent was used in response. Answer: {xml_text}")
            
            self.execution_tree.create_agent_node(
                agent_name=self.agent.name,
                input_data=AgentInputData(
                    params=ExecutionParams(
                        params={
                            "result": next_agent_node_data,
                        },
                    ),
                    source=next_agent_node_source,
                ),
                messages=messages,
                model_name=self.main_agent_model if context.parent_agent is None else self.child_agent_model,
                temperature=0.0, # TODO do not make this hardcoded
                max_tokens=100000, # TODO do not make this hardcoded
            )
            
    def _execute_tool_and_return_string_result(self, tool: ToolDefinition, args: Dict[str, Any], context: ExecutionContext) -> str:
        self._on_new_tool_created(
            tool_name=tool.name,
            args=args,
            context=context,
        )

        tool_executor = ToolExecutor(tool)
        tool_result = tool_executor.execute_tool(
            args=args,
            context=context,
        )
        
        if tool_result.error is not None:
            self._on_tool_finished_with_error(tool.name, tool_result.error, context=context)
            return self._create_failure_tool_response(tool.name, tool_result.error)
        else:
            self._on_tool_finished_with_success(tool.name, tool_result.result, context=context)
            return f"Response from tool '{tool.name}':\n{tool_result.result}"
        
    def _execute_agent_and_return_string_result(self, agent: AgentDefinition, request: str, context: ExecutionContext) -> str:
        new_context = context.copy(
            current_agent=self.agent,
            parent_agent=context.current_agent,
            depth=context.depth + 1,
        )

        agent_executor = AgentExecutorNew(
            agent=agent, 
            service_locator=self.service_locator,
            main_agent_model=self.main_agent_model,
            child_agent_model=self.child_agent_model
        )
        agent_result = agent_executor._start_agent_internal(
            params_str=request,
            context=new_context,
        )
        if agent_result.error is not None:
            return self._create_failure_agent_response(agent.name, agent_result.error)
        else:
            return f"Response from agent '{agent.name}':\n{agent_result.result}"

    def _get_agent_or_tool_from_answer_key(self, answer_key: str) -> Tuple[AgentDefinition | None, ToolDefinition | None]:
        agent = self._try_get_agent_for_key(answer_key)
        tool = self._try_get_tool_for_key(answer_key)
        if agent is None and tool is None:
            raise ValueError(f"Answer key {answer_key} is not a valid agent or tool name")
        if agent is not None and tool is not None:
            raise ValueError(f"Answer key {answer_key} is not unique, it is both an agent and a tool name")
        return agent, tool


    def _get_first_answer_key(self, answer_dict: Dict[str, Any]) -> str:
        answer_keys = list(answer_dict.items())

        # Make sure that agent answer contains only one key (either tool or agent name)
        if len(answer_keys) == 0:
            raise ValueError(f"Agent answer is empty: {answer_dict}")
        if len(answer_keys) > 1:
            raise ValueError(f"Agent answer should contain only one key: {answer_dict}")
        
        return answer_keys[0][0] # answer_keys[0] is a tuple (key, value) so [0][0] is the value

    def _try_get_agent_for_key(self, answer_key: str) -> str:
        agent_name_to_agent_map = {agent.name: agent for agent in self.agent.available_agents}
        if answer_key not in agent_name_to_agent_map:
            return None
        return agent_name_to_agent_map[answer_key]
    
    def _try_get_tool_for_key(self, answer_key: str) -> str:
        tool_name_to_tool_map = {tool.name: tool for tool in self.agent.available_tools}
        if answer_key not in tool_name_to_tool_map:
            return None
        return tool_name_to_tool_map[answer_key]

    def _validate_agent_answer_elements_count(self, answer_dict: Dict[str, Any]) -> None:
        if len(answer_dict) == 0:
            raise ValueError("Agent answer is empty")
        if len(answer_dict) > 1:
            raise ValueError("Agent answer should contain only one key")

    def _create_initial_agent_messages(self, params_str: str, context: ExecutionContext) -> List[Dict[str, Any]]:
        prompt_template = PromptTemplate(
            tools_use_prompt=create_tools_use_prompt(self.agent.available_tools, context=context),
            agents_use_prompt=create_agents_use_prompt(self.agent.available_agents),
            file_paths_rules_prompt=create_file_paths_rules_prompt(),
            metadata_project_context_prompt=create_metadata_project_context_prompt(context=context),
            answer_format_prompt=create_answer_format_prompt(),
        )
        
        return [
            {
                "role": "system",
                "content": self.agent.create_system_prompt(prompt_template=prompt_template, context=context),
            },
            {
                "role": "user",
                "content": params_str,
            },
        ]        

    def _on_new_agent_created(self, params_str: str, messages: List[Dict[str, Any]], context: ExecutionContext) -> None:
        source: AgentInputDataSource
        if context.parent_agent is not None:
            source = AgentInputDataSource.AGENT_CREATED_BY_AGENT
        else:
            source = AgentInputDataSource.AGENT_CREATED_BY_USER

        self.execution_tree.create_agent_node(
            agent_name=self.agent.name,
            input_data=AgentInputData(
                params=ExecutionParams(
                    params={
                        "request": params_str,
                    },
                ),
                source=source,
            ),
            messages=messages,
            model_name=self.main_agent_model if context.parent_agent is None else self.child_agent_model,
            temperature=0.0,
            max_tokens=100000,
        )

        context.project_context.service_locator.get_llm_logger().log_agent_started(context)

    def _on_new_tool_created(self, tool_name: str, args: Dict[str, Any], context: ExecutionContext) -> None:
        self.execution_tree.create_tool_node(
            tool_name=tool_name,
            input_data=ExecutionParams(
                params=args,
            ),
        )
         
        context.project_context.service_locator.get_llm_logger().log_tool_usage(
            agent_name=self.agent.name,
            tool_name=tool_name,
            execution_context=context,
        )

    def _on_agent_finished_with_success(self, success_result: LLMSuccessResult, output_action: AgentOutputAction, context: ExecutionContext) -> None:
        self.execution_tree.update_last_agent_node_with_success(
            llm_response=LLMMessage(role=MessageRole.ASSISTANT, content=success_result.response),
            token_usage=TokenUsageData(
                prompt_tokens=success_result.token_usage_input,
                completion_tokens=success_result.token_usage_output,
                total_tokens=success_result.token_usage_input + success_result.token_usage_output,
                cost=success_result.cost,
            ),
            output_action=output_action,
        )
        context.project_context.service_locator.get_llm_logger().log_agent_finished(context)
    
    def _on_agent_finished_with_error(self, error: Exception, context: ExecutionContext) -> None:
        self.execution_tree.update_last_agent_node_with_error(error)
        context.project_context.service_locator.get_llm_logger().log_agent_finished_with_error(error, context)
         
    def _on_tool_finished_with_success(self, tool_name: str, result: str, context: ExecutionContext) -> None:
        self.execution_tree.update_last_tool_node_with_success(
            output_data=result,
            output_metadata={},
        )
        context.project_context.service_locator.get_llm_logger().log_tool_success(tool_name=tool_name, agent_name=self.agent.name, execution_context=context)

    def _on_tool_finished_with_error(self, tool_name: str, error: Exception, context: ExecutionContext) -> None:
        self.execution_tree.update_last_tool_node_with_error(error)
        context.project_context.service_locator.get_llm_logger().log_tool_error(tool_name=tool_name, agent_name=self.agent.name, error=error, execution_context=context)

    def _create_failure_tool_response(self, tool_name: str, error: Exception) -> str:
        error_message = f"Tool '{tool_name}' failed with the following error: {str(error)}"
        traceback_str = ''.join(traceback.format_tb(error.__traceback__))
        stack_trace = f"Stack trace:\n{traceback_str}"
        return f"{error_message}\n\n{stack_trace}"
    
    def _create_failure_agent_response(self, agent_name: str, error: Exception) -> AgentResult:
        error_message = f"Agent '{agent_name}' failed with the following error: {str(error)}"
        traceback_str = ''.join(traceback.format_tb(error.__traceback__))
        stack_trace = f"Stack trace:\n{traceback_str}"
        error_message = f"{error_message}\n\n{stack_trace}"
        return AgentResult.create_failure(error_message, error)