from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json

count_of_restaurant = 0
# for restaurant details
restaurant_lists = []

for N in range(1, 21):
    web = f"https://www.talabat.com/kuwait/restaurants/48/sharq?page={N}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(web)
        page.wait_for_timeout(5000)  # Wait for 5 seconds to ensure the page loads

        content = page.content()
        soup = BeautifulSoup(content, 'html.parser')
        restaurant_list = []
        cafes = soup.find_all("div", class_="content")
        for i, cafe in enumerate(cafes):
            restaurant = {}
            restaurant["Restaurant Name"] = cafe.h2.text if cafe.h2 else "N/A"
            restaurant["Category"] = cafe.find("div").text if cafe.find("div") else "N/A"
            restaurant["Reviews"] = cafe.find("div", class_="ml-1 undefined").text if cafe.find("div",
                                                                                                class_="ml-1 undefined") else "N/A"
            restaurant["Delivery"] = cafe.find_all("div", class_="row-grid")[1].text.split("Delivery")[0] if len(
                cafe.find_all("div", class_="row-grid")) > 1 else "N/A"
            try:
                restaurant["Services"] = (cafe.find_all("span", class_="one-badge")[0].text) + ", " + (
                    cafe.find_all("span", class_="one-badge")[1].text)
            except Exception:
                restaurant["Services"] = "N/A"

            # Food Category and Dishes
            link = page.locator('a[data-testid="restaurant-a"]').all()[i]
            new_page = browser.new_page(base_url="https://www.talabat.com/")
            url = link.get_attribute("href")
            if url is not None:
                new_page.goto(url)
                new_page.wait_for_timeout(5000)  # Wait for 5 seconds to ensure the page loads

                soup = BeautifulSoup(new_page.content(), 'html.parser')
                items = soup.find_all("div", attrs={'data-testid': "menu-category"})
                food_items = []
                for item in items:
                    food = {}
                    category = item.find("h4").text if item.find("h4") else "N/A"
                    food['Food category'] = category

                    dish_list = item.find_all("div", class_="content open")
                    lists = []
                    for dishes in dish_list:
                        dish_elements = dishes.find_all("div",
                                                        class_="sc-a1cbee13-0 elGcpJ d-flex justify-content-between py-2 clickable")
                        for dish in dish_elements:
                            names = dish.find_all("div", class_="item-name")
                            prices = dish.find_all("div", class_="mb-m-1 price")

                            for n, p in zip(names, prices):
                                category = {}
                                name = n.find("div").text if n.find("div") else "N/A"
                                price = p.text if p else "N/A"
                                category["Name of the food"] = name
                                category["Price of the food"] = price
                                lists.append(category)
                    food['dishes'] = lists
                    food_items.append(food)
                restaurant["Food"] = food_items
                count_of_restaurant += 1
                restaurant["Restaurant Number"] = count_of_restaurant
                print(restaurant)
                print("Count Of Restaurant = ", count_of_restaurant)

                # storing in json file
                with open("talabat4.json", "a") as f:
                    json.dump(restaurant, f, indent=4)
                    f.write("\n")

                new_page.close()
            else:
                new_page.close()

            restaurant_list.append(restaurant)

        restaurant_lists.append(restaurant_list)

        browser.close()
    print(f"Page_no {N} done !!")

print("Finish !!")