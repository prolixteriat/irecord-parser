'''
About  : Implements the GeoRegion class which identifies in-scope records based
         upon whether they lie within the target geographic region.
Author : Kevin Morley
Version: 1 (21-Mar-2023)
'''

# ------------------------------------------------------------------------------

import bng
import logging
import geopandas as gpd
import matplotlib.pyplot as plt
import os

from config import ConfigMgr            # KPM
from shapely.geometry import Polygon

# ------------------------------------------------------------------------------

log = logging.getLogger(__name__)

# ------------------------------------------------------------------------------
# Class which performs point-in-polygon operation to identify those records
# within the target geographic region.

class GeoRegion:

    COORDS = 'coords'

    # --------------------------------------------------------------------------
    # Constructor.

    def __init__(self, config):
        '''
        Params: config (ConfigMgr) - instance of class containing INI file
        Return: N/A
        '''
        self.config = config        # instance of ConfigMgr class
        self.gdf_region = None      # GeoDataFrame for region
        self.gs_region = None       # GeoSeries for region
        self.gs_inside = []         # list of GeoSeries objects inside region
        self.gs_outside = []        # list of GeoSeries objects outside region
        self.load_shape()
        self.reset()
            
    # --------------------------------------------------------------------------
    # Return the number of members of the gs_inside and gs_outside lists.

    def count(self):
        '''
        Params: N/A
        Return: (tuple: int/int) - count of members of inside/outside lists
        '''
        return len(self.gs_inside), len(self.gs_outside)
    
    # --------------------------------------------------------------------------
    # Determine whether a given gridref is inside the region.

    def gridref_in_region(self, gridref):
        '''
        Params: gridref (string) - grid reference
        Return: (bool) - True if gridref within region
        '''        
        poly = self.gridref_to_polygon(gridref)
        if poly is not None:
            gs_gridref = gpd.GeoSeries([poly], crs=self.gdf_region.crs)
            i = self.gs_region.intersects(gs_gridref)
            rv = i[0]
            # Add Polygon to relevant list for future use
            if rv == True:
                self.gs_inside.append(gs_gridref)
            else:
                self.gs_outside.append(gs_gridref)
        else:
            # return True to avoid double-counting as 'gridref' filter will apply
            rv = True

        return rv            

    # --------------------------------------------------------------------------
    # Convert a supplied grid reference to a Polygon (eastings/northings)

    def gridref_to_polygon(self, gridref):
        '''
        Params: gridref (string) - grid reference
        Return: (Polygon) - equivalent Polygon object
        '''
        try:
            e_l, n_l = bng.to_osgb36(gridref)
            l = len(gridref)
            if l == 4:
                s = 10000
            elif l == 6:
                s = 1000
            elif l == 8:
                s = 100
            elif l == 10:
                s = 10
            else:
                s = 100
                log.error(f'Unable to convert grid reference: {gridref}')

            e_u = e_l + s
            n_u = n_l + s

            p = Polygon([(e_l, n_l), 
                        (e_l, n_u), 
                        (e_u, n_u), 
                        (e_u, n_l)])
        except bng.BNGError as ex:
            # Invalid format gridref, including too short - e.g. 'SJ78'
            log.debug(f'Unable to convert gridref: {gridref}')
            p = None

        return p

    # --------------------------------------------------------------------------
    # Load the GIS shape file.

    def load_shape(self):
        '''
        Params: N/A
        Return: N/A
        '''
        fn = self.config.file_gis
        log.debug(f'Loading GIS file: {fn}')
        self.gdf_region = gpd.read_file(fn)
        self.gs_region = self.gdf_region['geometry']

    # --------------------------------------------------------------------------
    # Plot map showing region and polygons inside/outside the region.

    def plot(self, filename):
        '''
        Params: filename (string) - filename associated with data
        Return: N/A
        '''

        # Only plot if config flag is set to True
        if self.config.plot == False:
            return
        log.info('Generating plot')
        # Region
        base = self.gdf_region.plot(linewidth=1, edgecolor='black', 
                                    facecolor='white', legend=True)
        '''
        # Takes a long time, so comment-out unless required...
        # Inside region            
        for gs in self.gs_inside:
            gs.plot(ax=base, edgecolor='red')
        '''
        # Outside region
        for gs in self.gs_outside:
            gs.plot(ax=base, edgecolor='blue')

        title = (f'VC58 - External Gridref Count: {len(self.gs_outside)} '
                 f'(>= 4 digits)\nFile: {os.path.basename(filename)}')
        plt.title(title)
        plt.tight_layout()
        plt.ion()   # interactive on - non-blocking      
        plt.show()

    # --------------------------------------------------------------------------
    # Initialise
    
    def reset(self):
        '''
        Params: N/A
        Return: N/A
        '''
        self.gs_inside.clear()
        self.gs_outside.clear()


# ------------------------------------------------------------------------------
# Test
# ------------------------------------------------------------------------------
# Run module-specific tests.

def do_test():
    '''
    Params: N/A
    Return: (bool) Returns True if tests succesful, else False
    '''
    
    log.info('-'*50)
    log.info('Beginning test [georegion.py]...')
    config = ConfigMgr()    
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
        log.info(f'Grid reference: {gr}  inside: {inside}  correct: {ok}')  

    i_i, i_o = geo.count()
    log.info(f' No. inside: {i_i}, No. outside: {i_o}')
    geo.plot()
    log.info(f'Finished test. Test passed: {rv}')    
    # input('Press Enter key to continue...')  
    return rv

# ------------------------------------------------------------------------------

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
            format='[%(module)s]-[%(funcName)s]-[%(levelname)s] - %(message)s')
        
    do_test()

# ------------------------------------------------------------------------------
       
'''
End
'''