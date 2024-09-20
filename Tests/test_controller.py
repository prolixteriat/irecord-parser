'''
About  : Tests the controller.py module.
'''
# ------------------------------------------------------------------------------

import os
import sys
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '../Code'))

from controller import RecordController

# ------------------------------------------------------------------------------

def test_processing():

    rc = RecordController('Config/debug.ini')
    try:
        rc.process()
        assert True
    except Exception as e:  # pylint: disable=broad-exception-caught
        assert pytest.fail(e)

# ------------------------------------------------------------------------------

'''
End
'''
