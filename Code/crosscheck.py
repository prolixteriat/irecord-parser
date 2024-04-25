'''
About  : Implements the Crosschecker class which provides loads external 
         reference files and provides lookup functionality.
Author : Kevin Morley
Version: 1 (21-Mar-2023)
'''

# ------------------------------------------------------------------------------

import logging
import pandas as pd

from georegion import GeoRegion

# ------------------------------------------------------------------------------

log = logging.getLogger(__name__)

# ------------------------------------------------------------------------------
# Class which loads external reference files and provides lookup functionality.

class Crosschecker:

    # --------------------------------------------------------------------------
    # Constructor.

    def __init__(self, config):
        '''
        Params: config (ConfigMgr)
        Return: N/A
        '''
        self.config = config
        self.georegion = GeoRegion(config)
        self.duplicates = None      # TODO
        self.excluded_taxons = {}
        self.permissions = {}
        self.sample_methods = {}
        self.user_identities = {}
        self.load_files()

    # --------------------------------------------------------------------------
    # Map iRecord sample method to Swift record type.
    
    def get_record_type(self, sample_method):
        '''
        Params: sample_method (string) - iRecord sample method
        Return: (string/None) - mapped record type, else None if no match
        '''
        sm = sample_method.lower()
        if len(sm) == 0:
            rv = 'Field record'
        elif sm in self.sample_methods:
            rv = self.sample_methods[sm]
        elif sm == 'other method (add comment)':
            rv = None
        else:
            rv = None
            log.warning(f'Unknown sample method: {sample_method}')

        return rv
    
    # --------------------------------------------------------------------------
    # Check whether a username had provided permission to use real name.
    
    def get_user_identity(self, username):
        '''
        Params: username (string) - 
        Return: (string) - user identity if permission granted, else ''
        "For some records a username may have been provided for the 
        recorder/determiner, please refer to the ‘Username Identities&Permission 
        tracker’ spreadsheet in DBO > Data > iRecord data > 
        Username Identities& Name Use Permission, to see if the 
        recorder/determiner has informed us of their iNaturalist/iRecord 
        username and have given us permission for us to use their name."

        '''
        rv = ''
        if (username in self.user_identities and 
            self.user_identities[username]['permission'] == True):
                rv = self.user_identities['name']
        return rv

    # --------------------------------------------------------------------------
    # Return True if supplied insect taxon is not commonly referred to by rank 
    # of 'family' (rather than, say, 'genus')

    def is_excluded_taxon(self, taxon):
        '''
        Params: taxon (string) - 
        Return: (bool) - True if is excluded taxon, else False
        '''
        rv = taxon in self.excluded_taxons
        return rv

    # --------------------------------------------------------------------------
    # Return True if a Recorder has explicitly granted permission to cite name.

    def is_permission_granted(self, name):
        '''
        Params: name (string) - Recorder identity
        Return: (bool) - True if recorder had explicitly granted permission
        "before removing records with these licences, please check the ‘iNat 
        Permissions Tracker’ spreadsheet, as some recorders have provided us 
        with permission to use their records despite their records having these 
        licences. The spreadsheet is in DBO > Data > iRecord data > iNat 
        Licensed Records Use Permission. ONLY REMOVE LICENCED RECORDS WHICH WE 
        DO NOT HAVE PERMISSIONS TO USE."
        '''
        rv = self.permissions[name] if name in self.permissions else False
        return rv

    # --------------------------------------------------------------------------
    # Load and parse external reference files as defined in ConfigMgr object.

    def load_files(self):
        '''
        Params: N/A
        Return: N/A
        '''        
        log.info('Loading crosscheck files')
        # Excluded taxons file -
        self.excluded_taxons.clear()
        if len(self.config.file_exc_taxons) > 0:
            log.debug(f'Loading excluded taxons file: {self.config.file_exc_taxons}')
            df = pd.read_excel(self.config.file_exc_taxons)
            # Map dataframe to dictionary containing the columns of interest        
            self.excluded_taxons = dict((t, '') for t in df['Taxons'])
        # iNat permissions file - 
        # define column headers
        p_name = 'Please enter your full name'
        p_permission = ('Are you happy for your full name to be used with your '
                        'records (in the ways described above)?')
        self.permissions.clear()
        if len(self.config.file_permissions) > 0:
            log.debug(f'Loading iNat permissions file: {self.config.file_permissions}')
            df = pd.read_excel(self.config.file_permissions)
            # Map dataframe to dictionary containing the columns of interest        
            self.permissions = dict((n, True if p.lower() == 'yes' else False) 
                                for n, p in  zip(df[p_name], df[p_permission]))
        # Sample method / record type mapping file -
        self.sample_methods.clear()
        if len(self.config.file_rec_type) > 0:
            log.debug(f'Loading sample method/record type file: {self.config.file_rec_type}')
            df = pd.read_excel(self.config.file_rec_type)
            # Map dataframe to dictionary containing the columns of interest        
            self.sample_methods = dict((s, r) for s, r in 
                                    zip(df['Sample Method'], df['Record Type']))
        # User identities file - 
        # define column headers
        i_username = ("Please enter your iRecord/iNaturalist username. (If you "
                      "use multiple recording platforms, e.g., bird track and "
                      "iNaturalist, and use different usernames across these "
                      "platforms, then please complete...")
        i_name = 'Please enter your name'
        i_permission = ("I agree that RECORD LRC can use my full name for "
                        "records I submit to iRecord or iNaturalist and store "
                        "them in their database for the uses outlined in "
                        "RECORD's terms and conditions")
        self.user_identities.clear()
        if len(self.config.file_users) > 0:
            log.debug(f'Loading user identities file: {self.config.file_users}')
            df = pd.read_excel(self.config.file_users)
            # Map dataframe to dictionary containing the columns of interest        
            self.user_identities = dict((u, {'name': n, 'permission': 
                                        True if p.lower() == 'yes' else False}) 
                for u, n, p in zip(df[i_username], df[i_name], df[i_permission]))

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
    log.info(f'Beginning test [crosscheck.py]...')
    # TODO
    config = ConfigMgr()
    cc = Crosschecker(config)
    rv = cc.get_record_type('412 mustard sampling') == 'Mustard sampling'
    log.info(f'Finished test. Test passed: {rv}')
    return rv

# ------------------------------------------------------------------------------

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
            format='[%(module)s]-[%(funcName)s]-[%(levelname)s] - %(message)s')
    from config import ConfigMgr

    do_test()

# ------------------------------------------------------------------------------
       
'''
End
'''