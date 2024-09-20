'''
About  : Tests the georegion.py module.
'''
# ------------------------------------------------------------------------------

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../Code'))

from configmgr import ConfigMgr
from georegion import GeoRegion

# ------------------------------------------------------------------------------

def test_point_in_poly():

    config = ConfigMgr('Config/debug.ini')

    geo = GeoRegion(config)
    gridrefs = [('SJ403661', True),
                ('SJ405664', True),
                ('SJ406667', True),
                ('SJ40696678', True),
                ('SJ414667', True),
                ('SJ415665', True),
                ('SJ41756640',True),
                ('SH874544', False),
                ('SH83764493', False),
                ('SP450440', False),
                ('SP36593729', False)]
    rv = True
    for gr in gridrefs:
        inside = geo.gridref_in_region(gr[0])
        ok = inside == gr[1]
        if not ok:
            rv = False
        print(f'Grid reference: {gr}  inside: {inside} correct: {ok}')

    i_i, i_o = geo.count()
    print(f'No. inside: {i_i}, No. outside: {i_o}')
    ## geo.plot('test')
    assert rv

# ------------------------------------------------------------------------------

'''
End
'''
