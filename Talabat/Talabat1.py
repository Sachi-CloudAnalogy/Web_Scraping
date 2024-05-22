from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json

web = "https://www.talabat.com/kuwait/restaurants/48/sharq"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(web)
    content = page.content()

    #for restaurant details
    restaurant_list = []

    soup = BeautifulSoup(content, 'html.parser')
    cafes = soup.find_all("div", class_="content")
    i=0
    for cafe in cafes:
        restaurant = {}
        restaurant["Name"] = cafe.h2.text
        restaurant["Category"] = cafe.find("div").text
        restaurant["Reviews"] = cafe.find("div", class_="ml-1 undefined").text
        restaurant["Delivery"] = cafe.find_all("div", class_="row-grid")[1].text.split("Delivery")[0]
        try:
            restaurant["Services"] = (cafe.find_all("span", class_="one-badge")[0].text) + ", " + (cafe.find_all("span", class_="one-badge")[1].text)
        except Exception:
            restaurant["Services"] = "N/A"


        # Food Category and Dishes
        # for link in page.locator('a[data-testid="restaurant-a"]').all()[i]:
        link = page.locator('a[data-testid="restaurant-a"]').all()[i]
        new_page = browser.new_page(base_url="https://www.talabat.com/")
        url = link.get_attribute("href")
        if url is not None:
            new_page.goto(url)

            soup = BeautifulSoup(new_page.content(), 'html.parser')
            items = soup.find_all("div", attrs={'data-testid': "menu-category"})
            food_items = []
            for item in items:
                food = {}
                category = item.find("h4").text
                food['Category'] = category

                dish_list = item.find_all("div", class_="content open")
                for dishes in dish_list:
                    dishes = dishes.find_all("div", class_="sc-a1cbee13-0 elGcpJ d-flex justify-content-between py-2 clickable")
                    lists = []
                    for dish in dishes:
                        names = dish.find_all("div", class_="item-name")
                        prices = dish.find_all("div", class_="mb-m-1 price")


                        for n, p in zip(names, prices):
                            category = {}
                            name = n.find("div").text
                            price = p.text
                            category["Name"] = name
                            category["Price"] = price
                            lists.append(category)
                            food['dishes'] = lists

                food_items.append(food)
            restaurant["Food"] = food_items
            print(restaurant)

        else:
            new_page.close()

        restaurant_list.append(restaurant)
        i = i+1
        new_page.close()

    #storing in json file
    with open("restaurants.json", "w") as f:
        json.dump(restaurant_list, f, indent=4)

browser.close()
