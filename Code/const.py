'''
About  : Define constants.
Author : Kevin Morley
Version: 1 (21-Mar-2023)
'''

import logging

# ------------------------------------------------------------------------------

log = logging.getLogger(__name__)

# ------------------------------------------------------------------------------
# Config file section headings and fiedl names
C_DATA = 'Data'
C_FOLDER_IN = 'Folder_Input'
C_FOLDER_OUT = 'Folder_Output'
C_FILES = 'Files'
C_FILE_DUPLICATES = 'File_Duplicates'
C_FILE_GIS = 'File_GIS'
C_FILE_EXC_TAXONS = 'File_ExcludedTaxons'
C_FILE_PERMS = 'File_iNatPermissions'
C_FILE_REC_TYPE = 'File_RecordType'
C_FILE_USERS = 'File_UserIdenties'
C_LOGGING = 'Logging'
C_LOGLEVEL = 'LogLevel'
C_OPTIONS = 'Options'
C_PLOT = 'Plot'
C_EXCEL = 'Excel'

# ------------------------------------------------------------------------------
# Swift species import file column headers.
B_TAXONKEY = 'preferred_taxon_key'
B_TAXONVERSION = 'taxon_version_key'
B_PARENTTAXON = 'parent_taxon_key'
B_COUNT = 'sum_records_count'
B_PRECISION = 'public_precision'
B_CONCATNAMES = 'concat_mixed_names'
B_CONCATABBREVS = 'concat_abbreviations'
B_TAXONGROUP = 'taxon_group'
B_COMMON = 'preferred_common_name'
B_SCIENTIFIC = 'preferred_scientific_name'
B_TAXONRANK = 'taxon_rank'
B_HIERARCHY = 'hierarchy'
B_VERIFICATION = 'verification_config'
B_DATE = 'date_updated'

# ------------------------------------------------------------------------------
# iRecord import file column headers
I_ID = 'ID'
I_RECORDKEY = 'RecordKey'
I_EXTERNAL_KEY = 'External key'
I_SOURCE = 'Source'
I_RANK = 'Rank'
I_TAXON = 'Taxon'
I_COMMON_NAME = 'Common name'
I_TAXON_GROUP = 'Taxon group'
I_KINGDOM = 'Kingdom'
I_ORDER = 'Order'
I_FAMILY = 'Family'
I_TAXONVERSIONKEY = 'TaxonVersionKey'
I_SITE_NAME = 'Site name'
I_ORIGINAL_MAP_REF = 'Original map ref'
I_LATITUDE = 'Latitude'
I_LONGITUDE = 'Longitude'
I_PROJECTION_INPUT = 'Projection (input)'
I_PRECISION = 'Precision'
I_OUTPUT_MAP_REF = 'Output map ref'
I_PROJECTION_OUTPUT = 'Projection (output)'
I_BIOTOPE = 'Biotope'
I_VC_NUMBER = 'VC number'
I_VICE_COUNTY = 'Vice County'
I_DATE_INTERPRETED = 'Date interpreted'
I_DATE_FROM = 'Date from'
I_DATE_TO = 'Date to'
I_DATE_TYPE = 'Date type'
I_SAMPLE_METHOD = 'Sample method'
I_RECORDER = 'Recorder'
I_DETERMINER = 'Determiner'
I_RECORDER_CERTAINTY = 'Recorder certainty'
I_SEX = 'Sex'
I_STAGE = 'Stage'
I_COUNT_OF_SEX_OR_STAGE = 'Count of sex or stage'
I_ZERO_ABUNDANCE = 'Zero abundance'
I_COMMENT = 'Comment'
I_SAMPLE_COMMENT = 'Sample comment'
I_IMAGES = 'Images'
I_INPUT_ON_DATE = 'Input on date'
I_LAST_EDITED_ON_DATE = 'Last edited on date'
I_VERIFICATION_STATUS_1 = 'Verification status 1'
I_VERIFICATION_STATUS_2 = 'Verification status 2'
I_QUERY = 'Query'
I_VERIFIER = 'Verifier'
I_VERIFIED_ON = 'Verified on'
I_LICENCE = 'Licence'
I_AUTOMATED_CHECKS = 'Automated checks'
# Additional key to allow cross-referencing between files
I_KEY = 'Key'
I_IMPORTTYPE = 'Status type'
I_IMPORTNOTE = 'Status note'
I_IMPORTCOMMENT = 'Import comment'
I_RECORDREGION = 'In RECORD region'

