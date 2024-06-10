from bs4 import BeautifulSoup
import requests
import csv

proxy = "45.94.255.2:8110"

page = requests.get("https://quotes.toscrape.com/", proxies={"http": proxy, "https": proxy})
print(page.status_code)
soup = BeautifulSoup(page.text, "html.parser")
quotes = soup.findAll("span", attrs={"class": "text"})
authors = soup.findAll("small", attrs={"class": "author"})

file = open("scraped_quotes.csv", "w")
writer = csv.writer(file)
writer.writerow(["Quotes", "Authors"])

for quote, author in zip(quotes, authors):
    print(quote.text + " - " + author.text)
    writer.writerow([quote.text, author.text])

file.close()