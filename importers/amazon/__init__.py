from beancount.ingest.importers import csv
from enum import Enum
import sys

class AmazonCSVCol(Enum):
    # Extra fields for Amazon
    AMOUNT_SUBTOTAL = "[SUBTOTAL]"
    AMOUNT_SUBTOTAL_TAX = "[TAX]"
    AMOUNT_SHIPPING = "[SHIPPING]"

class AmazonCSVImporter(csv.Importer):

    def get_amounts(self, iconfig, row, allow_zero_amounts, parse_amount):
        """See function get_amounts() for details.
        This method is present to allow clients to override it in order to deal
        with special cases, e.g., columns with currency symbols in them.
        """

        subtotal = parse_amount(row[iconfig[AmazonCSVCol.AMOUNT_SUBTOTAL]])
        tax = parse_amount(row[iconfig[AmazonCSVCol.AMOUNT_SUBTOTAL_TAX]])
        shipping = parse_amount(row[iconfig[AmazonCSVCol.AMOUNT_SHIPPING]])

        total = sum(subtotal, tax, shipping)

        return (None, total)