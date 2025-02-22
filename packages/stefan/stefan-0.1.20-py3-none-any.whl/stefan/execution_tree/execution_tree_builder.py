import json
import os
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel

from stefan.execution_tree.execution_tree_data import (
    AgentExecutionNode,
    AgentExecutionStatus,
    AgentInputData,
    AgentInputDataSource,
    AgentOutputAction,
    BaseExecutionNode,
    ExecutionError,
    ExecutionNodeType,
    ExecutionParams,
    FinishAgentAction,
    LLMMessage,
    MessageRole,
    ModelConfigData,
    StartChildAgentAction,
    StartChildToolAction,
    TimeExecutionData,
    TokenUsageData,
    ToolExecutionNode,
    ToolExecutionStatus,
)
from stefan.project_configuration import ProjectContext


class ExecutionTreeBuilder:
    def __init__(self, project_context: ProjectContext):
        self.nodes: List[BaseExecutionNode] = []
        self.active_agents_ids: List[UUID] = []
        self.project_context = project_context

    def create_agent_node(
        self,
        agent_name: str,
        input_data: ExecutionParams,
        messages: Optional[List[LLMMessage]],
        model_name: str,
        temperature: Optional[float],
        max_tokens: Optional[int],
    ) -> AgentExecutionNode:
        
        self._assert_previous_node_status_for_new_agent_node(input_data=input_data)

        # Create agent node id
        node_id = uuid4()
        self.project_context.service_locator.get_llm_logger().log_executor(f"Creating agent node {agent_name} - {node_id}")
        
        # Get parent ID BEFORE modifying active_agents_ids
        parent_agent_id = self._get_parent_agent_id_for_new_agent()

        # Add new agent to active agents list AFTER getting parent ID
        match input_data.source:
            case AgentInputDataSource.AGENT_CREATED_BY_USER:
                self.active_agents_ids.append(node_id)
            case AgentInputDataSource.AGENT_CREATED_BY_AGENT:
                self.active_agents_ids.append(node_id)
            case AgentInputDataSource.AGENT_RESULT:
                pass
            case AgentInputDataSource.TOOL_RESULT:
                pass

        node = AgentExecutionNode(
            # Execution node properties
            id=node_id,
            parent_agent_id=parent_agent_id,
            node_type=ExecutionNodeType.AGENT,
            name=agent_name,
            depth=self._get_depth_for_new_agent(),
            time_execution_data=TimeExecutionData(
                start_time=datetime.now(),
                end_time=None,
            ),

            # Agent execution node properties
            execution_status=AgentExecutionStatus.STARTED,
            input_data=input_data,
            llm_messages=messages,
            model_config_data=ModelConfigData(
                model_name=model_name,
                temperature=temperature,
                max_tokens=max_tokens,
            ),

            # Agent execution node properties (these properties are set when agent is finished)
            llm_response=None,
            token_usage=None,
            output_action=None,
            output_error=None,
        )
        
        # Add node to the list of nodes
        self.nodes.append(node)

        self._on_node_updated()

        return node
    
    def create_tool_node(
        self,
        tool_name: str,
        input_data: ExecutionParams,
    ) -> ToolExecutionNode:
        self.project_context.service_locator.get_llm_logger().log_executor(f"Creating tool node {tool_name}")

        self._assert_previous_node_status_for_new_tool_node()

        node = ToolExecutionNode(
            # Execution node properties
            id=uuid4(),
            parent_agent_id=self._get_parent_agent_id_for_tool(),
            node_type=ExecutionNodeType.TOOL,
            name=tool_name,
            depth=self._get_depth_for_new_tool(),
            time_execution_data=TimeExecutionData(
                start_time=datetime.now(),
                end_time=None,
            ),

            # Tool execution node properties
            input_data=input_data,
            execution_status=ToolExecutionStatus.RUNNING,

            # Tools execution node properties (these properties are set when tool is finished)
            output_data=None,
            output_metadata=None,
            output_error=None,
        )

        # Add node to the list of nodes
        self.nodes.append(node)

        self._on_node_updated()

        return node
    
    def update_last_agent_node_with_success(
        self,
        llm_response: LLMMessage,
        token_usage: TokenUsageData,
        output_action: AgentOutputAction,
    ) -> AgentExecutionNode:       
        self.project_context.service_locator.get_llm_logger().log_executor(f"Updating last agent node with success {output_action}")

        last_agent_node = self._get_last_node_as_agent_node()
        last_agent_node.time_execution_data.end_time = datetime.now()

        match output_action:
            case FinishAgentAction():
                # Agent is finished, remove it from active agents
                self.active_agents_ids.pop()
                last_agent_node.execution_status=AgentExecutionStatus.COMPLETED
            case StartChildAgentAction():
                last_agent_node.execution_status=AgentExecutionStatus.CONTINUE
            case StartChildToolAction():
                last_agent_node.execution_status=AgentExecutionStatus.CONTINUE
            case _:
                raise ValueError(f"Invalid output action: {output_action}")

        # Agent execution node properties
        last_agent_node.llm_response = llm_response
        last_agent_node.token_usage = token_usage
        last_agent_node.output_action = output_action
        last_agent_node.output_error = None

        self._on_node_updated()

        return last_agent_node
    
    def update_last_agent_node_with_error(
        self,
        error: Exception,
    ) -> AgentExecutionNode:
        self.project_context.service_locator.get_llm_logger().log_executor("Updating last agent node with error")

        last_agent_node = self._get_last_node_as_agent_node()

        # Execution node properties
        last_agent_node.time_execution_data.end_time = datetime.now()
        last_agent_node.execution_status=AgentExecutionStatus.FAILED

        # Agent execution node properties
        last_agent_node.llm_response = None
        last_agent_node.token_usage = None
        last_agent_node.output_action = None
        last_agent_node.output_error = error

        # Remove the last active agent
        self.active_agents_ids.pop()
        self._on_node_updated()

        return last_agent_node
    
    def update_last_tool_node_with_success(
        self,
        output_data: ExecutionParams,
        output_metadata: Dict[str, str],
    ) -> ToolExecutionNode:
        self.project_context.service_locator.get_llm_logger().log_executor("Updating last tool node with success")
        
        last_tool_node = self._get_last_node_as_tool_node()

        # Execution node properties
        last_tool_node.time_execution_data.end_time = datetime.now()
        last_tool_node.execution_status=ToolExecutionStatus.COMPLETED

        # Tool execution node properties
        last_tool_node.output_data = output_data
        last_tool_node.output_metadata = output_metadata
        last_tool_node.output_error = None

        self._on_node_updated()

        return last_tool_node
    
    def update_last_tool_node_with_error(
        self,
        error: Exception,
    ) -> ToolExecutionNode:
        self.project_context.service_locator.get_llm_logger().log_executor("Updating last tool node with error")

        last_tool_node = self._get_last_node_as_tool_node()

        # Execution node properties
        last_tool_node.time_execution_data.end_time = datetime.now()
        last_tool_node.execution_status=ToolExecutionStatus.FAILED

        # Tool execution node properties
        last_tool_node.output_data = None
        last_tool_node.output_metadata = None
        last_tool_node.output_error = error

        self._on_node_updated()
        
        return last_tool_node
    
    def dump_tree(self) -> str:
        def custom_json_serializer(obj):
            if isinstance(obj, (UUID, Enum)):
                return str(obj)
            if isinstance(obj, datetime):
                return obj.isoformat()
            if isinstance(obj, BaseModel):
                return obj.model_dump()
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

        return json.dumps(self.nodes, default=custom_json_serializer, indent=2)
    
    def get_total_cost(self) -> float:
        total_cost = 0.0
        for node in self.nodes:
            if isinstance(node, AgentExecutionNode) and node.token_usage is not None:
                total_cost += node.token_usage.cost
        return total_cost
    
    def get_total_execution_time(self) -> timedelta:
        if not self.nodes:
            return timedelta()
        
        first_node = self.nodes[0]
        end_time = datetime.now()
        
        return end_time - first_node.time_execution_data.start_time
    
    def _on_node_updated(self) -> None:
        if self.project_context.execution_tree_settings.save_on_update:
            self._save_tree_to_file()

    def _save_tree_to_file(self) -> None:
        dir = self.project_context.execution_directory / "execution_tree"
        execution_id = self.project_context.execution_id

        os.makedirs(dir, exist_ok=True)
        with open(f'{dir}/execution_tree_{execution_id}.json', 'w') as f:
            f.write(self.dump_tree())
    
    def _get_depth_for_new_agent(self) -> int:
        return len(self.active_agents_ids) - 1
    
    def _get_depth_for_new_tool(self) -> int:
        return len(self.active_agents_ids)
    
    def _get_last_node_as_agent_node(self) -> AgentExecutionNode:
        self._assert_nodes_non_empty()
        last_agent_node = self.nodes[-1]
        self._assert_node_is_agent_node(last_agent_node)
        return last_agent_node
    
    def _get_last_node_as_tool_node(self) -> ToolExecutionNode:
        self._assert_nodes_non_empty()
        last_tool_node = self.nodes[-1]
        self._assert_node_is_tool_node(last_tool_node)
        return last_tool_node
    
    def _get_parent_agent_id_for_new_agent(self) -> UUID:
        return self.active_agents_ids[-1] if self.active_agents_ids else None    
    
    def _get_parent_agent_id_for_tool(self) -> UUID:
        self._assert_nodes_non_empty()
        return self.active_agents_ids[-1] if self.active_agents_ids else None  
    
    def _assert_previous_node_is_agent_node(self):
        self._assert_nodes_non_empty()
        last_node = self.nodes[-1]
        if not isinstance(last_node, AgentExecutionNode):
            raise ValueError(f"Previous node is not an agent node but {last_node}")
        
    def _assert_previous_node_is_tool_node(self):
        self._assert_nodes_non_empty()
        last_node = self.nodes[-1]
        if not isinstance(last_node, ToolExecutionNode):
            raise ValueError(f"Previous node is not a tool node but {last_node}")
        
    def _assert_previous_node_status_for_new_agent_node(self, input_data: AgentInputData):
        if len(self.nodes) == 0:
            return # No previous node is expected for the first agent node
        last_node = self.nodes[-1]
        if isinstance(last_node, AgentExecutionNode) and last_node.execution_status == AgentExecutionStatus.STARTED:
            raise ValueError(f"Previous node is unfinished agent node {last_node}")
        if isinstance(last_node, ToolExecutionNode) and last_node.execution_status == ToolExecutionStatus.RUNNING:
            raise ValueError(f"Previous node is unfinished tool node {last_node}")
        
        match input_data.source:
            case AgentInputDataSource.AGENT_CREATED_BY_USER:
                self._assert_nodes_empty()
            case AgentInputDataSource.AGENT_CREATED_BY_AGENT:
                self._assert_previous_node_is_agent_node()
            case AgentInputDataSource.AGENT_RESULT:
                self._assert_previous_node_is_agent_node()
            case AgentInputDataSource.TOOL_RESULT:
                self._assert_previous_node_is_tool_node()
        
    def _assert_previous_node_status_for_new_tool_node(self):
        self._assert_nodes_non_empty()
        last_node = self.nodes[-1]
        if isinstance(last_node, AgentExecutionNode) and last_node.execution_status == AgentExecutionStatus.STARTED:
            raise ValueError(f"Previous node is unfinished agent node {last_node}")
        if isinstance(last_node, ToolExecutionNode):
            raise ValueError(f"Tool node is expected to have agent node as a parent {last_node}")
    
    def _assert_nodes_empty(self):
        if len(self.nodes) != 0:
            raise ValueError("Nodes list is expected to be empty")

    def _assert_nodes_non_empty(self):
        if len(self.nodes) == 0:
            raise ValueError("No agent is started")
        
    def _assert_nodes_at_least_two(self):
        if len(self.nodes) <= 2:
            raise ValueError("No agent is started")
    
    def _assert_node_is_agent_node(self, node: BaseExecutionNode):
        if not isinstance(node, AgentExecutionNode):
            raise ValueError(f"Last node is not an agent node but {node}")
        
    def _assert_node_is_tool_node(self, node: BaseExecutionNode):
        if not isinstance(node, ToolExecutionNode):
            raise ValueError(f"Last node is not a tool node but {node}")
    
