import pytest

from stefan.execution_context import ExecutionContext
from stefan.tests.fixtures.dummy_project_context import create_dummy_project_context
from stefan.tool.tool_localization import LocalizationToolDefinition
from stefan.utils.gspread.gspread_client import MockGspreadClient
from stefan.utils.xml_answer_parser import XMLAnswerParser

@pytest.fixture
def mock_gspread_client():
    return MockGspreadClient()

@pytest.fixture
def localization_tool():
    return LocalizationToolDefinition()

@pytest.fixture
def execution_context():
    project_context = create_dummy_project_context()
    return ExecutionContext.test(project_context=project_context)

def test_get_all_command(localization_tool, execution_context, mock_gspread_client):
    # Create XML command for get_all
    args = XMLAnswerParser.parse_xml_without_answer_tag(
        xml="<commands><get_all></get_all></commands>",
        preserve_order=["commands"]
    )
    localization_tool.execute_tool(args.answer_dict, execution_context, client=mock_gspread_client)
    
    # Verify the operation was recorded
    assert mock_gspread_client.operations == [("get_all", {})]

def test_update_cell_command(localization_tool, execution_context, mock_gspread_client):
    # Create XML command for update_cell
    args = XMLAnswerParser.parse_xml_without_answer_tag(
        xml="""
            <commands>
                <update_cell>
                    <row>2</row>
                    <column>B</column>
                    <value>Test Value</value>
                </update_cell>
            </commands>
        """,
        preserve_order=["commands"]
    )
    result = localization_tool.execute_tool(args.answer_dict, execution_context, client=mock_gspread_client)
    
    # Verify the operation was recorded correctly
    assert mock_gspread_client.operations == [
        ("update_cell", {"row": 2, "col": "B", "value": "Test Value"})
    ]
    assert "Updated cell B2 with value: Test Value" in result

def test_insert_row_command(localization_tool, execution_context, mock_gspread_client):
    args = XMLAnswerParser.parse_xml_without_answer_tag(
        xml="""
            <commands>
                <insert_row>
                    <row>2</row>
                    <values>Test Section</values>
                    <values>test_key</values>
                    <values>Test Translation</values>
                </insert_row>
            </commands>
        """,
        preserve_order=["commands"]
    )
    result = localization_tool.execute_tool(args.answer_dict, execution_context, client=mock_gspread_client)
    
    # Verify the operation was recorded correctly
    assert mock_gspread_client.operations == [
        ("insert_row", {"values": ["Test Section", "test_key", "Test Translation"], "row_index": 2})
    ]
    assert "Inserted new row at position 2" in result

def test_delete_row_command(localization_tool, execution_context, mock_gspread_client):
    # Create XML command for delete_row
    args = XMLAnswerParser.parse_xml_without_answer_tag(
        xml="""
            <commands>
                <delete_row>
                    <row>2</row>
                </delete_row>
            </commands>
        """,
        preserve_order=["commands"]
    )
    result = localization_tool.execute_tool(args.answer_dict, execution_context, client=mock_gspread_client)
    
    # Verify the operation was recorded correctly
    assert mock_gspread_client.operations == [
        ("delete_row", {"row_index": 2})
    ]
    assert "Deleted row at position 2" in result

def test_invalid_command(localization_tool, execution_context, mock_gspread_client):
    # Test with an invalid command
    args = XMLAnswerParser.parse_xml_without_answer_tag(
        xml="<commands><invalid_command></invalid_command></commands>",
        preserve_order=["commands"]
    )
    result = localization_tool.execute_tool(args.answer_dict, execution_context, client=mock_gspread_client)
    
    # Verify no operations were recorded
    assert mock_gspread_client.operations == []
    assert "Unknown command: invalid_command" in result

def test_multiple_commands(localization_tool, execution_context, mock_gspread_client):
    # Create XML with multiple commands
    args = XMLAnswerParser.parse_xml_without_answer_tag(
        xml="""
            <commands>
                <update_cell>
                    <row>2</row>
                    <column>B</column>
                    <value>First Update</value>
                </update_cell>
                <insert_row>
                    <row>3</row>
                    <values>New Section</values>
                    <values>new_key</values>
                    <values>New Translation</values>
                </insert_row>
                <get_all></get_all>
            </commands>
        """,
        preserve_order=["commands"]
    )
    result = localization_tool.execute_tool(args.answer_dict, execution_context, client=mock_gspread_client)
    
    # Verify operations were executed in the correct order
    expected_operations = [
        ("update_cell", {"row": 2, "col": "B", "value": "First Update"}),
        ("insert_row", {"values": ["New Section", "new_key", "New Translation"], "row_index": 3}),
        ("get_all", {})
    ]
    assert mock_gspread_client.operations == expected_operations
    assert "Updated cell B2 with value: First Update" in result
    assert "Inserted new row at position 3" in result

def test_command_execution_order(localization_tool, execution_context, mock_gspread_client):
    # Test that commands are executed in the order they appear in XML
    args = XMLAnswerParser.parse_xml_without_answer_tag(
        xml="""
            <commands>
                <insert_row>
                    <row>2</row>
                    <values>First Row</values>
                    <values>Key1</values>
                    <values>Value1</values>
                </insert_row>
                <update_cell>
                    <row>2</row>
                    <column>C</column>
                    <value>Updated Value</value>
                </update_cell>
                <delete_row>
                    <row>2</row>
                </delete_row>
            </commands>
        """,
        preserve_order=["commands"]
    )
    result = localization_tool.execute_tool(args.answer_dict, execution_context, client=mock_gspread_client)
    
    # Verify operations were executed in the correct order
    expected_operations = [
        ("insert_row", {"values": ["First Row", "Key1", "Value1"], "row_index": 2}),
        ("update_cell", {"row": 2, "col": "C", "value": "Updated Value"}),
        ("delete_row", {"row_index": 2})
    ]
    
    assert mock_gspread_client.operations == expected_operations
    assert "Inserted new row at position 2" in result
    assert "Updated cell C2 with value: Updated Value" in result
    assert "Deleted row at position 2" in result

def test_multiple_same_commands_order(localization_tool, execution_context, mock_gspread_client):
    # Test that multiple instances of the same command are executed in order
    arguments = XMLAnswerParser.parse_xml_without_answer_tag(
        xml="""
            <commands>
                <update_cell>
                    <row>2</row>
                    <column>B</column>
                    <value>First Update</value>
                </update_cell>
                <update_cell>
                    <row>2</row>
                    <column>B</column>
                    <value>Second Update</value>
                </update_cell>
                <get_all>
                </get_all>
                <update_cell>
                    <row>2</row>
                    <column>B</column>
                    <value>Final Update</value>
                </update_cell>
            </commands>
        """,
        preserve_order=["commands"],
    )

    result = localization_tool.execute_tool(arguments.answer_dict, execution_context, client=mock_gspread_client)
    
    # Verify operations were executed in the correct order
    expected_operations = [
        ("update_cell", {"row": 2, "col": "B", "value": "First Update"}),
        ("update_cell", {"row": 2, "col": "B", "value": "Second Update"}),
        ("get_all", {}),
        ("update_cell", {"row": 2, "col": "B", "value": "Final Update"}),
    ]
    
    assert mock_gspread_client.operations == expected_operations
    assert "Updated cell B2 with value: First Update" in result
    assert "Updated cell B2 with value: Second Update" in result
    assert "Updated cell B2 with value: Final Update" in result
