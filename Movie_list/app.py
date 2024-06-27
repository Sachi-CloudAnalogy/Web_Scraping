from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

def scrape_imdb_top_250():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'}

        URL = "https://www.imdb.com/chart/top/"
        resp = requests.get(URL, headers=headers)
        resp.raise_for_status()

        list_of_movies = []
        soup = BeautifulSoup(resp.text, "html.parser")

        # Find the table containing the list of top 250 movies
        movie_table = soup.find("ul", class_="ipc-metadata-list ipc-metadata-list--dividers-between sc-a1e81754-0 eBRbsI compact-list-view ipc-metadata-list--base")

        movie_rows = movie_table.find_all("div", class_="sc-b189961a-0 hBZnfJ cli-children")

        for movie in movie_rows:
            dict_of_movies = {}

            rank = movie.find("div", class_="ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-b189961a-9 iALATN cli-title").a.text.split(".")[0]
            title = movie.find("div", class_="ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-b189961a-9 iALATN cli-title").a.text.split(".")[1]

            desc = movie.find("div", class_="sc-b189961a-7 feoqjK cli-title-metadata").find_all("span")
            time = []
            for span in desc:
                data = span.text
                time.append(data)

            year = time[0]
            duration = time[1]

            rate = movie.find("span", class_="ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating")

            rating = (rate.text.split("(")[0]).replace("\xa0", "")
            views = (rate.text.split("(")[1]).replace(")", "")

            dict_of_movies = {'Rank': rank, 'Title': title, 'Year of release': year,
                              'Duration': duration, 'Rating': rating, 'Views': views}
            list_of_movies.append(dict_of_movies)

        return list_of_movies

    except Exception as e:
        print(e)

@app.route('/')
def index():
    start_time = time.time()
    list_of_movies = scrape_imdb_top_250()
    end_time = time.time()
    duration = end_time - start_time
    return render_template('index.html', movies=list_of_movies, duration=duration)

if __name__ == '__main__':
    app.run(debug=True)
