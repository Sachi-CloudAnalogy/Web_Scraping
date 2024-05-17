import requests
from bs4 import BeautifulSoup
import csv

URL = "http://www.values.com/inspirational-quotes"
res = requests.get(URL)
soup = BeautifulSoup(res.content, 'html5lib')

quotes = []
table = soup.findAll("div", attrs={'class': 'col-6 col-lg-4 text-center margin-30px-bottom sm-margin-30px-top'})
for row in table:
    quote = {}
    quote['theme'] = row.h5.text
    quote['url'] = row.a['href']
    quote['img'] = row.img['src']
    quote['lines'] = row.img['alt'].split(" #")[0]
    quote['author'] = row.img['alt'].split(" #")[1]
    quotes.append(quote)

with open("quotes.csv", "w", newline='') as f:
    w = csv.DictWriter(f, ['theme', 'url', 'img', 'lines', 'author'])
    w.writeheader()
    for quote in quotes:
        w.writerow(quote)
        print(quote)
