from bs4 import BeautifulSoup
import json
import time
import asyncio
import aiohttp

animes_data_list = []
start_time = time.time()


async def get_page_data(session, anime_url):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/"
                  "*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                      "91.0.4472.106 Safari/537.36"
    }
    async with session.get(url=anime_url, headers=headers) as response:
        response_text = await response.text()

        soup = BeautifulSoup(response_text, 'lxml')

        """Get info for every anime"""
        anime_information = soup.find_all("div", class_="spaceit_pad")
        anime_name = soup.find("h1", class_="title-name h1_bold_none").text
        anime_themes = "No anime themes info"
        anime_genres = "No anime genres info"
        anime_episodes = "No anime episodes info"
        anime_studio = "No anime studios info"
        for el in anime_information:
            if "Genre:" in el.text or "Genres:" in el.text:
                anime_genres = [genre.strip()[0:int(len(genre.strip()) / 2)]
                                for genre in el.text.strip().split('\n')[1].split(',')]
            if 'Themes:' in el.text or 'Theme:' in el.text:
                anime_themes = [genre.strip()[0:int(len(genre.strip()) / 2)]
                                for genre in el.text.strip().split('\n')[1].split(',')]
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


async def gather_data(items):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/"
                  "*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                      "91.0.4472.106 Safari/537.36"
    }
    url = f"https://myanimelist.net/topanime.php?limit={items}"

    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await response.text(), "lxml")

        animes = soup.find_all(class_="hoverinfo_trigger fl-l ml12 mr8")
        anime_urls = []
        anime_names = []
        for anime in animes:
            anime_href = anime.get("href")
            anime_urls.append(anime_href)
            anime_names.append(anime_href.split("/")[5])

        tasks = []

        for anime_url, anime_name in zip(anime_urls, anime_names):
            task = asyncio.create_task(get_page_data(session, anime_url))
            tasks.append(task)
        await asyncio.gather(*tasks)


def main(anime_count):
    for items in range(0, anime_count, 50):
        asyncio.run(gather_data(items))
        print(f'Processed {items+50} anime.')
    print(len(animes_data_list))

    with open(f"anime_data.json", "w", encoding="utf-8") as file:
        json.dump(animes_data_list, file, indent=4, ensure_ascii=False)

    finish_time = time.time() - start_time
    print(f"Total time is {round(finish_time, 2)}")


anime_count = int(input('How many anime you want to process (round up to multiples of 50): '))
main(anime_count)