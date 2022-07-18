from dateutil.parser import parse
import json

from beancount.core import data
from beancount.ingest import importer

from beancount.core.number import D
from beancount.core.number import ZERO
from beancount.core import data
from beancount.core import account
from beancount.core import amount


class ItunesJSONImporter(importer.ImporterProtocol):

    def __init__(self, account, currency="USD"):
        super().__init__()
        self.account = account
        self.currency = currency

    def identify(self, file):
        if file.mimetype() != 'application/json':
            return False
        return True
    
    def file_account(self, _):
        return self.account

    def extract(self, file):

        index = 0

        with open(file.name) as fp:
            orders = json.load(fp)

        entries = []

        for order in orders:

            links = set()
            if "id" in order.keys():
                links.add(order["id"])

            is_free = ("total" not in order.keys())

            if not is_free:

                total = round(float(order.get("total", "$0.00").lstrip("$")), 2)
                price_total = round(sum(float(item["price"].lstrip("$")) for item in order["items"]), 2)
                cost_left = total
                taxed_rate = total / price_total

            for i, item in enumerate(order["items"]):

                postings = []

                if not is_free:

                    price = float(item["price"].lstrip("$"))

                    if i != len(order["items"]):
                        cost = round(price * taxed_rate, 2)
                    else:
                        cost = cost_left

                    postings.append(data.Posting(
                        account=self.account,
                        units=amount.Amount(D(f"{-cost:0.2f}"), self.currency),
                        cost=None,
                        price=None,
                        flag=None,
                        meta=None,
                    ))

                    cost_left -= cost

                    print(cost_left, cost)

                date = parse(order["date"]).date()
                document = f"{date}-{order['id']}.html" if not is_free else None
                if is_free:
                    meta = data.new_metadata(file.name, index)
                else:
                    meta = data.new_metadata(file.name, index, kvlist={
                        "document": document
                    })
                

                txn = data.Transaction(
                    meta=meta,
                    date=date,
                    flag=self.FLAG,
                    tags=data.EMPTY_SET,
                    links=links,
                    postings=postings,
                    payee="",
                    narration="{title} ({subtitle})".format_map(item),
                )
        
                entries.append(txn)

        return entries