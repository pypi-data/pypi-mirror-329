from typing import Dict, Any
from stefan.settings import Settings
from stefan.execution_context import ExecutionContext
from stefan.tool.tool_definition import ToolDefinition
from stefan.utils.gspread.gspread_client import GspreadClient
from stefan.utils.multiline import multiline

class LocalizationToolDefinition(ToolDefinition):
    name: str = "localization_tool"
    description: str = multiline("""
        This tool manages translations in Google Sheets. It allows you to perform multiple operations
        on the translation sheet in a single run. The sheet structure has three columns:
        - Column A: Section (e.g., 'General', 'Navigation', etc.)
        - Column B: Translation key
        - Next columns: Translation values in different languages

        Available operations:
        1. GET_ALL - Retrieve all values from the sheet
           Example: 
           <get_all>
           </get_all>
        
        2. UPDATE_CELL - Update a single cell
           Example:
           <update_cell>
               <row>5</row>
               <column>C</column>
               <value>Text</value>
           </update_cell>
        
        3. INSERT_ROW - Insert a new row (values may be empty)
           Example:
           <insert_row>
                <row>3</row>
                <values></values>
                <values>Second column value</values>
                <values>Third column value</values>
           </insert_row>
        
        4. DELETE_ROW - Delete a row
           Example:
           <delete_row>
               <row>3</row>
           </delete_row>

        Notes:
        - Row numbers are 1-based (first row is 1)
        - Column letters are uppercase (A, B, C, etc.)
        - Operations return status messages in the results
        - For multiple sheets, the first sheet is used by default
        - The sheet is always saved after the operations are executed
        - Order of operations is important as the operations are executed in the order they are given
        - The sheet is case sensitive and supports localized characters (like é, á, ď, etc.)
        """)

    parameters: Dict[str, str] = {
        "commands": "(required) XML string containing commands to execute. Each command should be nested XML elements:\n"
            "- <get_all></get_all>\n"
            "- <update_cell><row>5</row><column>C</column><value>translation</value></update_cell>\n"
            "- <insert_row><row>3</row><values><value>Col1</value><value>Col2</value><value>Col3</value></values></insert_row>\n"
            "- <delete_row><row>3</row></delete_row>"
    }

    usage: str = multiline("""
        <localization_tool>
            <commands>
                <get_all>
                </get_all>
                <update_cell>
                    <row>5</row>
                    <column>C</column>
                    <value>Nový překlad</value>
                </update_cell>
                <insert_row>
                    <row>3</row>
                    <values>General</values>
                    <values>new_key</values>
                    <values>New translation</values>
                </insert_row>
                <delete_row>
                    <row>3</row>
                </delete_row>
            </commands>
        </localization_tool>
                           
        Multiple operations can be combined in a single command:
        <commands>
            <update_cell><row>5</row><column>C</column><value>Nový překlad 1</value></update_cell>
            <update_cell><row>6</row><column>C</column><value>Nový překlad 2</value></update_cell>
            <insert_row>
                <row>7</row>
                <values>General</values>
                <values>another_key</values>
                <values>Another translation</values>
            </insert_row>
        </commands>
        """)
    
    def execute_tool(
        self,
        args: Dict[str, Any],
        context: ExecutionContext,
        *,
        client: GspreadClient | None = None,
    ) -> str:
        if context.project_context.metadata.localization_sheet is None:
            return "Localization sheet is not set in project metadata - no way to change translations or strings"

        if client is None:
            sheet_url = context.project_context.metadata.localization_sheet.sheet_url
            settings = Settings()
            service_account_json = settings.google_service_account_json_dict
            client = GspreadClient(sheet_url, service_account_json)

        commands = args.get("commands", [])
        
        results = []
        for command in commands:
            cmd_type = command["type"]
            cmd_args = command["data"]
            
            if cmd_type == "get_all":
                sheet_data = client.show_all_data()
                results.append(("SHOW_ALL_DATA", f"Current sheet data:\n{sheet_data}"))
            
            elif cmd_type == "update_cell":
                row = int(cmd_args["row"])
                column = cmd_args["column"]
                value = cmd_args["value"]
                client.update_cell(row, column, value)
                results.append(("UPDATE_CELL", f"Updated cell {column}{row} with value: {value}"))
            
            elif cmd_type == "insert_row":
                row = int(cmd_args["row"])
                values = cmd_args["values"]
                client.insert_row(values, row)
                results.append(("INSERT_ROW", f"Inserted new row at position {row}"))
            
            elif cmd_type == "delete_row":
                row = int(cmd_args["row"])
                client.delete_row(row)
                results.append(("DELETE_ROW", f"Deleted row at position {row}"))
            
            else:
                results.append(("UNKNOWN_COMMAND", f"Unknown command: {cmd_type}"))

        return "\n".join([result[1] for result in results])
