from beancount.ingest import importer
import dateutil.parser
from pathlib import Path
import re

FNAME_REGEX = r"^eStmt_(\d{4,4}-[01]\d-[0-3]\d)$"

class ChaseStatementPDFImporter(importer.ImporterProtocol):

    def __init__(self, account, currency: str ="USD"):
        self.account = account
        self.currency = currency

    def _parse_date(self):
        
        def parse(file):
            fname = Path(file).stem
            res = re.search(FNAME_REGEX, fname)
            if not res: return None
            return dateutil.parser.parse(res.group(1))

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
        return list(_get_transactions(
            account=self.account,
            currency=self.currency,
            fname=file.name))

            
import itertools, io, csv
import camelot
from ..utils import build_transaction


def _process_csv(text_csv):
    sio = io.StringIO(text_csv)
    reader = csv.reader(sio)

    is_table = False
    has_table = 0

    res_tables = []
    res_rows = []
    res_row = []
    for row in reader:
        if len(row) != 7: return []
        if has_table < 2:
            if (
                row[0] == "Date" and
                row[1] == "Date" and
                row[2] == "Description" and
                row[3] == "Number" and
                row[4] == "Number" and
                row[5] == "Amount" and
                row[6] == "Total" 
            ):
                has_table = 2
                continue
            else:
                continue
        if (
            is_table == False and
            re.search(r"[01]\d/[0123]\d", row[0]) and
            re.search(r"[01]\d/[0123]\d", row[1])
        ):
            is_table = True
        if (
            is_table == True and
            re.search(r"[01]\d/[0123]\d", row[0]) and
            re.search(r"[01]\d/[0123]\d", row[1])
        ):
            if len(res_row) > 1: res_rows.append(res_row)
            res_row = [row[0], row[1], row[2], row[5]]
        elif (
            is_table == True and
            (row[2].startswith("TOTAL") or row[2].startswith("continue"))
        ):
            res_rows.append(res_row)
            res_row = []
            is_table = False
            res_tables.append(res_rows)
            res_rows = []
        elif (
            is_table == True
        ):
            res_row[0] += row[0]
            res_row[1] += row[1]
            res_row[2] += (" " + row[2])
            res_row[3] += row[5]
    return res_tables
    

def _get_transactions(account, currency, fname: Path):
    tables = camelot.read_pdf(str(fname), flavor="stream", pages="all")
    res = []
    for table in tables:
        sio = io.StringIO()
        table.to_csv(sio)
        res.extend(_process_csv(sio.getvalue()))
    counter = itertools.count()
    for table in res:
        for row in table:
            transaction = build_transaction(
                repr(fname),
                next(counter),
                account,
                dateutil.parser.parse(row[1]).date(),
                row[2],
                row[3],
                currency
            )
            yield transaction
