from beancount.ingest import importer
import dateutil.parser
from pathlib import Path
import re

FNAME_REGEX = r"^(\d{4,4}[01]\d[0-3]\d)-statements-(\d{4,4})-$"

class ChaseStatementPDFImporter(importer.ImporterProtocol):

    def __init__(self, account, last4):
        self.account = account
        self.last4 = last4

    def _parse_date_last4(self):
        
        def parse(file):
            fname = Path(file).stem
            res = re.search(FNAME_REGEX, fname)
            if not res: return (None, None)
            return dateutil.parser.parse(res.group(1)).date(), res.group(2)

        return parse
        
    def identify(self, file):

        if file.mimetype() != "application/pdf": return False

        _, last4 = file.convert(self._parse_date_last4())
        if last4 is None or last4 != self.last4: return False

        return True

    def file_date(self, file):
        date, _ = file.convert(self._parse_date_last4())
        return date

    def file_account(self, file):
        return self.account

    def extract(self, file):
        return []