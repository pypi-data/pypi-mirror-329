import pytest

from stefan.execution_tree.execution_tree_builder import ExecutionTreeBuilder
from stefan.execution_tree.execution_tree_data import (
    ExecutionParams, AgentInputData,
    AgentInputDataSource, LLMMessage, MessageRole, TokenUsageData,
    StartChildAgentAction, StartChildToolAction, FinishAgentAction,
    AgentExecutionStatus, ToolExecutionStatus
)
from stefan.tests.fixtures.dummy_project_context import create_dummy_project_context

@pytest.fixture
def tree_builder():
    builder = ExecutionTreeBuilder(create_dummy_project_context())
    builder.nodes = []
    return builder

def test_single_agent_lifecycle(tree_builder):
    # Create initial agent
    agent = tree_builder.create_agent_node(
        agent_name="MainAgent",
        input_data=AgentInputData(
            params=ExecutionParams(params={"task": "test"}),
            source=AgentInputDataSource.AGENT_CREATED_BY_USER
        ),
        messages=[],
        model_name="test-model",
        temperature=0.5,
        max_tokens=100
    )
    
    assert len(tree_builder.active_agents_ids) == 1
    assert agent.execution_status == AgentExecutionStatus.STARTED
    assert agent.depth == 0

    # Complete the agent
    updated_agent = tree_builder.update_last_agent_node_with_success(
        llm_response=LLMMessage(role=MessageRole.ASSISTANT, content="done"),
        token_usage=TokenUsageData(prompt_tokens=1, completion_tokens=1, total_tokens=2, cost=0.1),
        output_action=FinishAgentAction(params=ExecutionParams(params={"result": "success"}))
    )

    assert len(tree_builder.active_agents_ids) == 0
    assert updated_agent.execution_status == AgentExecutionStatus.COMPLETED
    assert updated_agent.time_execution_data.end_time is not None

def test_agent_with_tool_lifecycle(tree_builder):
    # Create initial agent
    agent = tree_builder.create_agent_node(
        agent_name="MainAgent",
        input_data=AgentInputData(
            params=ExecutionParams(params={"task": "test"}),
            source=AgentInputDataSource.AGENT_CREATED_BY_USER
        ),
        messages=[],
        model_name="test-model",
        temperature=0.5,
        max_tokens=100
    )

    # Start tool
    tree_builder.update_last_agent_node_with_success(
        llm_response=LLMMessage(role=MessageRole.ASSISTANT, content="using tool"),
        token_usage=TokenUsageData(prompt_tokens=1, completion_tokens=1, total_tokens=2, cost=0.1),
        output_action=StartChildToolAction(
            child_tool_name="TestTool",
            params=ExecutionParams(params={"tool_task": "test"})
        )
    )

    tool = tree_builder.create_tool_node(
        tool_name="TestTool",
        input_data=ExecutionParams(params={"tool_task": "test"})
    )

    assert len(tree_builder.active_agents_ids) == 1
    assert tool.depth == 1
    assert tool.parent_agent_id == agent.id

    # Complete tool
    updated_tool = tree_builder.update_last_tool_node_with_success(
        output_data=ExecutionParams(params={"result": "success"}),
        output_metadata={"duration": "1s"}
    )

    assert updated_tool.execution_status == ToolExecutionStatus.COMPLETED

def test_nested_agents_lifecycle(tree_builder):
    # Create parent agent
    parent = tree_builder.create_agent_node(
        agent_name="ParentAgent",
        input_data=AgentInputData(
            params=ExecutionParams(params={"task": "parent"}),
            source=AgentInputDataSource.AGENT_CREATED_BY_USER
        ),
        messages=[],
        model_name="test-model",
        temperature=0.5,
        max_tokens=100
    )

    # Start child agent
    tree_builder.update_last_agent_node_with_success(
        llm_response=LLMMessage(role=MessageRole.ASSISTANT, content="starting child"),
        token_usage=TokenUsageData(prompt_tokens=1, completion_tokens=1, total_tokens=2, cost=0.1),
        output_action=StartChildAgentAction(
            child_agent_name="ChildAgent",
            params=ExecutionParams(params={"task": "child"})
        )
    )

    child = tree_builder.create_agent_node(
        agent_name="ChildAgent",
        input_data=AgentInputData(
            params=ExecutionParams(params={"task": "child"}),
            source=AgentInputDataSource.AGENT_CREATED_BY_AGENT
        ),
        messages=[],
        model_name="test-model",
        temperature=0.5,
        max_tokens=100
    )

    assert len(tree_builder.active_agents_ids) == 2
    assert child.depth == 1
    assert child.parent_agent_id == parent.id

    # Complete child agent
    tree_builder.update_last_agent_node_with_success(
        llm_response=LLMMessage(role=MessageRole.ASSISTANT, content="child done"),
        token_usage=TokenUsageData(prompt_tokens=1, completion_tokens=1, total_tokens=2, cost=0.1),
        output_action=FinishAgentAction(params=ExecutionParams(params={"result": "success"}))
    )

    assert len(tree_builder.active_agents_ids) == 1

def test_agent_error_handling(tree_builder):
    # Create agent
    tree_builder.create_agent_node(
        agent_name="MainAgent",
        input_data=AgentInputData(
            params=ExecutionParams(params={"task": "test"}),
            source=AgentInputDataSource.AGENT_CREATED_BY_USER
        ),
        messages=[],
        model_name="test-model",
        temperature=0.5,
        max_tokens=100
    )

    # Simulate error
    error = Exception("Test error")
    updated_agent = tree_builder.update_last_agent_node_with_error(error=error)

    assert len(tree_builder.active_agents_ids) == 0
    assert updated_agent.execution_status == AgentExecutionStatus.FAILED
    assert updated_agent.output_error == error
    assert updated_agent.time_execution_data.end_time is not None