I_COLUMNS = [
    I_KEY,
    I_ID,
    I_RECORDKEY,
    I_EXTERNAL_KEY,
    I_SOURCE,
    I_RANK,
    I_TAXON,
    I_COMMON_NAME,
    I_TAXON_GROUP,
    I_KINGDOM,
    I_ORDER,
    I_FAMILY,
    I_TAXONVERSIONKEY,
    I_SITE_NAME,
    I_ORIGINAL_MAP_REF,
    I_LATITUDE,
    I_LONGITUDE,
    I_PROJECTION_INPUT,
    I_PRECISION,
    I_OUTPUT_MAP_REF,
    I_PROJECTION_OUTPUT,
    I_BIOTOPE,
    I_VC_NUMBER,
    I_VICE_COUNTY,
    I_DATE_INTERPRETED,
    I_DATE_FROM,
    I_DATE_TO,
    I_DATE_TYPE,
    I_SAMPLE_METHOD,
    I_RECORDER,
    I_DETERMINER,
    I_RECORDER_CERTAINTY,
    I_SEX,
    I_STAGE,
    I_COUNT_OF_SEX_OR_STAGE,
    I_ZERO_ABUNDANCE,
    I_COMMENT,
    I_SAMPLE_COMMENT,
    I_IMAGES,
    I_INPUT_ON_DATE,
    I_LAST_EDITED_ON_DATE,
    I_VERIFICATION_STATUS_1,
    I_VERIFICATION_STATUS_2,
    I_QUERY,
    I_VERIFIER,
    I_VERIFIED_ON,
    I_LICENCE,
    I_AUTOMATED_CHECKS
]

# ------------------------------------------------------------------------------
# Swift export columns headers
S_NAME = 'Scientific or Common Name'
S_DATE = 'Date'
S_LOCATION = 'Location'
S_GRID_REFERENCE = 'Grid Reference'
S_ABUNDANCE = 'Abundance'
S_SEXSTAGE = 'Sex/Stage'
S_RECORD_TYPE = 'Record Type'
S_OBSERVER = 'Observer'
S_DETERMINER = 'Determiner'
S_COMMENTS = 'Comments'
S_DETERMINATION_TYPE = 'Determination Type'
S_DETERMINAION_COMMENT = 'Determination Comment'
# Additional columns for troubleshooting
S_KEY = 'Key'
S_IMPORTNOTE = 'Status note'
S_IMPORTTYPE = 'Status type'

S_COLUMNS = [
    S_IMPORTTYPE,
    S_IMPORTNOTE,
    S_KEY,
    S_NAME,
    S_DATE,
    S_LOCATION,
    S_GRID_REFERENCE,
    S_ABUNDANCE,
    S_SEXSTAGE,
    S_RECORD_TYPE,
    S_OBSERVER,
    S_DETERMINER,
    S_COMMENTS,
    S_DETERMINATION_TYPE,
    S_DETERMINAION_COMMENT
]

# ------------------------------------------------------------------------------
# Orders making up the Insecta class (classes not included in iRecord exports).

ORDERS_INSECTA = {
    'blattodea',
    'coleoptera',
    'dermaptera',
    'diptera',
    'embioptera',
    'ephemeroptera',
    'hemiptera',
    'hymenoptera',
    'isoptera',
    'lepidoptera',
    'mantodea',
    'mecoptera',
    'megaloptera',
    'microcoryphia',
    'neuroptera',
    'odonata',
    'orthoptera',
    'phasmatodea',
    'phthiraptera',
    'plecoptera',
    'psocoptera',
    'raphidioptera',
    'siphonaptera',
    'strepsiptera',
    'thysanoptera',
    'thysanura',
    'trichoptera',
    'zoraptera'
}

# ------------------------------------------------------------------------------

# Sex/stage terms.
FEMALE = 'female'       # Text to be written to Swift upload CSV
MALE = 'male'           # Text to be written to Swift upload CSV
SEX_TERMS = {
    'males': MALE,
    'male': MALE,
    'm': MALE,
    'females': FEMALE,
    'female': FEMALE,
    'fems': FEMALE,
    'fem': FEMALE,
    'f': FEMALE
}

# Stage terms.
ADULT = 'Adult'         # Text to be written to Swift upload CSV
JUVENILE = 'Juvenile'   # Text to be written to Swift upload CSV
LARVA = 'Larva'
NYMPH = 'Nymph'
STAGE_TERMS = {
    'adults': ADULT,
    'adult': ADULT,
    'ads': ADULT,
    'ad': ADULT,
    'chicks': JUVENILE,
    'chick': JUVENILE,
    'fledglings': JUVENILE,
    'fledgling': JUVENILE,
    'immature': JUVENILE,
    'imm': JUVENILE,
    'juveniles': JUVENILE,
    'juvenile': JUVENILE,
    'juvs': JUVENILE,
    'juv': JUVENILE,
    'sub-adult': JUVENILE,
    'sub-ad': JUVENILE,
    'young': JUVENILE,
    'larva': LARVA,
    'larvae': LARVA,
    'larval': LARVA,
    'nymph': NYMPH

}

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
    log.info('Beginning test [const.py]...')
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