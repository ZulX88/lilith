import requests

def threads_download(url): 
    api_url = "https://api.threadsphotodownloader.com/v2/media"
       
    params = {
        'url': url
    }
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract download_url from image_urls
        image_urls = []
        for item in data.get('image_urls', []):
            if isinstance(item, dict) and 'download_url' in item:
                image_urls.append(item['download_url'])
            elif isinstance(item, str):
                image_urls.append(item)
        
        # Extract download_url from video_urls
        video_urls = []
        for item in data.get('video_urls', []):
            if isinstance(item, dict) and 'download_url' in item:
                video_urls.append(item['download_url'])
            elif isinstance(item, str):
                video_urls.append(item)
        
        return {
            'image_urls': image_urls,
            'video_urls': video_urls
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading media: {e}")
        return {'image_urls': [], 'video_urls': []}