if __name__ == "__main__":
    tree = ExecutionTreeBuilder(create_dummy_project_context())
    tree.nodes = []

    # Start main agent (depth 0)
    tree.create_agent_node(
        agent_name="MainAgent",
        input_data=AgentInputData(
            params=ExecutionParams(params={"task": "Analyze and improve code"}),
            source=AgentInputDataSource.AGENT_CREATED_BY_USER
        ),
        messages=[
            LLMMessage(role=MessageRole.SYSTEM, content="You are a code analysis assistant"),
            LLMMessage(role=MessageRole.USER, content="Please analyze this code")
        ],
        model_name="gpt-4",
        temperature=0.7,
        max_tokens=1000
    )

    # Update main agent to continue with analyzer tool
    tree.update_last_agent_node_with_success(
        llm_response=LLMMessage(
            role=MessageRole.ASSISTANT,
            content="Let's analyze the code first"
        ),
        token_usage=TokenUsageData(
            prompt_tokens=100,
            completion_tokens=50,
            total_tokens=150,
            cost=0.002
        ),
        output_action=StartChildToolAction(
            child_tool_name="CodeAnalyzer",
            params=ExecutionParams(params={"task": "Analyze code"})
        )
    )

    # Start and complete code analyzer tool
    tree.create_tool_node(
        tool_name="CodeAnalyzer",
        input_data=ExecutionParams(params={"file": "main.py", "action": "analyze"})
    )
    
    tree.update_last_tool_node_with_success(
        output_data=ExecutionParams(params={"findings": "3 improvements needed"}),
        output_metadata={"duration": "1.2s", "lines_analyzed": "150"}
    )

    # Before updating the main agent again, we need to create a new agent node for it
    tree.create_agent_node(
        agent_name="MainAgent",
        input_data=AgentInputData(
            params=ExecutionParams(params={"task": "Process analyzer results"}),
            source=AgentInputDataSource.TOOL_RESULT
        ),
        messages=[
            LLMMessage(role=MessageRole.SYSTEM, content="You are a code analysis assistant"),
            LLMMessage(role=MessageRole.USER, content="Process analyzer results")
        ],
        model_name="gpt-4",
        temperature=0.7,
        max_tokens=1000
    )

    # Now we can update the main agent to start refactor agent
    tree.update_last_agent_node_with_success(
        llm_response=LLMMessage(
            role=MessageRole.ASSISTANT,
            content="Analysis completed, starting refactor"
        ),
        token_usage=TokenUsageData(
            prompt_tokens=150,
            completion_tokens=70,
            total_tokens=220,
            cost=0.003
        ),
        output_action=StartChildAgentAction(
            child_agent_name="RefactorAgent",
            params=ExecutionParams(params={"task": "Refactor based on analysis"})
        )
    )

    # Start refactor agent
    tree.create_agent_node(
        agent_name="RefactorAgent",
        input_data=AgentInputData(
            params=ExecutionParams(params={"task": "Refactor based on analysis"}),
            source=AgentInputDataSource.AGENT_CREATED_BY_AGENT
        ),
        messages=[
            LLMMessage(role=MessageRole.SYSTEM, content="You are a code refactoring specialist"),
            LLMMessage(role=MessageRole.USER, content="Implement the suggested improvements")
        ],
        model_name="gpt-4",
        temperature=0.5,
        max_tokens=800
    )

    # Update refactor agent to start refactor tool
    tree.update_last_agent_node_with_success(
        llm_response=LLMMessage(
            role=MessageRole.ASSISTANT,
            content="Starting refactoring process"
        ),
        token_usage=TokenUsageData(
            prompt_tokens=120,
            completion_tokens=30,
            total_tokens=150,
            cost=0.002
        ),
        output_action=StartChildToolAction(
            child_tool_name="RefactorTool",
            params=ExecutionParams(params={"changes": ["improvement1"]})
        )
    )

    # Start and complete refactor tool (with error)
    tree.create_tool_node(
        tool_name="RefactorTool",
        input_data=ExecutionParams(params={"file": "main.py", "changes": ["improvement1"]})
    )
    
    tree.update_tool_status_with_error(
        error=ExecutionError(
            message="Failed to apply changes",
            stacktrace="FileNotFoundError: main.py not found"
        )
    )

    tree.create_agent_node(
        agent_name="RefactorAgent",
        input_data=AgentInputData(
            params=ExecutionParams(params={"task": "Refactor based on analysis"}),
            source=AgentInputDataSource.TOOL_RESULT
        ),
        messages=[
            LLMMessage(role=MessageRole.SYSTEM, content="You are a code refactoring specialist"),
            LLMMessage(role=MessageRole.USER, content="Implement the suggested improvements")
        ],
        model_name="gpt-4",
        temperature=0.5,
        max_tokens=800
    )

    # Complete main agent
    tree.update_last_agent_node_with_success(
        llm_response=LLMMessage(
            role=MessageRole.ASSISTANT,
            content="Analysis completed with mixed results"
        ),
        token_usage=TokenUsageData(
            prompt_tokens=200,
            completion_tokens=100,
            total_tokens=300,
            cost=0.004
        ),
        output_action=FinishAgentAction(
            params=ExecutionParams(params={"final_status": "completed"})
        )
    )

    tree.create_agent_node(
        agent_name="RefactorAgent",
        input_data=AgentInputData(
            params=ExecutionParams(params={"task": "Refactor based on analysis"}),
            source=AgentInputDataSource.AGENT_RESULT
        ),
        messages=[
            LLMMessage(role=MessageRole.SYSTEM, content="You are a code refactoring specialist"),
            LLMMessage(role=MessageRole.USER, content="Implement the suggested improvements")
        ],
        model_name="gpt-4",
        temperature=0.5,
        max_tokens=800
    )

    # Complete main agent
    tree.update_last_agent_node_with_success(
        llm_response=LLMMessage(
            role=MessageRole.ASSISTANT,
            content="Analysis completed with mixed results"
        ),
        token_usage=TokenUsageData(
            prompt_tokens=200,
            completion_tokens=100,
            total_tokens=300,
            cost=0.004
        ),
        output_action=FinishAgentAction(
            params=ExecutionParams(params={"final_status": "completed"})
        )
    )

    # Dump the interaction tree to JSON
    tree_json = tree.dump_tree()
    
    with open(f'interaction_tree_{datetime.now().isoformat()}.json', 'w') as f:
        f.write(tree_json)

    