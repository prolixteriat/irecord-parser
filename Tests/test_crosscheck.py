'''
About  : Tests the crosscheck.py module.
'''

# ------------------------------------------------------------------------------

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../Code'))

from configmgr import ConfigMgr
from crosscheck import Crosschecker
from utils_tests import INI_FILE

# ------------------------------------------------------------------------------

def test_record_type_mapping():

    config = ConfigMgr(INI_FILE)
    cc = Crosschecker(config)
    rv = cc.get_record_type('412 mustard sampling', '') == 'Mustard sampling'

    assert rv

# ------------------------------------------------------------------------------

def test_abundance_mapping():

    config = ConfigMgr(INI_FILE)
    cc = Crosschecker(config)
    (match, value) = cc.get_abundance('insect - butterfly', 'D')

    assert match and value == '30 to 99'

# ------------------------------------------------------------------------------

'''
End
'''
