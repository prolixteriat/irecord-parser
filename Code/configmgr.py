'''
About  : Read contents of INI file containing runtime configuration.         
Uses   : https://docs.python.org/3/library/configparser.html
'''

# ------------------------------------------------------------------------------

import logging
import os

from configparser import ConfigParser
from typing import Final

import const

# ------------------------------------------------------------------------------

log: logging.Logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------

DEFAULT_FN_CONFIG: Final[str] = '../Config/config.ini'  # default config filename

# ------------------------------------------------------------------------------

class ConfigMgr:
    '''Class which loads runtime configuration from file.'''

    dir_data_in: str = None       # folder in which to find iRecords to be processed
    dir_data_out: str = None      # folder in which to find iRecords to be processed
    excel: bool = True            # produce Excel workbook results file
    file_abundance: str = ''      # path to abundance mapping file
    file_duplicates: str = ''     # path to duplicate records file
    file_exc_taxons: str = ''     # path to family-exluded insect taxons
    file_gis: str = ''            # path to GIS shape file
    file_permissions: str = ''    # path to iNaturalist permissions file
    file_rec_type: str = ''       # path to sample method / record type map file
    file_users: str = ''          # path to user identities & permissions file
    plot: bool = True             # plot region chart
    log_level: int = logging.INFO

    # --------------------------------------------------------------------------

    def __init__(self, fn_config: str=None) -> None:
        '''Constructor.
        Args: 
            fn_config (string) = config filename
        Returns: 
            N/A
        '''
        self.fn_config = fn_config or DEFAULT_FN_CONFIG
        self.config = ConfigParser()
        self.read_config()

    # --------------------------------------------------------------------------

    def check_files_exist(self) -> None:
        '''Confirm that files referenced in the config file do exist.
        Args: 
            N/A
        Returns:
            N/A
        Raises: 
            Raises OSError exception if a file does not exist.
        '''
        # ----------------------------------------------------------------------
        def check_file(fn: str, key: str) -> bool:
            if len(fn) == 0 or os.path.isfile(fn):
                rv = True
            else:
                rv= False
                log.error('Config key "%s" error: file does not exist "%s"', key, fn)
            return rv
        # ----------------------------------------------------------------------

        f1 = check_file(self.file_abundance, const.C_FILE_ABUNDANCE)
        f2 = check_file(self.file_duplicates, const.C_FILE_DUPLICATES)
        f3 = check_file(self.file_exc_taxons, const.C_FILE_EXC_TAXONS)
        f4 = check_file(self.file_gis, const.C_FILE_GIS)
        f5 = check_file(self.file_permissions, const.C_FILE_PERMS)
        f6 = check_file(self.file_rec_type, const.C_FILE_REC_TYPE)
        f7 = check_file(self.file_users, const.C_FILE_USERS)
        if not (f1 and f2 and f3 and f4 and f5 and f6 and f7):
            raise OSError('One or more config files do not exist')

    # --------------------------------------------------------------------------

    def read_config(self) -> None:
        '''Read contents of INI file.
        Args: 
            N/A
        Returns: 
            N/A
        Raises:
            OSError exception if config file does not exist.
        '''
        if not os.path.isfile(self.fn_config):
            raise OSError(f'Config file does not exist: {self.fn_config}')

        errmsg: str = 'Config file "%s" does not contain section "%s"'
        self.config.read(self.fn_config)
        # [Data]
        if const.C_DATA in self.config:
            s_data = self.config[const.C_DATA]
            self.dir_data_in = s_data.get(const.C_FOLDER_IN)
            self.dir_data_out = s_data.get(const.C_FOLDER_OUT)
        else:
            log.error(errmsg, self.fn_config, const.C_DATA)
        # [Files]
        if const.C_FILES in self.config:
            s_files = self.config[const.C_FILES]
            self.file_abundance = s_files.get(const.C_FILE_ABUNDANCE, '')
            self.file_duplicates = s_files.get(const.C_FILE_DUPLICATES, '')
            self.file_gis = s_files.get(const.C_FILE_GIS, '')
            self.file_permissions = s_files.get(const.C_FILE_PERMS, '')
            self.file_rec_type = s_files.get(const.C_FILE_REC_TYPE, '')
            self.file_users = s_files.get(const.C_FILE_USERS, '')
            self.file_exc_taxons = s_files.get(const.C_FILE_EXC_TAXONS, '')
            self.check_files_exist()
        else:
            log.error(errmsg, self.fn_config, const.C_FILES)
        # [Options]
        if const.C_OPTIONS in self.config:
            s_options = self.config[const.C_OPTIONS]
            self.plot = s_options.get(const.C_PLOT, 'True').lower() == 'true'
            self.excel = s_options.get(const.C_EXCEL, 'True').lower() == 'true'
        else:
            log.error(errmsg, self.fn_config, const.C_OPTIONS)
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
                log.error('Unknown log level: %s', ll)

# ------------------------------------------------------------------------------

'''
End
'''
