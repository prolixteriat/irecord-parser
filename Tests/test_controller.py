'''
About  : Tests the controller.py module.
'''
# ------------------------------------------------------------------------------

import os
import sys
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '../Code'))

from controller import RecordController
from utils_tests import compare_excel_sheets, INI_FILE

# ------------------------------------------------------------------------------

def test_processing():

    rc = RecordController(INI_FILE)
    file_1 = 'Tests/Data_Out/test_data.xlsx'
    file_2 = 'Tests/Data_Out/test_data_comparator.xlsx'

    try:
        rc.process()
        assert True
        assert compare_excel_sheets(file_1, file_2) is True

    except Exception as e:  # pylint: disable=broad-exception-caught
        print(e)
        assert pytest.fail(str(e))

# ------------------------------------------------------------------------------

'''
End
'''
