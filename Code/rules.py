'''
About  : Implements the Rules class which contains the logic to transform
         iRecord data into Swift format.
'''

# ------------------------------------------------------------------------------

import logging
import re
from typing import Final, TypeAlias
from datetime import datetime

import const
import utils
from crosscheck import Crosschecker

# ------------------------------------------------------------------------------

log: logging.Logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------

Record: TypeAlias = dict[str, str]
Records: TypeAlias = list[Record]

# Types for de-duping. Use this approach for performance reasons.
DupeTuple: TypeAlias = tuple[str, str, str, str, str, str, str, str, str]
DupeDict: TypeAlias = dict[DupeTuple, str]

# ------------------------------------------------------------------------------

class Rules:
    '''Class which performs the transformation of iRecord data into Swift format.'''
    NO_RECORD: Final[str] = 'not recorded'  # iRecord standard text

    # --------------------------------------------------------------------------

    def __init__(self, record: Record, crosscheck: Crosschecker) -> None:
        '''Constructor.
        Args: 
            record (Record) = iRecord record to be assessed
            crosscheck (CrossChecker) - instance of object used for lookups
        Returns: 
            N/A
        '''
        self.crosscheck = crosscheck
        self.record = record.copy()
        # Returned processed records in list format as one record may be cloned
        self.swift: Records = []

    # --------------------------------------------------------------------------

    def get_swift(self) -> Records:
        '''Populate the 'swift' export list.
        Args: 
            N/A
        Returns: 
            (list) - 'swift' list
        '''
        self.init_swift()
        self.get_swift_identity()
        self.get_swift_recordtype()
        self.get_swift_comment()    # call second last in sequence
        self.get_swift_sexstage()   # call last in sequence - cloning of dict
        return self.swift

    # --------------------------------------------------------------------------

    def get_swift_comment(self) -> None:
        '''Process the comment data. Generate comment from multiple fields.
        Args: 
            N/A
        Returns: 
            N/A
        '''
        # ----------------------------------------------------------------------
        def formatstr(name: str, value: str) -> str:
            '''Format a sub-section of the comment string.'''
            v = value.strip()
            return f'[{name}: "{v}"] ' if len(v) > 0 else ''
        # ----------------------------------------------------------------------

        com = det_com = ''
        com += formatstr('iRecord Key', self.record[const.I_RECORDKEY])
        com += formatstr('Source', self.record[const.I_SOURCE])
        com += formatstr('Recorder certainty', self.record[const.I_RECORDER_CERTAINTY])
        com += formatstr('Comment', self.record[const.I_COMMENT])
        com += formatstr('Sample Comment', self.record[const.I_SAMPLE_COMMENT])
        v = self.record[const.I_VERIFIER]
        com += formatstr('Verifier', v)
        if len(v) > 0:
            det_com += f'Verified by {v} '
        vos = self.record[const.I_VERIFIED_ON]
        if len(vos) > 0:
            dto = datetime.strptime(vos, '%d/%m/%Y %H:%M')
            dts = dto.strftime('%d/%m/%Y')
            com += formatstr('Verified on', dts)
            det_com += dts
        com += formatstr('Licence', self.record[const.I_LICENCE])

        s = self.swift[0]
        p = self.record
        s[const.S_COMMENTS] = com
        s[const.S_DETERMINAION_COMMENT] = det_com
        if p[const.I_VERIFICATION_STATUS_2].lower() == 'not reviewed':
            s[const.S_DETERMINATION_TYPE] = 'Requires Confirmation'
        else:
            s[const.S_DETERMINATION_TYPE] = p[const.I_VERIFICATION_STATUS_2]

    # --------------------------------------------------------------------------

    def get_swift_identity(self) -> None:
        '''Process the identity data. Complicated by potential use of usernames.
        Args: 
            N/A
        Returns: 
            N/A
        '''
        # ----------------------------------------------------------------------
        # Return the supplied name in a Swift-compatible format
        def formatstr(name: str) -> str:
            if len(name) == 0:
                return name

            # Use only first name if more than one supplied
            p = name.split(';')
            n = name if len(p) == 1 else p[0]
            # Do we have 'surname, forename'?
            p = n.split(',')
            if len(p) > 1:
                rv = ' '.join(reversed(p))
            else:
                # Do we have 'forename surname'?
                p = n.split(' ')
                if len(p) > 1:
                    rv = n
                else:
                    # Assume we have a username - ok to use real identity?
                    rv = self.crosscheck.get_user_identity(name)
                    if len(rv) == 0:
                        # Permission for identity not granted
                        s_l = self.record[const.I_SOURCE].lower()
                        if 'irecord' in s_l:
                            rv = 'Anon at iRecord'
                        elif 'inaturalist' in s_l:
                            rv = 'Anon at iNaturalist'
                        else:
                            rv = name
                            log.debug('Unknown source: %s', s_l)

            return rv.strip()
        # ----------------------------------------------------------------------
        # Process the identities contained within iRecord.
        rec = formatstr(self.record[const.I_RECORDER])
        det = formatstr(self.record[const.I_DETERMINER])
        # ver = formatstr(self.record[const.I_VERIFIER])

        self.swift[0][const.S_OBSERVER] = rec
        self.swift[0][const.S_DETERMINER] = det

    # --------------------------------------------------------------------------

    def get_swift_recordtype(self) -> None:
        '''Process the record type data. Map iRecord to Swift equivalent.
        Args: 
            N/A
        Returns: 
            N/A
        '''
        msg = 'Record Type'
        msg_note = '[Record Type: "{}"; Comment: "{}"]'
        p = self.record
        s = self.swift[0]
        rt = self.crosscheck.get_record_type(p[const.I_SAMPLE_METHOD], p[const.I_IMAGES])
        if rt is None:
            # add unknown sample method warning
            s[const.S_IMPORTTYPE] = utils.append_comment(s[const.S_IMPORTTYPE],
                                                         msg)
            note = msg_note.format(p[const.I_SAMPLE_METHOD], p[const.I_COMMENT])
            s[const.S_IMPORTNOTE] = (s[const.S_IMPORTNOTE] + ' ' + note if
                len(s[const.S_IMPORTNOTE]) > 0 else note)
        else:
            s[const.S_RECORD_TYPE] = rt

    # --------------------------------------------------------------------------

    def get_swift_sexstage(self) -> None:
        '''Process the sex/stage data. Complicated by potential need to clone record.
        Args: 
            N/A
        Returns: 
            N/A
        '''
        msg = 'Cloned'
        msg_note = '[Count of sex or stage: "{}"; Sex: "{}"; Stage: "{}"]'

        p = self.record
        s = self.swift[0]
        match, abund = self.crosscheck.get_abundance(p[const.I_TAXON_GROUP],
                                              p[const.I_COUNT_OF_SEX_OR_STAGE])
        if match is True:
            s[const.S_ABUNDANCE] = abund

        c = p[const.I_COUNT_OF_SEX_OR_STAGE].strip()
        n = utils.word_to_num(c)
        if n is not None:
            c = str(n)
        # If count is a number or number range, then return
        if len(c) == 0 or c.replace('-', '').isdigit():
            return

        # Extract abundance
        pattern = r">?c?\d[0-9\-+/,'s ]*"
        num = re.findall(pattern, c)
        # Extract sex/stage terms
        trm = re.split(pattern, c)
        if all(len(t) == 0 for t in trm):
            return
        if len(num) != len(trm)-1:
            log.error('"%s" parse error: %s', const.I_COUNT_OF_SEX_OR_STAGE, c)
            return
        # Prepare for cloning of records
        p_c = self.record
        s_c = self.swift[0]
        # If 'mixed' & not already flagged for cloning then record will be cloned
        mixed_clone = p_c[const.I_SEX].lower() == 'mixed' and len(num) == 0
        # Make a comment to indicate record has been cloned
        if len(num) > 1 or mixed_clone:
            sex = p_c[const.I_SEX].strip()
            stage = p_c[const.I_STAGE].strip()
            s_c[const.S_IMPORTTYPE] = utils.append_comment(
                    s_c[const.S_IMPORTTYPE], msg)
            note = msg_note.format(c, sex, stage)
            s_c[const.S_IMPORTNOTE] = (s_c[const.S_IMPORTNOTE] + ' ' + note if
                len(s_c[const.S_IMPORTNOTE]) > 0 else note)

        if mixed_clone:
            stage = p_c[const.I_STAGE].lower().strip()
            if stage in const.STAGE_TERMS:
                stage = const.STAGE_TERMS[stage].capitalize()
            s_c[const.S_SEXSTAGE] = f'{stage} {const.MALE}'.strip()
            s_c = self.swift[0].copy()
            s_c[const.S_SEXSTAGE] = f'{stage} {const.FEMALE}'.strip()
            self.swift.append(s_c)

        # Process each pair of number and term
        for i, term in enumerate(num):
            sex = ''
            stage = ''
            spec = trm[i+1].lower().strip()
            spec = re.sub(r'[(),]', '', spec)
            # Parse spec into separate words and check against sex/stage terms
            words = spec.split()
            for word in words:
                # Is this a sex/stage term?
                if word in const.STAGE_TERMS:
                    stage = const.STAGE_TERMS[word].capitalize()
                elif word in const.SEX_TERMS:
                    sex = const.SEX_TERMS[word].lower()
            # No stage found in comment - use 'Stage' field
            if len(stage) == 0:
                stage = p_c[const.I_STAGE]

            s_c[const.S_ABUNDANCE] = term.strip()
            s_c[const.S_SEXSTAGE] = f'{stage} {sex}'.strip()
            # Avoid duplicating first record
            if i > 0:
                self.swift.append(s_c)
            # Prepare for next loop
            s_c = self.swift[0].copy()

    # --------------------------------------------------------------------------

    def init_swift(self) -> None:
        '''Initialise the Swift export list.
        Args: 
            N/A
        Returns: 
            N/A
        '''
        self.swift.clear()
        s = {}
        c = self.record[const.I_COUNT_OF_SEX_OR_STAGE].lower()
        n = utils.word_to_num(c)
        if n is not None:
            c = str(n)

        stage = '' if self.record[const.I_STAGE].lower() == self.NO_RECORD \
                    else self.record[const.I_STAGE].capitalize()
        sex = '' if self.record[const.I_SEX].lower() == self.NO_RECORD \
                    else self.record[const.I_SEX].lower()
        s[const.S_KEY] = self.record[const.I_KEY]
        s[const.S_IMPORTTYPE] = ''
        s[const.S_IMPORTNOTE] = ''
        s[const.S_NAME] = self.record[const.I_TAXON]
        s[const.S_DATE] = self.record[const.I_DATE_FROM]
        s[const.S_LOCATION] = self.record[const.I_SITE_NAME]
        s[const.S_GRID_REFERENCE] = self.record[const.I_OUTPUT_MAP_REF]
        s[const.S_ABUNDANCE] = c
        s[const.S_SEXSTAGE] = f'{stage} {sex}'.strip()
        s[const.S_RECORD_TYPE] = ''
        s[const.S_OBSERVER] = ''
        s[const.S_DETERMINER] = ''
        s[const.S_COMMENTS] = ''
        s[const.S_DETERMINATION_TYPE] = ''
        s[const.S_DETERMINAION_COMMENT] = ''
        self.swift.append(s)

    # --------------------------------------------------------------------------

    def is_skip(self, records: Records, dupedict: DupeDict) -> tuple[str, str]:
        '''Perform tests to determine whether record should be skipped.
        Args: 
            records (Records) - potential new record, including clones
            dupedict (DupeDict) - dict of existing records
        Returns: 
            (string, string) - type/note with reasons for skip, else ('','')
        '''
        rvs = []   # list of tuples returned from individual tests
        # Run tests
        rvs.append(self.is_skip_duplicate(records, dupedict))
        rvs.append(self.is_skip_gridref())
        rvs.append(self.is_skip_licence())
        rvs.append(self.is_skip_rank())
        rvs.append(self.is_skip_region())
        rvs.append(self.is_skip_verification())
        # Process results of all tests into two strings returned as a tuple
        rv_n = rv_t = ''
        for rv in rvs:
            rv_t += rv[0]
            rv_n += rv[1]

        return rv_t.strip(' ;'), rv_n.strip(' ;')

    # --------------------------------------------------------------------------

    def is_skip_duplicate(self, records: Records, dupedict: DupeDict) -> tuple[str, str]:
        '''Determine whether record should be skipped because it is a duplicate.
        Args: 
            record (Record) - potential new record, including duplicates
            dupedict (DupeDict) - dict of existing records
        Returns: 
            (string, string) - type/note describing reason for skip, else ''
        '''
        rec = records[0]
        dupecheck: DupeTuple = (
            rec[const.S_NAME],
            rec[const.S_DATE],
            rec[const.S_LOCATION],
            rec[const.S_GRID_REFERENCE],
            rec[const.S_ABUNDANCE],
            rec[const.S_SEXSTAGE],
            rec[const.S_RECORD_TYPE],
            rec[const.S_OBSERVER],
            rec[const.S_DETERMINER]
        )
        skip_str = '[Duplicate: "{}"] '
        rv_n = rv_t = ''
        if dupecheck in dupedict:
            rv_t = ' Duplicate;'
            rv_n = skip_str.format(dupedict[dupecheck])
        else:
            dupedict[dupecheck] = rec[const.S_KEY]

        return rv_t, rv_n

    # --------------------------------------------------------------------------

    def is_skip_gridref(self) -> tuple[str, str]:
        '''Determine whether record should be skipped based upon its gridref.
        Args: 
            N/A
        Returns: 
            (string, string) - type/note describing reason for skip, else ''
        '''
        skip_str = '[Gridref: "{}"] '
        g = self.record[const.I_OUTPUT_MAP_REF]     # gridref
        rv_n = ''
        if len(g) < 6:      # confirm correct minimum length?
            rv_n = skip_str.format(g)

        rv_t = ' Gridref;' if len(rv_n) > 0 else ''
        return rv_t, rv_n

    # --------------------------------------------------------------------------

    def is_skip_licence(self) -> tuple[str, str]:
        '''Determine whether record should be skipped based upon its licence.
        Args: 
            N/A
        Returns: 
            (string, string) - type/note describing reason for skip, else ''
        '''
        skip_str = '[Licence: "{}"] '
        l_u = self.record[const.I_LICENCE].upper()     # licence
        r_l = self.record[const.I_RECORDER].lower()    # recorder
        rv_n = ''
        if (l_u in {'CC BY', 'CC BY-NC'} and
                not self.crosscheck.is_permission_granted(r_l)):
            rv_n = skip_str.format(l_u)

        rv_t = ' Licence;' if len(rv_n) > 0 else ''
        return rv_t, rv_n

    # --------------------------------------------------------------------------

    def is_skip_rank(self) -> tuple[str, str]:
        '''Determine whether record should be skipped based upon its rank.
        Args: 
            N/A
        Returns: 
            (string, string) - type/note describing reason for skip, else ''
        '''
        skip_str = '[Rank: "{}"; Kingdom: "{}"; Order: "{}"; Taxon: "{}"] '
        k_l = self.record[const.I_KINGDOM].lower()  # kingdom
        o_l = self.record[const.I_ORDER].lower()    # order
        r_l = self.record[const.I_RANK].lower()     # rank
        t_l = self.record[const.I_TAXON].lower()    # taxon
        rv_n = ''
        if r_l in ['domain', 'kingdom', 'class', 'order']:
            # Not acceptable
            rv_n = skip_str.format(r_l, k_l, o_l, t_l)
        elif r_l == 'family':
            # Acceptable for insects only (possibly with some exceptions)
            if (o_l not in const.ORDERS_INSECTA or
                    self.crosscheck.is_excluded_taxon(t_l)):
                rv_n = skip_str.format(r_l, k_l, o_l, t_l)
        elif r_l == 'genus':
            # Acceptable for insects, plants and bats only
            if (o_l not in const.ORDERS_INSECTA and k_l != 'plantae' and
                o_l != 'chiroptera'):
                rv_n = skip_str.format(r_l, k_l, o_l, t_l)

        rv_t = ' Rank;' if len(rv_n) > 0 else ''
        return rv_t, rv_n

    # --------------------------------------------------------------------------

    def is_skip_region(self) -> tuple[str, str]:
        '''Determine whether record should be skipped based upon whether it is
           inside/outside the in-scope VC region.
        Args: 
            N/A
        Returns: 
            (string, string) - type/note describing reason for skip, else ''
        '''
        skip_str = '[Region: "{}"] '
        g = self.record[const.I_OUTPUT_MAP_REF]     # gridref
        inside = self.crosscheck.georegion.gridref_in_region(g)
        rv_n = ''
        if not inside:
            rv_n = skip_str.format(g)

        rv_t = ' Region;' if len(rv_n) > 0 else ''
        return rv_t, rv_n

    # --------------------------------------------------------------------------

    def is_skip_verification(self) -> tuple[str, str]:
        '''Determine whether record should be skipped based upon its verification.
        Args: 
            N/A
        Returns: 
            (string, string) - type/note describing reason for skip, else ''
        '''
        skip_str = '[Verification 1: "{}"; Verification 2: "{}"] '
        v1_l = self.record[const.I_VERIFICATION_STATUS_1].lower()   # verify 1
        v2_l = self.record[const.I_VERIFICATION_STATUS_2].lower()   # verify 2
        if (v1_l in {'accepted', 'queried', 'unconfirmed'} and
            v2_l in {'considered correct', 'correct', 'not reviewed',
                     'plausible', 'unconfirmed', ''}):
            rv_n = ''
        else:
            rv_n = skip_str.format(v1_l, v2_l)

        rv_t = ' Verification;' if len(rv_n) > 0 else ''
        return rv_t, rv_n

# ------------------------------------------------------------------------------

'''
End
'''
