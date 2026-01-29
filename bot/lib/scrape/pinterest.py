import httpx
import asyncio
import re
import json
import time
from typing import Optional, List, Dict, Any

def is_pin(url: str) -> bool:
    if not url:
        return False
    patterns = [
        r'^https?:\/\/(?:www\.)?pinterest\.com\/pin\/[\w.-]+',
        r'^https?:\/\/(?:www\.)?pinterest\.[\w.]+\/pin\/[\w.-]+',
        r'^https?:\/\/(?:www\.)?pinterest\.(?:ca|co\.uk|com\.au|de|fr|id|es|mx|br|pt|jp|kr|nz|ru|at|be|ch|cl|dk|fi|gr|ie|nl|no|pl|pt|se|th|tr)\/pin\/[\w.-]+',
        r'^https?:\/\/pin\.it\/[\w.-]+',
        r'^https?:\/\/(?:www\.)?pinterest\.com\/amp\/pin\/[\w.-]+',
        r'^https?:\/\/(?:[a-z]{2}|www)\.pinterest\.com\/pin\/[\w.-]+',
        r'^https?:\/\/(?:www\.)?pinterest\.com\/pin\/[\d]+(?:\/)?$',
        r'^https?:\/\/(?:www\.)?pinterest\.[\w.]+\/pin\/[\d]+(?:\/)?$',
        r'^https?:\/\/(?:www\.)?pinterestcn\.com\/pin\/[\w.-]+',
        r'^https?:\/\/(?:www\.)?pinterest\.com\.[\w.]+\/pin\/[\w.-]+'
    ]
    url_lower = url.strip().lower()
    return any(re.match(pattern, url_lower) for pattern in patterns)

async def get_cookies() -> Optional[str]:
    try:
        # Pakai httpx.AsyncClient biar cookie otomatis ter-manage
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get('https://www.pinterest.com/csrf_error/')
            cookies = response.cookies
            if cookies:
                cookie_string = '; '.join(f"{k}={v}" for k, v in cookies.items())
                return cookie_string
            else:
                print('Warning: No cookies found in the response.')
                return None
    except Exception as error:
        print(f'Error fetching cookies: {error}')
        return None

async def pindl(pin_url: str) -> Optional[Dict[str, Any]]:
    try:
        cookies = await get_cookies()
        if not cookies:
            print('Failed to retrieve cookies. Exiting.')
            return None

        if not is_pin(pin_url):
            print('URL is not a valid Pinterest pin.')
            return None

        pin_id = pin_url.split('/pin/')[1].replace('/', '') if '/pin/' in pin_url else None

        if not pin_id:
            async with httpx.AsyncClient(follow_redirects=True) as client:
                response = await client.get(pin_url)
                final_url = str(response.url)
                pin_id = final_url.split('/pin/')[1].split('/')[0]

        url = 'https://www.pinterest.com/resource/PinResource/get/'
        params = {
            'source_url': f'/pin/{pin_id}/',
            'data': json.dumps({
                'options': {'field_set_key': 'detailed', 'id': pin_id},
                'context': {}
            }),
            '_': str(int(time.time() * 1000))
        }

        headers = {
            'accept': 'application/json, text/javascript, */*, q=0.01',
            'cookie': cookies,
            'referer': 'https://www.pinterest.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'x-app-version': 'a9522f',
            'x-pinterest-appstate': 'active',
            'x-pinterest-pws-handler': 'www/[username]/[slug].js',
            'x-pinterest-source-url': '/pin-resource/',
            'x-requested-with': 'XMLHttpRequest'
        }

        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url, headers=headers, params=params)
            data = response.json()

        if not data.get('resource_response', {}).get('data'):
            print('Pin not found or no longer available.')
            return None

        pd = data['resource_response']['data']
        media_urls = []

        if pd.get('videos'):
            video_formats = list(pd['videos']['video_list'].values())
            video_formats.sort(key=lambda x: x['width'], reverse=True)
            for video in video_formats:
                media_urls.append({
                    'type': 'video',
                    'quality': f"{video['width']}x{video['height']}",
                    'url': video['url'],
                    'width': video['width'],
                    'height': video['height']
                })

        if pd.get('images'):
            images = {
                'original': pd['images'].get('orig'),
                'large': pd['images'].get('736x'),
                'medium': pd['images'].get('474x'),
                'small': pd['images'].get('236x'),
                'thumbnail': pd['images'].get('170x')
            }
            for quality, image in images.items():
                if image:
                    media_urls.append({
                        'type': 'image',
                        'quality': quality,
                        'url': image['url'],
                        'width': image.get('width'),
                        'height': image.get('height')
                    })

        return {
            'id': pd['id'],
            'title': pd.get('title', ''),
            'description': pd.get('description', ''),
            'media': media_urls
        }

    except Exception as error:
        print(f'Error: {error}')
        return None

async def pinterest(query: str, limit: int = 20) -> List[Dict[str, Any]]:
    try:
        cookies = await get_cookies()
        if not cookies:
            print('Failed to retrieve cookies. Exiting.')
            return []

        url = 'https://www.pinterest.com/resource/BaseSearchResource/get/'
        params = {
            'source_url': f'/search/pins/?q={query}',
            'data': json.dumps({
                'options': {
                    'isPrefetch': False,
                    'query': query,
                    'scope': 'pins',
                    'no_fetch_context_on_resource': False,
                    'page_size': min(limit, 250)
                },
                'context': {}
            }),
            '_': str(int(time.time() * 1000))
        }

        headers = {
            'accept': 'application/json, text/javascript, */*, q=0.01',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': cookies,
            'dnt': '1',
            'referer': 'https://www.pinterest.com/',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
            'sec-ch-ua-full-version-list': '"Not(A:Brand";v="99.0.0.0", "Microsoft Edge";v="133.0.3065.92", "Chromium";v="133.0.6943.142"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"10.0.0"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0',
            'x-app-version': 'c056fb7',
            'x-pinterest-appstate': 'active',
            'x-pinterest-pws-handler': 'www/[username]/[slug].js',
            'x-pinterest-source-url': '/hargr003/cat-pictures/',
            'x-requested-with': 'XMLHttpRequest'
        }

        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url, headers=headers, params=params)
            data = response.json()

        container = []
        results = data['resource_response']['data']['results']
        filtered_results = [r for r in results if r.get('images', {}).get('orig')]
        
        limited_results = filtered_results[:limit]
        
        for result in limited_results:
            container.append({
                'upload_by': result['pinner']['username'],
                'fullname': result['pinner']['full_name'],
                'followers': result['pinner']['follower_count'],
                'caption': result['grid_title'],
                'image': result['images']['orig']['url'],
                'source': f"https://id.pinterest.com/pin/{result['id']}",
            })

        return container

    except Exception as error:
        print(f'Error: {error}')
        return []
