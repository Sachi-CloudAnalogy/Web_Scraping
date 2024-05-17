from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

options = Options()

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

element_list = []

for page in range(1, 3):
    page_url = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops?page=" + str(page)
    driver.get(page_url)
    titles = driver.find_elements(By.CLASS_NAME, "title")
    prices = driver.find_elements(By.CLASS_NAME, "price")
    descriptions = driver.find_elements(By.CLASS_NAME, "description")
    ratings = driver.find_elements(By.CLASS_NAME, "ratings")


    for title, price, description, rating in zip(titles, prices, descriptions, ratings):
        element_list.append([title.text, price.text, description.text, rating.text])

print(element_list)

