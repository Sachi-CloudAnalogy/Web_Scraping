from bs4 import BeautifulSoup
import requests
import db_handler

def scrape_laptops():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0 Safari/537.36'}
        url = "https://www.amazon.in/s?k=laptop&crid=2V1YRGR7JF2J5&sprefix=laptop%2Caps%2C252&ref=nb_sb_noss_1"
        r = requests.get(url, headers=headers)
        r.raise_for_status()

        soup = BeautifulSoup(r.content, "html.parser")

        title_list = soup.findAll("span", class_="a-size-medium a-color-base a-text-normal")
        # for i in range(len(title_list)):
        #     print(title_list[i].text)

        star_list = soup.findAll("div", class_="a-row a-size-small")

        # for i in range(len(title_list)):
        #     print(star_list[i].text.split('stars')[0])
       # sold_list = soup.findAll("span", class_="a-size-base a-color-secondary")
        # for i in range(len(title_list)):
        #     print(sold_list[i].text)

        price_div = soup.findAll("div", class_="a-row a-size-base a-color-base")
        # for i in range(len(title_list)):
        #     prev_price = price_div[i].text.split("₹")[-1]
        #     curr_price = price_div[i].text.split("₹")[1]
        #     print(prev_price, curr_price)

        laptops = []
        for i in range(len(title_list)):
            dict = {}
            dict["Title"] = title_list[i].text
            dict["Stars"] = star_list[i].text.split('stars')[0]
           # dict['Sold'] = sold_list[i].text
            prev_price = price_div[i].text.split("₹")[-1]
            curr_price = price_div[i].text.split("₹")[1]
            dict['Current Price'] = "₹" + curr_price
            dict['Previous Price'] = "₹" + prev_price

            laptops.append(dict)

        # for l in laptops:
        #     print(l)

        return laptops

    except Exception as e:
        print(e)
        return []

if __name__ == "__main__":
    laptops = scrape_laptops()
    db_handler.store_laptops(laptops)
    for laptop in laptops:
        print(laptop)