'''
About  : Tests the crosscheck.py module.
'''

# ------------------------------------------------------------------------------

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../Code'))

from configmgr import ConfigMgr
from crosscheck import Crosschecker

# ------------------------------------------------------------------------------

def test_record_type_mapping():

    config = ConfigMgr('Config/debug.ini')
    cc = Crosschecker(config)
    rv = cc.get_record_type('412 mustard sampling') == 'Mustard sampling'

    assert rv

# ------------------------------------------------------------------------------

def test_abundance_mapping():

    config = ConfigMgr('Config/debug.ini')
    cc = Crosschecker(config)
    rv = cc.get_abundance('insect - butterfly', 'D') == '30 to 99'

    assert rv

# ------------------------------------------------------------------------------

'''
End
'''
