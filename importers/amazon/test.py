from beancount.ingest import regression_pytest
import pathlib

from beancount.ingest.importers import csv
from . import AmazonCSVImporter, AmazonCSVCol

importer = AmazonCSVImporter(
    config={
            csv.Col.DATE: "Order Date",
            csv.Col.NARRATION: "Product Name",
            AmazonCSVCol.AMOUNT_SUBTOTAL: "Item Subtotal",
            AmazonCSVCol.AMOUNT_SUBTOTAL_TAX: "Item Subtotal Tax",
            AmazonCSVCol.AMOUNT_SHIPPING: "Shipping Charge",
        },
    account="Liabilities:Payable:Amazon",
    currency="USD"
)

directory = pathlib.Path(__file__).parent / "sample"

@regression_pytest.with_importer(importer)
@regression_pytest.with_testdir(directory)
class TestImporter(regression_pytest.ImporterTestBase):
    pass