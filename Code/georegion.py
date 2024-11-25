'''
About  : Implements the GeoRegion class which identifies in-scope records based
         upon whether they lie within the target geographic region.
'''

# ------------------------------------------------------------------------------

import logging
import os
from typing import Final
import bng
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

from configmgr import ConfigMgr

# ------------------------------------------------------------------------------

log: logging.Logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------

class GeoRegion:
    '''Class which performs point-in-polygon operation to identify those records
       within the target geographic region.'''

    COORDS: Final[str] = 'coords'

    # --------------------------------------------------------------------------

    def __init__(self, config: ConfigMgr) -> None:
        '''Constructor.
        Args: 
            config (ConfigMgr) - instance of class containing INI file
        Returns: 
            N/A
        '''
        self.config: ConfigMgr = config                # instance of ConfigMgr class
        self.gdf_region: gpd.GeoDataFrame|None = None  # GeoDataFrame for region
        self.gs_region : gpd.GeoSeries|None = None     # GeoSeries for region
        self.gs_inside: list[gpd.GeoSeries] = []   # list of objects inside region
        self.gs_outside: list[gpd.GeoSeries] = []  # list of objects outside region
        self.load_shape()
        self.reset()

    # --------------------------------------------------------------------------

    def count(self) -> tuple[int, int]:
        '''Return the number of members of the gs_inside and gs_outside lists.
        Args: 
            N/A
        Returns: 
            (tuple: int/int) - count of members of inside/outside lists
        '''
        return len(self.gs_inside), len(self.gs_outside)

    # --------------------------------------------------------------------------

    def gridref_in_region(self, gridref: str) -> bool:
        '''Determine whether a given gridref is inside the region.
        Args: 
            gridref (string) - grid reference
        Returns: 
            (bool) - True if gridref within region
        '''
        poly = self.gridref_to_polygon(gridref)
        if poly is not None and self.gs_region is not None:
            gs_gridref = gpd.GeoSeries([poly], crs=self.gdf_region.crs) # type: ignore
            intersects = self.gs_region.intersects(gs_gridref)
            rv = intersects.any()
            # Add GeoSeries to relevant list for future use
            if rv:
                self.gs_inside.append(gs_gridref)
            else:
                self.gs_outside.append(gs_gridref)
        else:
            # return True to avoid double-counting as 'gridref' filter will apply
            rv = True

        return rv

    # --------------------------------------------------------------------------

    def gridref_to_polygon(self, gridref: str) -> Polygon|None:
        '''Convert a supplied grid reference to a Polygon (eastings/northings).
        Args: 
            gridref (string) - grid reference
        Returns: 
            (Polygon) - equivalent Polygon object
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
                log.error('Unable to convert grid reference: %s', gridref)

            e_u = e_l + s
            n_u = n_l + s

            p = Polygon([(e_l, n_l),
                        (e_l, n_u),
                        (e_u, n_u),
                        (e_u, n_l)])
        except bng.BNGError as ex:
            # Invalid format gridref, including too short - e.g. 'SJ78'
            log.debug('Unable to convert gridref: %s', gridref)
            log.debug(ex)
            p = None

        return p

    # --------------------------------------------------------------------------

    def load_shape(self):
        '''Load the GIS shape file.
        Args: 
            N/A
        Returns: 
            N/A
        '''
        fn = self.config.file_gis
        log.debug('Loading GIS file: %s', fn)
        self.gdf_region = gpd.read_file(fn)
        if self.gdf_region is not None:
            self.gs_region = self.gdf_region['geometry'] # type: ignore

    # --------------------------------------------------------------------------

    def plot(self, filename: str) -> None:
        '''Plot map showing region and polygons inside/outside the region.
        Args: 
            filename (string) - filename associated with data
        Returns: 
            N/A
        '''
        # Only plot if config flag is set to True
        if self.config.plot is False:
            return
        log.info('Generating plot')
        # Region
        if self.gdf_region is None:
            log.info('No region to plot')
            return
        base = self.gdf_region.plot(linewidth=1, edgecolor='black',
                                    facecolor='white', legend=True)
        # Inside region
        '''
        # Takes a long time valid points, so comment-out unless required...
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

    def reset(self):
        '''Initialise.
        Args: 
            N/A
        Returns: 
            N/A
        '''
        self.gs_inside.clear()
        self.gs_outside.clear()

# ------------------------------------------------------------------------------

'''
End
'''
