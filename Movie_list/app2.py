import time
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify

app = Flask(__name__)

async def fetch(session, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
    async with session.get(url, headers=headers) as response:
        response.raise_for_status()
        return await response.text()

async def scrape_imdb_top_250():
    url = "https://www.imdb.com/chart/top/"
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        soup = BeautifulSoup(html, "html.parser")

        list_of_movies = []

        # Find the table containing the list of top 250 movies
        movie_table =soup.find("ul",
                  class_="ipc-metadata-list ipc-metadata-list--dividers-between sc-a1e81754-0 eBRbsI compact-list-view ipc-metadata-list--base")

        movie_rows = movie_table.find_all("div", class_="sc-b189961a-0 hBZnfJ cli-children")

        for movie in movie_rows:
            dict_of_movies = {}

            rank = movie.find("div",
                              class_="ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-b189961a-9 iALATN cli-title").a.text.split(
                ".")[0]
            title = movie.find("div",
                               class_="ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-b189961a-9 iALATN cli-title").a.text.split(
                ".")[1]

            desc = movie.find("div", class_="sc-b189961a-7 feoqjK cli-title-metadata").find_all("span")
            time = []
            for span in desc:
                data = span.text
                time.append(data)

            year = time[0]
            duration = time[1]

            rate = movie.find("span",
                              class_="ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating")

            rating = (rate.text.split("(")[0]).replace("\xa0", "")
            views = (rate.text.split("(")[1]).replace(")", "")

            dict_of_movies = {'Rank': rank, 'Title': title, 'Year of release': year,
                              'Duration': duration, 'rating': rating, 'views': views}

            list_of_movies.append(dict_of_movies)

        return list_of_movies


@app.route('/')
async def index():
    list_of_movies = await scrape_imdb_top_250()
    return render_template('index.html', movies=list_of_movies)

@app.route('/api/movies')
async def api_movies():
    list_of_movies = await scrape_imdb_top_250()
    return jsonify(list_of_movies)

if __name__ == '__main__':
    app.run(debug=True)
