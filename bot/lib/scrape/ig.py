import requests
import re

def instagram_download(instagram_url):
    api_url = 'https://ssvid.net/api/ajax/search?hl=en'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36'
    }
    
    data = {'query': instagram_url}
    response = requests.post(api_url, headers=headers, data=data)
    json_data = response.json()

    # Handle gallery (multiple images)
    if 'gallery' in json_data['data'] and 'items' in json_data['data']['gallery']:
        urls = []
        for item in json_data['data']['gallery']['items']:
            highest_res = max(item['resources'], key=lambda x: int(x['fsize'].split('x')[0]))
            urls.append(highest_res['src'])
        return {
            'type': 'gallery',
            'urls': urls
        }

    # Handle single image
    if 'video' in json_data['data']['links']:
        for quality, info in json_data['data']['links']['video'].items():
            if 'image' in quality.lower():
                return {
                    'type': 'image',
                    'url': info['url']
                }

    # Handle video
    if 'video' in json_data['data']['links']:
        for quality, info in json_data['data']['links']['video'].items():
            if 'hd' in quality.lower():
                return {
                    'type': 'video',
                    'url': info['url']
                }
        # fallback to first available video
        first_video = list(json_data['data']['links']['video'].values())[0]['url']
        return {
            'type': 'video',
            'url': first_video
        }

    raise Exception('No downloadable media found')