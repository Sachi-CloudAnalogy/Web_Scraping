from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    #launch a browser
    browser = p.chromium.launch(headless=False, slow_mo=2000)
    #create a new page
    page = browser.new_page()
    #visit playwright website
    page.goto("https://bootswatch.com/default/")

    #locate an element
    button = page.get_by_role('button', name="Large button")
    button.highlight()
    button.click()

    email_input = page.get_by_label("Default file input example")
    email_input.highlight()
    email_input.click()

    page.get_by_placeholder("Enter email").highlight()

    page.get_by_text("Navbars").highlight()    #can select any link, button, or any text
    page.get_by_title("")

    #get the url
    print(page.url)

    browser.close()
