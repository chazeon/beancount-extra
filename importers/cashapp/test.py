from beancount.ingest import regression_pytest
import pathlib

from beancount.ingest.importers import csv
from . import CashAppCSVImporter

importer = CashAppCSVImporter(
    config={
            csv.Col.DATE: "Date",
            csv.Col.AMOUNT: "Amount",
            csv.Col.NARRATION1: "Notes",
            csv.Col.NARRATION2: "Transaction Type"
        },
    account="Assets:EWallet:US:CashApp",
    currency="USD"
)

directory = pathlib.Path(__file__).parent / "sample"

@regression_pytest.with_importer(importer)
@regression_pytest.with_testdir(directory)
class TestImporter(regression_pytest.ImporterTestBase):
    pass