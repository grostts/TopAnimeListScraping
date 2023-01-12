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



    """Time calculation"""
    finish_time = time.time() - start_time
    print(f"Total time is {round(finish_time, 2)}")


anime_count = int(input('How many anime you want to process (round up to multiples of 50): '))
get_data(anime_count)