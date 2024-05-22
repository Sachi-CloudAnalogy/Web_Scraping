from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://www.talabat.com/")

    text = page.locator("div[class='banner-content flex flex-column align-items-center text-center']").text_content()
    print(text)

    browser.close()