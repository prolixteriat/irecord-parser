'''
About  : Utility functions for tests.
'''
# ------------------------------------------------------------------------------

from typing import Final

import pandas as pd

# ------------------------------------------------------------------------------

INI_FILE: Final[str] = 'Tests/Config/test_config.ini'

# ------------------------------------------------------------------------------

def compare_excel_sheets(file1: str, file2: str, sheet_name: str|None=None) -> bool:
    '''Compares two Excel spreadsheets to ensure they are identical.
    Args: 
        file1 (string) - path to first Excel file
        file2 (string) - path to second Excel file
        sheet_name (string) - sheet name to compare (default: None compares all sheets)
    Returns: 
        (bool) - True if identical, else False    
    '''
    rv: bool = True
    try:
        # Load the Excel files
        xl1 = pd.ExcelFile(file1)
        xl2 = pd.ExcelFile(file2)

        # Get sheet names if sheet_name is not provided
        sheets1 = xl1.sheet_names if sheet_name is None else [sheet_name]
        sheets2 = xl2.sheet_names if sheet_name is None else [sheet_name]

        # Check if sheet names match
        if sheets1 != sheets2:
            print(f'\nSheet names differ: "{sheets1}" vs "{sheets2}"')
            return False

        # Compare each sheet
        for sheet in sheets1:
            df1 = xl1.parse(sheet)
            df2 = xl2.parse(sheet)

            # Check if DataFrames are equal
            if df1.equals(df2) is False:
                rv = False
                print(f'\nDiscrepancies found in sheet: {sheet}')
                # Find the differences
                diff = pd.concat([df1, df2]).drop_duplicates(keep=False)
                print('Differences:\n', diff)
    except Exception as e:  # pylint: disable=broad-exception-caught
        rv = False
        print('Error occurred:', e)

    return rv

# ------------------------------------------------------------------------------

'''
End
'''
