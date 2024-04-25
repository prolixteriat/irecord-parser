'''
About  : Implements the iRecordController class which orchestrates the data 
         input and parsing processes.
Author : Kevin Morley
Version: 1 (21-Mar-2023)
'''

# ------------------------------------------------------------------------------

import logging
import os

from config import ConfigMgr                # KPM
from iRecordParser import iRecordParser     # KPM
from utils import ElapsedTime               # KPM

# ------------------------------------------------------------------------------

log = logging.getLogger(__name__)

# ------------------------------------------------------------------------------
# Class which orchestrates the data input, parsing and output processes.

class iRecordController:

    # --------------------------------------------------------------------------
    # Constructor.

    def __init__(self, fn_ini=None):
        '''
        Params: fn_ini (string) - filename of INI config file (None use default)
        Return: N/A
        '''
        self.config = ConfigMgr(fn_ini)
        logging.getLogger().setLevel(self.config.log_level)
        self.parser = iRecordParser(self.config)

    # --------------------------------------------------------------------------
    # Get list of filenames in a target folder.

    def get_files(self, folder):
        '''
        Params: folder (string) - path to folder containing files to parse
        Return: (list of strings) - filenames to be parsed
        '''
        log.info(f'Reading filenames in folder: {folder}')
        files = []
        for filename in os.listdir(folder):
            f = os.path.join(folder, filename)
            if os.path.isfile(f):
                files.append(f)

        return files

    # --------------------------------------------------------------------------
    # Process all files in the input folder.

    def process(self):
        '''
        Params: N/A
        Return: N/A
        '''
        et = ElapsedTime()
        files = self.get_files(self.config.dir_data_in)
        for ix, f in enumerate(files):
            log.info('-'*50)
            log.info(f'Processing file {ix+1} of {len(files)}')
            self.parser.read_file(f)

        log.info('-'*50)
        log.info('Finished')
        et.log_elapsed_time()
        # Avoid any plots being automatically closed at end of script
        if self.config.plot:
            input('Press Enter key to continue...')


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
    log.info('Beginning test [iRecordController.py]...')
    rc = iRecordController()
    rc.process()
    # TODO
    rv = True
    log.info(f'Finished test. Test passed: {rv}')
    return rv

# ------------------------------------------------------------------------------

if __name__ == '__main__':
    do_test()

# ------------------------------------------------------------------------------
       
'''
End
'''