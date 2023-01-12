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


    """Time calculation"""
    finish_time = time.time() - start_time
    print(f"Total time is {round(finish_time, 2)}")


anime_count = int(input('How many anime you want to process (round up to multiples of 50): '))
get_data(anime_count)
