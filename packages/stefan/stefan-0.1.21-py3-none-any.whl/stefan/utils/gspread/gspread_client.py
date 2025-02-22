from typing import List

import gspread
from gspread.worksheet import Worksheet
from gspread.utils import GridRangeType

class GspreadClient:

    def __init__(self, sheet_url: str, service_account_json: dict):
        self.sheet_url = sheet_url
        self.service_account_json = service_account_json

    def show_all_data(self) -> str:
        worksheet = self._load_worksheet()

        # Get all rows and columns from the sheet
        list_of_lists = worksheet.get(return_type=GridRangeType.ListOfLists)
        print(f"Debug - Retrieved data type: {type(list_of_lists)}")
        print(f"Debug - Retrieved data: {list_of_lists}")
        
        # Handle empty sheet case
        if not list_of_lists or not list_of_lists[0]:
            return "Sheet is empty"
        
        # Add column letters as header row
        column_letters = [chr(65 + i) for i in range(len(list_of_lists[0]))]  # A, B, C, etc.
        list_of_lists.insert(0, column_letters)
        
        # Calculate maximum width for each column, including row numbers
        row_num_width = len(str(len(list_of_lists)))
        col_widths = []
        for col_idx in range(len(list_of_lists[0])):
            col_width = max(len(str(row[col_idx])) for row in list_of_lists if len(row) > col_idx)
            col_widths.append(col_width)
        
        # Create formatted output
        output = []
        for row_idx, row in enumerate(list_of_lists):
            # Add row number (empty for header row)
            row_num = '' if row_idx == 0 else str(row_idx)
            formatted_row = [row_num.rjust(row_num_width)]
            
            # Format each cell
            for col_idx, cell in enumerate(row):
                formatted_row.append(str(cell).ljust(col_widths[col_idx]))
            output.append(" | ".join(formatted_row))
        
        # Add separator line after column letters
        separator = "-" * len(output[0])
        output.insert(1, separator)
        
        return "\n".join(output)

    def update_cell(self, row: int, col: str, value: str) -> None:
        """
        Update a single cell value.
        Args:
            row: Row number (1-based)
            col: Column letter (A, B, C, etc.)
            value: New cell value
        """
        worksheet = self._load_worksheet()
        # Convert column letter to number (A=1, B=2, etc.)
        col_num = ord(col.upper()) - ord('A') + 1
        worksheet.update_cell(row, col_num, value)

    def insert_row(self, values: List[str], row_index: int) -> None:
        """
        Insert a new row at specified index and fill it with values.
        Args:
            values: List of values for the new row
            row_index: Row index where to insert (1-based)
        """
        worksheet = self._load_worksheet()
        worksheet.insert_row(values, row_index)

    def delete_row(self, row_index: int) -> None:
        """
        Delete a row at specified index.
        Args:
            row_index: Row index to delete (1-based)
        """
        worksheet = self._load_worksheet()
        worksheet.delete_rows(row_index)

    def _load_worksheet(self) -> Worksheet:
        gc = gspread.service_account_from_dict(self.service_account_json)
        # gc = gspread.service_account_from_dict(_SERVICE_ACCOUNT_MAP)
        spreadsheet = gc.open_by_url(self.sheet_url)
        worksheet = spreadsheet.sheet1
        return worksheet

    def _clear_and_update_worksheet(self, values: List[List[str]]) -> None:
        """
        Clears the entire worksheet and updates it with new values.

        Args:
            values: List of lists containing the new values to populate the worksheet with
        """
        worksheet = self._load_worksheet()
        # Clear existing content
        worksheet.clear()
        # Update with new values starting from A1
        worksheet.update(values)

class MockGspreadClient:
    def __init__(self):
        self.operations = []
        self._mock_data = [
            ["Section", "Key", "Value"],
            ["General", "key1", "value1"],
            ["Navigation", "key2", "value2"]
        ]

    def show_all_data(self) -> str:
        self.operations.append(("get_all", {}))
        return "\n".join(["\t".join(row) for row in self._mock_data])

    def update_cell(self, row: int, col: str, value: str) -> None:
        self.operations.append(("update_cell", {"row": row, "col": col, "value": value}))

    def insert_row(self, values: List[str], row_index: int) -> None:
        self.operations.append(("insert_row", {"values": values, "row_index": row_index}))

    def delete_row(self, row_index: int) -> None:
        self.operations.append(("delete_row", {"row_index": row_index}))
