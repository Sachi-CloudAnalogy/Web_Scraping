from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json

web = "https://www.talabat.com/kuwait/restaurants/48/sharq"

count_of_restaurant = 0
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(web)
    content = page.content()

    #for restaurant details
    restaurant_lists = []

    soup = BeautifulSoup(content, 'html.parser')
    #For pagination
    while True:
        restaurant_list = []
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
                count_of_restaurant += 1
                print(restaurant)
                print("Count Of Restaurant = ", count_of_restaurant)

            else:
                new_page.close()

            restaurant_list.append(restaurant)
            i = i+1
            new_page.close()

        #for different pages
        restaurant_lists.append(restaurant_list)

        # storing in json file
        with open("Restaurant_list.json", "w") as f:
            json.dump(restaurant_lists, f, indent=4)

        try:
            current_page = page.locator("li.sc-1b71585b-0.sc-1b71585b-2.bqafA-D.hEGBfg.-active").text_content()
        except Exception:
            current_page = page.locator("li.sc-1b71585b-0.sc-1b71585b-2.bqafA-D.hEGBfg.-first.-active").text_content()
        # try:
        #     last_page = page.locator("li.sc-1b71585b-0.sc-1b71585b-2.bqafA-D.hEGBfg.-last").text_content()
        # except Exception:
        #     last_page = page.locator("li.sc-1b71585b-0.sc-1b71585b-2.bqafA-D.hEGBfg.-last.-active").text_content()

        print(current_page + " out of 5 Pages")
        if int(current_page) == 5:
            print("No more Items !!")
            break
        else:
            page.locator("a[aria-label='Go to next page']").click()
            page.wait_for_timeout(2000)  # Wait for 2 seconds to ensure the page loads
            content = page.content()
            soup = BeautifulSoup(content, 'html.parser')


browser.close()
