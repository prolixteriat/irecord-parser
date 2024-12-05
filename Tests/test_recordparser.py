'''
About  : Tests the recordparser.py module.
'''
# ------------------------------------------------------------------------------

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../Code'))

from configmgr import ConfigMgr
from recordparser import RecordParser
from utils_tests import INI_FILE

# ------------------------------------------------------------------------------

def test_parse_record_file():

    config = ConfigMgr(INI_FILE)
    rp = RecordParser(config)
    fn = 'Tests/Data_In/test_data.csv'
    rv = rp.read_file(fn)
    assert rv is True

# ------------------------------------------------------------------------------

'''
End
'''
