from beancount.ingest.importers.csv import Importer, Col, get_amounts
from enum import Enum
import sys

class CashAppCSVImporter(Importer):

    def get_amounts(self, iconfig, row, allow_zero_amounts, parse_amount):
        """See function get_amounts() for details.
        This method is present to allow clients to override it in order to deal
        with special cases, e.g., columns with currency symbols in them.
        """

        row[iconfig[Col.AMOUNT]] = row[iconfig[Col.AMOUNT]].replace("$", "")

        # sys.stderr.write(row[iconfig[AmazonCSVCol.AMOUNT_SUBTOTAL]])
        # raise NotImplementedError(str(subtotal))

        return get_amounts(iconfig, row, allow_zero_amounts, parse_amount)
