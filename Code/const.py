'''
About  : Define constants.
'''

from typing import Final

# ------------------------------------------------------------------------------
# Config file section headings and field names
C_DATA: Final[str] = 'Data'
C_FOLDER_IN: Final[str] = 'Folder_Input'
C_FOLDER_OUT: Final[str] = 'Folder_Output'
C_FILES: Final[str] = 'Files'
C_FILE_ABUNDANCE: Final[str] = 'File_Abundance'
C_FILE_DUPLICATES: Final[str] = 'File_Duplicates'
C_FILE_GIS: Final[str] = 'File_GIS'
C_FILE_EXC_TAXONS: Final[str] = 'File_ExcludedTaxons'
C_FILE_PERMS: Final[str] = 'File_iNatPermissions'
C_FILE_REC_TYPE: Final[str] = 'File_RecordType'
C_FILE_USERS: Final[str] = 'File_UserIdenties'
C_LOGGING: Final[str] = 'Logging'
C_LOGLEVEL: Final[str] = 'LogLevel'
C_OPTIONS: Final[str] = 'Options'
C_PLOT: Final[str] = 'Plot'
C_EXCEL: Final[str] = 'Excel'

# ------------------------------------------------------------------------------
# Swift species import file column headers.
B_TAXONKEY: Final[str] = 'preferred_taxon_key'
B_TAXONVERSION: Final[str] = 'taxon_version_key'
B_PARENTTAXON: Final[str] = 'parent_taxon_key'
B_COUNT: Final[str] = 'sum_records_count'
B_PRECISION: Final[str] = 'public_precision'
B_CONCATNAMES: Final[str] = 'concat_mixed_names'
B_CONCATABBREVS: Final[str] = 'concat_abbreviations'
B_TAXONGROUP: Final[str] = 'taxon_group'
B_COMMON: Final[str] = 'preferred_common_name'
B_SCIENTIFIC: Final[str] = 'preferred_scientific_name'
B_TAXONRANK: Final[str] = 'taxon_rank'
B_HIERARCHY: Final[str] = 'hierarchy'
B_VERIFICATION: Final[str] = 'verification_config'
B_DATE: Final[str] = 'date_updated'

# ------------------------------------------------------------------------------
# iRecord import file column headers
I_ID: Final[str] = 'ID'
I_RECORDKEY: Final[str] = 'RecordKey'
I_EXTERNAL_KEY: Final[str] = 'External key'
I_SOURCE: Final[str] = 'Source'
I_RANK: Final[str] = 'Rank'
I_TAXON: Final[str] = 'Taxon'
I_COMMON_NAME: Final[str] = 'Common name'
I_TAXON_GROUP: Final[str] = 'Taxon group'
I_KINGDOM: Final[str] = 'Kingdom'
I_ORDER: Final[str] = 'Order'
I_FAMILY: Final[str] = 'Family'
I_TAXONVERSIONKEY: Final[str] = 'TaxonVersionKey'
I_SITE_NAME: Final[str] = 'Site name'
I_ORIGINAL_MAP_REF: Final[str] = 'Original map ref'
I_LATITUDE: Final[str] = 'Latitude'
I_LONGITUDE: Final[str] = 'Longitude'
I_PROJECTION_INPUT: Final[str] = 'Projection (input)'
I_PRECISION: Final[str] = 'Precision'
I_OUTPUT_MAP_REF: Final[str] = 'Output map ref'
I_PROJECTION_OUTPUT: Final[str] = 'Projection (output)'
I_BIOTOPE: Final[str] = 'Biotope'
I_VC_NUMBER: Final[str] = 'VC number'
I_VICE_COUNTY: Final[str] = 'Vice County'
I_DATE_INTERPRETED: Final[str] = 'Date interpreted'
I_DATE_FROM: Final[str] = 'Date from'
I_DATE_TO: Final[str] = 'Date to'
I_DATE_TYPE: Final[str] = 'Date type'
I_SAMPLE_METHOD: Final[str] = 'Sample method'
I_RECORDER: Final[str] = 'Recorder'
I_DETERMINER: Final[str] = 'Determiner'
I_RECORDER_CERTAINTY: Final[str] = 'Recorder certainty'
I_SEX: Final[str] = 'Sex'
I_STAGE: Final[str] = 'Stage'
I_COUNT_OF_SEX_OR_STAGE: Final[str] = 'Count of sex or stage'
I_ZERO_ABUNDANCE: Final[str] = 'Zero abundance'
I_COMMENT: Final[str] = 'Comment'
I_SAMPLE_COMMENT: Final[str] = 'Sample comment'
I_IMAGES: Final[str] = 'Images'
I_INPUT_ON_DATE: Final[str] = 'Input on date'
I_LAST_EDITED_ON_DATE: Final[str] = 'Last edited on date'
I_VERIFICATION_STATUS_1: Final[str] = 'Verification status 1'
I_VERIFICATION_STATUS_2: Final[str] = 'Verification status 2'
I_QUERY: Final[str] = 'Query'
I_VERIFIER: Final[str] = 'Verifier'
I_VERIFIED_ON: Final[str] = 'Verified on'
I_LICENCE: Final[str] = 'Licence'
I_AUTOMATED_CHECKS: Final[str] = 'Automated checks'
# Additional key to allow cross-referencing between files
I_KEY: Final[str] = 'Key'
I_IMPORTNOTE: Final[str] = 'Status note'
I_IMPORTTYPE: Final[str] = 'Status type'

I_COLUMNS: Final[list[str]] = [
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
S_NAME: Final[str] = 'Scientific or Common Name'
S_DATE: Final[str] = 'Date'
S_LOCATION: Final[str] = 'Location'
S_GRID_REFERENCE: Final[str] = 'Grid Reference'
S_ABUNDANCE: Final[str] = 'Abundance'
S_SEXSTAGE: Final[str] = 'Sex/Stage'
S_RECORD_TYPE: Final[str] = 'Record Type'
S_OBSERVER: Final[str] = 'Observer'
S_DETERMINER: Final[str] = 'Determiner'
S_COMMENTS: Final[str] = 'Comments'
S_DETERMINATION_TYPE: Final[str] = 'Determination Type'
S_DETERMINAION_COMMENT: Final[str] = 'Determination Comment'
# Additional columns for troubleshooting
S_KEY: Final[str] = 'Key'
S_IMPORTNOTE: Final[str] = 'Status note'
S_IMPORTTYPE: Final[str] = 'Status type'

S_COLUMNS: Final[list[str]] = [
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

ORDERS_INSECTA: Final[set[str]] = {
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
FEMALE: Final[str] = 'female'       # Text to be written to Swift upload CSV
MALE: Final[str] = 'male'           # Text to be written to Swift upload CSV
SEX_TERMS: Final[dict[str, str]] = {
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
ADULT: Final[str] = 'Adult'         # Text to be written to Swift upload CSV
JUVENILE: Final[str] = 'Juvenile'   # Text to be written to Swift upload CSV
LARVA: Final[str] = 'Larva'
NYMPH: Final[str] = 'Nymph'
STAGE_TERMS: Final[dict[str, str]] = {
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

'''
End
'''
