from selenium import webdriver

driver = webdriver.Chrome()

for year in range(1990, 2023):
    page_num = str(year) + '-' + str(year+1) + '/'
    url = "https://hoopshype.com/salaries/players/" + page_num
    driver.get(url)

    players = driver.find_elements('xpath', '//td[@class="name"]')
    players_list = []
    for p in range(len(players)):
        players_list.append(players[p].text)

    salaries = driver.find_elements('xpath', '//td[@class="hh-salaries-sorted"]')
    salaries_list = []
    for s in range(len(salaries)):
        salaries_list.append(salaries[s].text)

    data_tuples = list(zip(players_list[1:], salaries_list[1:]))
    print(data_tuples)

driver.close()