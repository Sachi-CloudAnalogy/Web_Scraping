import requests
from bs4 import BeautifulSoup

URL = "https://www.geeksforgeeks.org/implementing-web-scraping-python-beautiful-soup/"
data = requests.get(URL)
print(data.content)
# raw HTML content

soup = BeautifulSoup(data.content, "html5lib")
print(soup.prettify())

title = soup.title
print(title)
print(type(title))
print(type(soup))
