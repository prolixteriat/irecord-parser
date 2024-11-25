'''
About  : Implements the RecordController class which orchestrates the data 
         input and parsing processes.
'''

# ------------------------------------------------------------------------------

import logging
import os

from configmgr import ConfigMgr
from recordparser import RecordParser
from utils import ElapsedTime

# ------------------------------------------------------------------------------

log: logging.Logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------

class RecordController:
    '''Class which orchestrates the data input, parsing and output processes.'''
    # --------------------------------------------------------------------------

    def __init__(self, fn_ini: str|None=None) -> None:
        '''Constructor.
        Args: 
            fn_ini (string) - filename of INI config file (None use default)
        Returns: 
            N/A
        '''
        self.config: ConfigMgr = ConfigMgr(fn_ini)
        logging.getLogger().setLevel(self.config.log_level)
        self.parser: RecordParser = RecordParser(self.config)

    # --------------------------------------------------------------------------

    def get_files(self, folder: str) -> list[str]:
        '''Get list of filenames in a target folder.
        Args: 
            folder (string) - path to folder containing files to parse
        Returns: 
            (list of strings) - filenames to be parsed
        '''
        log.info('Reading filenames in folder: %s', folder)
        files: list[str] = []
        for filename in os.listdir(folder):
            f = os.path.join(folder, filename)
            if os.path.isfile(f):
                files.append(f)

        return files

    # --------------------------------------------------------------------------

    def process(self) -> None:
        '''Process all files in the input folder.
        Args: 
            N/A
        Returns: 
            N/A
        '''
        et = ElapsedTime()
        files = self.get_files(self.config.dir_data_in)
        for ix, f in enumerate(files):
            log.info('-'*50)
            log.info('Processing file %i of %i', ix+1, len(files))
            self.parser.read_file(f)

        log.info('-'*50)
        log.info('Finished')
        et.log_elapsed_time()
        # Avoid any plots being automatically closed at end of script
        if self.config.plot is True:
            input('Press Enter key to continue...')

# ------------------------------------------------------------------------------

'''
End
'''
