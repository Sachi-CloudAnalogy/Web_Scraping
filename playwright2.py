from playwright.sync_api import sync_playwright, Playwright
from rich import print
import json
def run(playwright: Playwright):
    start_url = "https://www.snapdeal.com/products/water-bottles?sort=plrty"
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(start_url)

    while True:
        for link in page.locator("a[class='dp-widget-link hashAdded']").all():
            new_page = browser.new_page(base_url="https://www.snapdeal.com/")
            url = link.get_attribute("href")
            if url is not None:
                new_page.goto(url)
            else:
                new_page.close()

            data = new_page.locator("script[type='application/ld+json']").all_text_contents()
            for d in data:
                json_data = json.loads(d)
                print(json_data)
            new_page.close()

            item_num = (page.locator("span.see-more-lower")).text_content()
            total_item = (page.locator("span.see-more-upper")).text_content()
            if int(item_num) == int(total_item):
                print("no more items !!")
                break
            else:
                page.locator("div.show-more btn btn-line btn-theme-secondary").click()

            browser.close()

with sync_playwright() as p:
    run(p)