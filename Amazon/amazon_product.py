from bs4 import BeautifulSoup
import requests

try:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0 Safari/537.36'}
    for i in range(1, 6):
        url = ("https://www.amazon.in/s?k=mobile&page=") + str(i)
        r = requests.get(url, headers = headers)
        r.raise_for_status()

        new_soup = BeautifulSoup(r.content, 'html.parser')
        soup = new_soup.find("span", class_="rush-component s-latency-cf-section")


        title_div = soup.findAll("div", class_="a-section a-spacing-none puis-padding-right-small s-title-instructions-style")
        star_div = soup.findAll("div", class_="a-row a-size-small")
        price = soup.findAll("span", class_="a-offscreen")

        list_of_products = []

        for i in range(len(title_div)):
            product = {}
            title = title_div[i].find("span", class_="a-size-medium a-color-base a-text-normal")
            star = star_div[i].find("span")
            product['title'] = title.text
            product['star'] = star.text
            product['price'] = price[i].text
            list_of_products.append(product)

        for products in list_of_products:
            print(products)



except Exception as e:
    print(e)

