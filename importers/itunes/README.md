# Apple iTunes 

## Introduction 

Apple's AppStore indends to take over the relationship between the consumer and App Developer. For consumer, the shows as `APPLE.COM/BILL 866-712-7753 CA / PAYMENT`, makes it particular challeging to understand the subscription detail.

The order information is only accessible through iTunes, you can only look at these orders, but there is no way to export these data, as CSV / HTML. Not to mention the receipts.

Apple Card make it a little easier if one is using iPhone, but consumer can only access the detail data within the Apple Wallet, but does not have a way to access the raw data for post processing or book-keeping. So the situation is basically no better than iTunes.

Apple seems to only able to export user's order data "[Get a copy of your data](https://support.apple.com/en-us/HT208502)" but normally you will have to wait days and those links have an expiration date.

Right now the only way seems to be able to access to these data via open web technoly is through the [Report a Problem](https://reportaproblem.apple.com/) page, which will list your order detail in the past ~6mos.

Therefore I have to create my script to give me access to these records.

## Usage

### Scraping

The `orders.py` scripts is based on Microsoft's Playwright engine. You execute

```bash
python orders.py
```

it opens [Report a Problem](https://reportaproblem.apple.com/) page. You do the login, it scrape the order information and save them to a `orders.json` and save receipts as HTML files.

### Importing

There is also a Beancount importer `__init__.py` for `bean-extract` to convert the `order.json` into Beancount format, with receipts linked.