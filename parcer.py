import requests
from bs4 import BeautifulSoup
import json
import os
import time
import random

start_time = time.time()


def get_data(anime_count):
    headers = {
        "user-agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko)"
                      " Version/11.0 Mobile/15A5341f Safari/604.1"
    }

    animes_data_list = []
    iteration_count = round(anime_count / 50)
    print(f"Total iterations: #{iteration_count}")

    for item in range(0, anime_count, 50):
        url = f"https://myanimelist.net/topanime.php?limit={item}"
        req = requests.get(headers=headers, url=url)

        """Create Folders"""
        folder_name = f"data/data_{item}"
        if os.path.exists(folder_name):
            print("The folder exists")
        else:
            os.mkdir(folder_name)

        """Saving a website page for 50 animes"""
        with open(f'myanimelist_data_{item}.html', 'w', encoding='utf-8') as file:
            file.write(req.text)
        with open(f'myanimelist_data_{item}.html', 'r', encoding='utf-8') as file:
            src = file.read()

        """Get anime list from the page"""
        soup = BeautifulSoup(src, 'lxml')
        animes = soup.find_all(class_="hoverinfo_trigger fl-l ml12 mr8")
        anime_urls = []
        anime_names = []
        for anime in animes:
            anime_href = anime.get("href")
            anime_urls.append(anime_href)
            anime_names.append(anime_href.split("/")[5])

        """Saving a html page for every anime"""
        for i in range(len(anime_urls)):
            req = requests.get(headers=headers, url=anime_urls[i])
            with open(f'{folder_name}/{anime_names[i]}.html', 'w', encoding="utf-8") as file:
                file.write(req.text)
            with open(f'{folder_name}/{anime_names[i]}.html', 'r', encoding="utf-8") as file:
                src1 = file.read()
            soup = BeautifulSoup(src1, "lxml")

            """Get info for every anime"""
            anime_information = soup.find_all("div", class_="spaceit_pad")
            anime_name = soup.find("h1", class_="title-name h1_bold_none").text
            anime_themes = "No anime themes info"
            anime_genres = "No anime genres info"
            anime_episodes = "No anime episodes info"
            anime_studio = "No anime studios info"
            for el in anime_information:
                if "Genre:" in el.text or "Genres:" in el.text:
                    anime_genres = [genre.strip()[0:int(len(genre.strip()) / 2)] for genre in
                                    el.text.strip().split('\n')[1].split(',')]
                if 'Themes:' in el.text or 'Theme:' in el.text:
                    anime_themes = [genre.strip()[0:int(len(genre.strip()) / 2)] for genre in
                                    el.text.strip().split('\n')[1].split(',')]
                if 'Episodes' in el.text:
                    anime_episodes = el.text.strip().split('\n')[1].strip()
                if 'Studios:' in el.text:
                    anime_studio = el.text.strip().split('\n')[1]

            """Get raiting"""
            try:
                anime_raiting = soup.find(class_="fl-l score").text
            except Exception:
                anime_raiting = "No anime rating"

            """Get description"""
            try:
                anime_description = soup.find("tr").find("p").text
            except Exception:
                anime_description = "No anime description"
            """Get poster"""
            try:
                anime_poster = soup.find("div", class_="leftside").find('img').get("data-src")
            except Exception:
                anime_poster = "No anime poster"
            animes_data_list.append(
                {
                    "name": anime_name,
                    "genres": anime_genres,
                    "themes": anime_themes,
                    "score": anime_raiting,
                    "episodes": anime_episodes,
                    "studio": anime_studio,
                    "description": anime_description,
                    "poster": anime_poster
                }
            )
            print(f"[INFO] Processed the {anime_name} page.")


    """Time calculation"""
    finish_time = time.time() - start_time
    print(f"Total time is {round(finish_time, 2)}")


anime_count = int(input('How many anime you want to process (round up to multiples of 50): '))
get_data(anime_count)
