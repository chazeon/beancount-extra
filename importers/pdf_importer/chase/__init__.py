from beancount.ingest import importer
import dateutil.parser
from pathlib import Path
import re

FNAME_REGEX = r"^(\d{4,4}[01]\d[0-3]\d)-statements-(\d{4,4})-$"

class ChaseStatementPDFImporter(importer.ImporterProtocol):

    def __init__(self, account, last4, currency: str ="USD"):
        self.account = account
        self.last4 = last4
        self.currency = currency

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
        if len(row) != 4: return []
        if has_table < 2:
            if row[0] == "TRANSACTION DETAIL":
                has_table = 2
                continue
            else:
                continue
        is_table = True
        if row[1] == "Beginning Balance": continue
        if (
            is_table == True and
            re.search(r"[01]\d/[0123]\d", row[0]) 
        ):
            if len(res_row) > 1: res_rows.append(res_row)
            res_row = [row[0], row[1], row[2]]
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
            # res_row[0] += row[0]
            res_row[1] += (" " + row[1])
            res_row[2] += row[2]
        print("> " + repr(res_row))

    if is_table == True:
        res_rows.append(res_row)
        res_row = []
        is_table = False
        res_tables.append(res_rows)
        res_rows = []
    
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
            print(row)
            transaction = build_transaction(
                repr(fname),
                next(counter),
                account,
                dateutil.parser.parse(row[0]).date(),
                row[1],
                row[2],
                currency
            )
            yield transaction
