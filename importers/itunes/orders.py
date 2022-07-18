from playwright.sync_api import Playwright, sync_playwright, expect
from datetime import datetime
import json
from tqdm.cli import tqdm

playwright = sync_playwright().start()

browser = playwright.chromium.launch(headless=False)
context = browser.new_context()
page = context.new_page()
page.goto("https://reportaproblem.apple.com/")

input()

orders = []

for p in tqdm(page.query_selector_all(".purchase.loaded")):

    order = {}

    date = p.query_selector(".purchase-header span").text_content()
    if "PENDING" in date: continue

    orders.append(order)

    date = datetime.strptime(date, '%b %d, %Y')
    date = datetime.strftime(date, '%Y-%m-%d')

    items = []

    order["date"] = date
    order["items"] = items

    p.query_selector(".purchase-header").click()

    for item in p.query_selector_all(".pli"):
        items.append({
            "title": item.query_selector(".pli-title").text_content(),
            "price": item.query_selector(".pli-price").text_content() if item.query_selector(".pli-price") != "Free" else "$0.00",
            "date": item.query_selector(".pli-purchase-date").text_content(),
            "type": item.query_selector(".pli-media-type").text_content(),
            "subtitle": item.query_selector(".pli-publisher").text_content() if item.query_selector(".pli-publisher") else None,
        })

    if p.query_selector(".purchase-details.no-invoice"):
        continue

    p.wait_for_selector(".purchase-details.loaded")
    info = p.query_selector(".order-info-headers")

    if info:
        tmp = []
        for elem in p.query_selector(".order-info-headers").query_selector_all("span"):
            tmp.append(elem.text_content())

        # print(tmp)
        tmp = dict(list(zip(tmp[0::2], tmp[1::2])))

        order["id"] = tmp.get("Order ID", None)
        order["document"] = tmp.get("Document No.", None)
        order["total"] = tmp.get("Total", None)


        btn = info.query_selector("button")
        if btn:
            btn.click()
        
            page.wait_for_selector(".receipt.loaded")
            content = page.query_selector(".receipt.loaded").inner_html()
            page.query_selector(".close-receipt-button").click()
    
        with open("%s-%s.html" % (date, order["id"]), "w") as fp:
            fp.write(content)
 
with open("orders.json", "w") as fp:
    json.dump(orders, fp, indent=2)

with open("orders.html", "w") as fp:
    fp.write(page.content())

exit()