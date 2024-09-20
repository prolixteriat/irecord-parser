'''
About  : Tests the recordparser.py module.
'''
# ------------------------------------------------------------------------------

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../Code'))

from configmgr import ConfigMgr
from recordparser import RecordParser

# ------------------------------------------------------------------------------

def test_parse_record_file():

    config = ConfigMgr('Config/debug.ini')
    rp = RecordParser(config)
    fn = 'Data_In/iRecord Data 09-01-2020 - 31-01-2020_original.csv'
    rv = rp.read_file(fn)
    assert rv is True

# ------------------------------------------------------------------------------

'''
End
'''
