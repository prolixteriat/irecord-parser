'''
About  : Read contents of INI file containing runtime configuration.         
Author : Kevin Morley
Version: 1 (21-Mar-2023)
Uses   :
    https://docs.python.org/3/library/configparser.html
'''

# ------------------------------------------------------------------------------

import const                    # KPM
import logging
import os

from configparser import ConfigParser

# ------------------------------------------------------------------------------

log = logging.getLogger(__name__)

# ------------------------------------------------------------------------------

DEFAULT_FN_CONFIG = 'Config/config.ini'  # default config filename

# ------------------------------------------------------------------------------
# Class which loads runtime configuration from file.

class ConfigMgr:

    dir_data_in = None       # folder in which to find iRecords to be processed
    dir_data_out = None      # folder in which to find iRecords to be processed
    excel = True             # produce Excel workbook results file
    file_duplicates = ''     # path to duplicate records file
    file_exc_taxons = ''     # path to family-exluded insect taxons
    file_gis = ''            # path to GIS shape file
    file_permissions = ''    # path to iNaturalist permissions file
    file_rec_type = ''       # path to sampel method / record type map file
    file_users = ''          # path to user identities & permissions file
    plot = True              # plot region chart
    log_level = logging.INFO

    # --------------------------------------------------------------------------
    # Constructor.

    def __init__(self, fn_config=None):
        '''
        Params: fn_config (string) = config filename
        Return: N/A
        '''
        self.fn_config = fn_config or DEFAULT_FN_CONFIG
        self.config = ConfigParser()
        self.read_config()
    
    # --------------------------------------------------------------------------
    # Confirm that files referenced in the config file do exist.

    def check_files_exist(self):
        '''
        Params: N/A
        Return: raises OSError exception if a file does not exist.
        '''
        # ----------------------------------------------------------------------
        def check_file(fn, key):
            if len(fn) == 0 or os.path.isfile(fn):
                rv = True
            else:
                rv= False
                log.error(f'Config key "{key}" error: file does not exist "{fn}"')
            return rv
        # ----------------------------------------------------------------------
       
        f1 = check_file(self.file_duplicates, const.C_FILE_DUPLICATES)
        f2 = check_file(self.file_exc_taxons, const.C_FILE_EXC_TAXONS)
        f3 = check_file(self.file_gis, const.C_FILE_GIS)
        f4 = check_file(self.file_permissions, const.C_FILE_PERMS)
        f5 = check_file(self.file_rec_type, const.C_FILE_REC_TYPE)
        f6 = check_file(self.file_users, const.C_FILE_USERS)
        if not (f1 and f2 and f3 and f4 and f5 and f6): 
            raise OSError('One or more config files do not exist')
                    
    # --------------------------------------------------------------------------
    # Read contents of INI file.

    def read_config(self):
        '''
        Params: N/A
        Return: N/A
        '''
        if not os.path.isfile(self.fn_config):
            raise OSError(f'Config file does not exist: {self.fn_config}')
        
        self.config.read(self.fn_config)
        # [Data]
        if const.C_DATA in self.config:
            s_data = self.config[const.C_DATA]
            self.dir_data_in = s_data.get(const.C_FOLDER_IN)
            self.dir_data_out = s_data.get(const.C_FOLDER_OUT)
        else:
            log.error(f'Config file "{self.fn_config} does not contain '
                      f'section "{const.C_DATA}"')
        # [Files]
        if const.C_FILES in self.config:
            s_files = self.config[const.C_FILES]
            self.file_duplicates = s_files.get(const.C_FILE_DUPLICATES, '')
            self.file_gis = s_files.get(const.C_FILE_GIS, '')
            self.file_permissions = s_files.get(const.C_FILE_PERMS, '')
            self.file_rec_type = s_files.get(const.C_FILE_REC_TYPE, '')
            self.file_users = s_files.get(const.C_FILE_USERS, '')
            self.file_exc_taxons = s_files.get(const.C_FILE_EXC_TAXONS, '')
            self.check_files_exist()
        else:
            log.warning(f'Config file "{self.fn_config} does not contain '
                      f'section "{const.C_FILES}"')
        # [Options]
        if const.C_OPTIONS in self.config:
            s_options = self.config[const.C_OPTIONS]
            self.plot = s_options.get(const.C_PLOT, 'True').lower() == 'true'
            self.excel = s_options.get(const.C_EXCEL, 'True').lower() == 'true'
        else:
            log.info(f'Config file "{self.fn_config} does not contain '
                      f'section "{const.C_DATA}"')
        # [Logging]
        if const.C_LOGGING in self.config:
            s_logging = self.config[const.C_LOGGING]
            ll = s_logging.get(const.C_LOGLEVEL, 'INFO').upper()
            if ll == 'NOTSET':
                self.log_level = logging.NOTSET
            if ll == 'DEBUG':
                self.log_level = logging.DEBUG
            elif ll == 'INFO':
                self.log_level = logging.INFO
            elif ll == 'WARNING':
                self.log_level = logging.WARNING
            elif ll == 'ERROR':
                self.log_level = logging.ERROR
            elif ll == 'CRITICAL':
                self.log_level = logging.CRITICAL
            else:
                log.error(f'Unknown log level: {ll}')

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
    log.info('Beginning test [config.py]...')
    config = ConfigMgr()
    rv = config.dir_data_in == 'Data_In/'
    log.info(f'Finished test. Test passed: {rv}')
    return rv

# ------------------------------------------------------------------------------

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
            format='[%(module)s]-[%(funcName)s]-[%(levelname)s] - %(message)s')
    
    do_test()

# ------------------------------------------------------------------------------
       
'''
End
'''