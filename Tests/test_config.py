'''
About  : Tests the config.py module.
'''
# ------------------------------------------------------------------------------

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../Code'))

from configmgr import ConfigMgr

# ------------------------------------------------------------------------------

def test_dir_is_present():

    config = ConfigMgr('Config/debug.ini')
    assert 'data_in' in config.dir_data_in.lower()

# ------------------------------------------------------------------------------

'''
End
'''
