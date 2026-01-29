import requests
from bs4 import BeautifulSoup


def fb_download(url):
    form_data = {"id": url, "locale": "id"}

    headers = {
        "HX-Request": "true",
        "HX-Trigger": "form",
        "HX-Target": "target",
        "HX-Current-URL": "https://getmyfb.com/id",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    }

    try:
        response = requests.post(
            "https://getmyfb.com/process", data=form_data, headers=headers, timeout=10
        )
        response.raise_for_status()
    except requests.RequestException as e:
        raise Exception(f"Request failed: {e}")

    # Parse the response HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the first download link in the results list
    link_element = soup.select(".results-list-item a")
    if link_element:
        download_link = link_element[0]["href"]
        return download_link
    else:
        raise Exception("Video download link not found")

