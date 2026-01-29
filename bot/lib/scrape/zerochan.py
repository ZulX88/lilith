import requests
from bs4 import BeautifulSoup


def zerochan(query, limit=5):
    image_urls = []
    headers = {"User-Agent": "axios/1.9.0"}

    try:
        response = requests.get(f"https://www.zerochan.net/{query}", headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        thumbs_ul = soup.find("ul", id="thumbs2")

        if thumbs_ul:
            for link in thumbs_ul.find_all("a", href=True):
                if link["href"].startswith("https://static.zerochan.net"):
                    image_urls.append(link["href"])
                    if len(image_urls) >= limit:
                        break

    except Exception as e:
        print("Error:", e)

    return image_urls
