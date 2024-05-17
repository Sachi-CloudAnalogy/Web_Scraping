from bs4 import BeautifulSoup
import requests
import database

try:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0 Safari/537.36'}
    url = "https://www.amazon.in/s?k=laptop&crid=2V1YRGR7JF2J5&sprefix=laptop%2Caps%2C252&ref=nb_sb_noss_1"
    r = requests.get(url, headers=headers)
    r.raise_for_status()

    soup = BeautifulSoup(r.content, "html.parser")
    datas = soup.findAll("div", class_="a-section a-spacing-none puis-padding-right-small s-title-instructions-style")

    for data in datas:
        print(data.text)
        link = data.find("a", class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal").get("href")
        page = "https://www.amazon.in" + link
       # print(page)

        res = requests.get(page, headers=headers)
        new_soup = BeautifulSoup(res.content, "html.parser")
        title = new_soup.find("span", id="productTitle").text.strip()
        star = new_soup.find("span", class_="a-size-base a-color-base").text
        price = new_soup.find("span", class_="a-price-whole").text
        #discount = new_soup.find("span", class_="a-size-large a-color-price savingPriceOverride aok-align-center reinventPriceSavingsPercentageMargin savingsPercentage").text

        laptop = {
                'title': title,
                'star': star,
                'price': price,
            }
        print(laptop)
        database.store_laptop(laptop)


except Exception as e:
    print(e)
