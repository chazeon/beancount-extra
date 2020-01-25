from beancount.core import data as b_data
from beancount.core import amount as b_amount
from beancount.core import number as b_number


def build_posting(account, number, currency):
    units = b_amount.Amount(b_number.D(number), currency)
    posting = b_data.Posting(
        account, units, None, None, None, None)
    return posting

def build_transaction(fname, lineno, account, date, description=None, number=None, currency="USD", txn_date=None):
    meta = b_data.new_metadata(fname, lineno)
    payee = None
    narration = description
    tags = b_data.EMPTY_SET
    links = b_data.EMPTY_SET
    postings = [build_posting(account, number, currency)]

    transaction = b_data.Transaction(
        meta, date, "*", payee, narration, tags, links, postings
    )

    return transaction