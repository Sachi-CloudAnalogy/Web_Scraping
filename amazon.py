from bs4 import BeautifulSoup
import requests

try:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0 Safari/537.36'}
    url = ("https://www.amazon.in/s?k=mobile&crid=1U7INVOBPZL47&sprefix=mobile%2Caps%2C218&ref=nb_sb_noss_1")
    r = requests.get(url, headers = headers)
    r.raise_for_status()

    new_soup = BeautifulSoup(r.content, 'html.parser')
    soup = new_soup.find("span", class_="rush-component s-latency-cf-section")


    title_div = soup.findAll("div", class_="a-section a-spacing-none puis-padding-right-small s-title-instructions-style")
    # print(title.text)
    titles = []
    for i in range(len(title_div)):
        title = title_div[i].find("span", class_="a-size-medium a-color-base a-text-normal")
        titles.append(title.text)
    # for t in range(len(title)):
    #     titles.append(title[t].text)

    star_div = soup.findAll("div", class_="a-row a-size-small")
    # print(star.text)
    stars = []
    for i in range(len(star_div)):
        star = star_div[i].find("span")
        stars.append(star.text)
    # for t in range(len(star)):
    #     stars.append(star[t].text)

    price = soup.findAll("span", class_="a-offscreen")
    # print(price.text)
    prices = []
    for t in range(len(price)):
        prices.append(price[t].text)


    data_tuples = list(zip(titles[1:], stars[1:], prices[1:]))
    for data in data_tuples:
        print(data)


except Exception as e:
    print(e)

