'''
About  : Implements the Crosschecker class which provides loads external 
         reference files and provides lookup functionality.
'''

# ------------------------------------------------------------------------------

import logging
from typing import Set, TypedDict

import pandas as pd
import const
from georegion import GeoRegion
from configmgr import ConfigMgr
from utils import read_csv_robust

# ------------------------------------------------------------------------------

log: logging.Logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------

class UserIdentity(TypedDict):
    '''Helper class to manage user identity permissions.'''
    name: str
    permission: bool

# ------------------------------------------------------------------------------

class Crosschecker:
    '''Class which loads external reference files and provides lookup functionality.'''
    # --------------------------------------------------------------------------

    def __init__(self, config: ConfigMgr) -> None:
        '''Constructor.
        Args: 
            config (ConfigMgr) - object containing program configuration
        Returns: 
            N/A
        '''
        self.config: ConfigMgr = config
        self.georegion: GeoRegion = GeoRegion(config)
        self.abundance: dict[tuple[str, str], str] = {}
        self.excluded_taxons: dict[str, str] = {}
        self.permissions: dict[str, bool] = {}
        self.processed: Set[str] = set()
        self.sample_methods: dict[str, str] = {}
        self.user_identities: dict[str, UserIdentity] = {}
        self.load_files()

    # --------------------------------------------------------------------------

    def get_abundance(self, taxon_group: str, count: str) -> tuple[bool, str]:
        '''Map iRecord count to Swift abundance.
        Args:
            taxon_group (string) - iRecord taxon group
            count (string) - iRecord count
        Returns: 
            (tuple[bool,str]) - (True,mapped abundance type), else (False,'') if no match
        '''
        tuple_key = (taxon_group.strip().lower(), count.strip().lower())
        value = self.abundance[tuple_key] if tuple_key in self.abundance else ''
        if len(value) > 0:
            match = True
        elif len(count) == 1 and count.isalpha():
            match = True
            value = 'Present'
        else:
            match = False
        return (match, value)

    # --------------------------------------------------------------------------

    def get_record_type(self, sample_method: str, images: str) -> str|None:
        '''Map iRecord sample method to Swift record type.
        Args: 
            sample_method (string) - iRecord sample method
            images (string) - iRecord images
        Returns: 
            (string/None) - mapped record type, else None if no match
        '''
        # If there are images, assume it's a photograph or video
        images = images.strip()
        if len(images) > 0:
            return 'Photographed (or videoed)'

        sm = sample_method.strip().lower()
        if len(sm) == 0:
            rv = 'Field record'
        elif sm in self.sample_methods:
            rv = self.sample_methods[sm]
        elif sm == 'other method (add comment)':
            rv = None
        else:
            rv = None
            log.warning('Unknown sample method: %s', sample_method)

        return rv

    # --------------------------------------------------------------------------

    def get_user_identity(self, username: str) -> str:
        '''Check whether a user has provided permission to use their real name.
        Args: 
            username (string) - user name 
        Returns: 
            (string) - user identity if permission granted, else empty string
        "For some records a username may have been provided for the 
        recorder/determiner, please refer to the ‘Username Identities&Permission 
        tracker’ spreadsheet in DBO > Data > iRecord data > 
        Username Identities& Name Use Permission, to see if the 
        recorder/determiner has informed us of their iNaturalist/iRecord 
        username and have given us permission for us to use their name."
        '''
        rv = ''
        un = username.strip().lower()
        if un in self.user_identities:
            urec = self.user_identities[un]
            if urec['permission'] is True:
                rv = urec['name']

        return rv

    # --------------------------------------------------------------------------

    def is_excluded_taxon(self, taxon: str) -> bool:
        '''Return True if supplied insect taxon is not commonly referred to by 
        rank of 'family' (rather than, say, 'genus').
        Args: 
            taxon (string) - taxon
        Returns: 
            (bool) - True if is excluded taxon, else False
        '''
        rv = taxon.strip().lower() in self.excluded_taxons
        return rv

    # --------------------------------------------------------------------------

    def is_permission_granted(self, name: str) -> bool:
        '''Return True if a Recorder has explicitly granted permission to cite name.
        Args: 
            name (string) - Recorder identity
        Returns: 
            (bool) - True if recorder had explicitly granted permission
        "before removing records with these licences, please check the ‘iNat 
        Permissions Tracker’ spreadsheet, as some recorders have provided us 
        with permission to use their records despite their records having these 
        licences. The spreadsheet is in DBO > Data > iRecord data > iNat 
        Licensed Records Use Permission. ONLY REMOVE LICENCED RECORDS WHICH WE 
        DO NOT HAVE PERMISSIONS TO USE."
        '''
        name_lower = name.strip().lower()
        rv = self.permissions[name_lower] if name_lower in self.permissions else False
        return rv

    # --------------------------------------------------------------------------

    def is_processed(self, record_key: str) -> bool:
        '''Return True if supplied record key has already been processed.
        Args:
            key (string) - record key
        Returns:
            (bool) - True if record key has already been processed, else False
        '''
        rv = record_key.strip().lower() in self.processed
        return rv

    # --------------------------------------------------------------------------

    def load_files(self) -> None:
        '''Load and parse external reference files as defined in config object.
        Args: 
            N/A
        Returns: 
            N/A
        '''
        log.info('Loading crosscheck files')
        # Abundance mapping file -
        self.abundance.clear()
        if len(self.config.file_abundance) > 0:
            log.debug('Loading abundance file: %s', self.config.file_abundance)
            df = pd.read_excel(self.config.file_abundance)
            # Map dataframe to dictionary containing the columns of interest
            self.abundance = dict(
                ((str(s[0]).lower(),
                  str(s[1]).lower())
                  if isinstance(s[0], str) and isinstance(s[1], str) else s,
                  str(r).lower() if isinstance(r, str) else r)
                for s, r in zip(zip(df['Taxon Group'],
                                    df['Count of sex or stage']),
                                    df['Abundance']))
        # Excluded taxons file -
        self.excluded_taxons.clear()
        if len(self.config.file_exc_taxons) > 0:
            log.debug('Loading excluded taxons file: %s', self.config.file_exc_taxons)
            df = pd.read_excel(self.config.file_exc_taxons)
            # Map dataframe to dictionary containing the columns of interest
            self.excluded_taxons = dict((t.lower(), '') for t in df['Taxons'])
        # iNat permissions file -
        # define column headers
        p_name = 'Please enter your full name'
        p_permission = ('Are you happy for your full name to be used with your '
                        'records (in the ways described above)?')
        self.permissions.clear()
        if len(self.config.file_permissions) > 0:
            log.debug('Loading iNat permissions file: %s', self.config.file_permissions)
            df = pd.read_excel(self.config.file_permissions)
            # Map dataframe to dictionary containing the columns of interest
            self.permissions = dict((n.lower(), True if p.lower() == 'yes' else False)
                                for n, p in  zip(df[p_name], df[p_permission]))
        # Processed records file - use CSV to cope with potentially large no. records
        self.processed.clear()
        if len(self.config.file_processed) > 0:
            log.debug('Loading processed records file: %s', self.config.file_processed)
            df = read_csv_robust(self.config.file_processed)
            self.processed = set(df[const.I_RECORDKEY].dropna().astype(str)
                                .str.strip().str.lower())

        # Sample method / record type mapping file -
        self.sample_methods.clear()
        if len(self.config.file_rec_type) > 0:
            log.debug('Loading sample method/record type file: %s', self.config.file_rec_type)
            df = pd.read_excel(self.config.file_rec_type)
            # Map dataframe to dictionary containing the columns of interest
            self.sample_methods = dict((s.lower(), r) for s, r in
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
            log.debug('Loading user identities file: %s', self.config.file_users)
            df = pd.read_excel(self.config.file_users)
            # Map dataframe to dictionary containing the columns of interest
            self.user_identities = dict((u.lower(), {'name': n, 'permission':
                                        True if p.lower() == 'yes' else False})
                for u, n, p in zip(df[i_username], df[i_name], df[i_permission]))

# ------------------------------------------------------------------------------

'''
End
'''
