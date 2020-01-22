from beancount.ingest import importer
import dateutil.parser
from pathlib import Path
import re

FNAME_REGEX = r"^eStmt_(\d{4,4}-[01]\d-[0-3]\d)$"

class ChaseStatementPDFImporter(importer.ImporterProtocol):

    def __init__(self, account):
        self.account = account

    def _parse_date(self):
        
        def parse(file):
            fname = Path(file).stem
            res = re.search(FNAME_REGEX, fname)
            if not res: return None
            return res.group(1)

        return parse
        
    def identify(self, file):

        if file.mimetype() != "application/pdf": return False
        if file.convert(self._parse_date()) is None: return False

        return True

    def file_date(self, file):
        date = file.convert(self._parse_date())
        return date

    def file_account(self, file):
        return self.account

    def extract(self, file):
        return []