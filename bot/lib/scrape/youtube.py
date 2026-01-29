import httpx
import random
import string
import asyncio

class YTDownloader:
    def __init__(self, timeout: int = 30):
        self.url = {
            "audio128": "https://api.apiapi.lat",
            "video": "https://api5.apiapi.lat",
            "else": "https://api3.apiapi.lat",
            "referrer": "https://ogmp3.pro/"
        }
        self.timeout = timeout

    def enc_url(self, s: str) -> str:
        return ";".join(str(ord(c)) for c in reversed(s))

    def xor(self, s: str) -> str:
        return "".join(chr(ord(c) ^ 1) for c in s)

    def gen_random_hex(self, length: int = 32) -> str:
        return "".join(random.choice("0123456789abcdef") for _ in range(length))

    async def init(self, client: httpx.AsyncClient, rp_obj: dict) -> dict:
        api_origin, payload = rp_obj["apiOrigin"], rp_obj["payload"]
        api = f"{api_origin}/{self.gen_random_hex()}/init/{self.enc_url(self.xor(payload['data']))}/{self.gen_random_hex()}/"
        r = await client.post(api, json=payload, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def gen_file_url(self, i: str, pk: str, rp_obj: dict) -> dict:
        api_origin = rp_obj["apiOrigin"]
        pk_value = f"{pk}/" if pk else ""
        download_url = f"{api_origin}/{self.gen_random_hex()}/download/{i}/{self.gen_random_hex()}/{pk_value}"
        return {"downloadUrl": download_url}

    async def status_check(self, client: httpx.AsyncClient, i: str, pk: str, rp_obj: dict) -> dict:
        api_origin = rp_obj["apiOrigin"]
        count = 0
        json_resp = None
        while True:
            await asyncio.sleep(5)
            count += 1
            pk_val = f"{pk}/" if pk else ""
            api = f"{api_origin}/{self.gen_random_hex()}/status/{i}/{self.gen_random_hex()}/{pk_val}"
            r = await client.post(api, json={"data": i}, headers={"Content-Type": "application/json"}, timeout=self.timeout)
            r.raise_for_status()
            json_resp = r.json()
            if count >= 100:
                raise Exception("pooling mencapai 100, dihentikan")
            if json_resp.get("s") != "P":
                break
        if json_resp.get("s") == "E":
            raise Exception(str(json_resp))
        return self.gen_file_url(i, pk, rp_obj)

    def resolve_payload(self, yt_url: str, user_format: str) -> dict:
        valid = ["64k","96k","128k","192k","256k","320k","240p","360p","480p","720p","1080p"]
        if user_format not in valid:
            raise Exception(f"format salah. tersedia: {', '.join(valid)}")

        api_origin = self.url["audio128"]
        data = self.xor(yt_url)
        referer = self.url["referrer"]
        format_val = "0"
        mp3_quality = "128"
        mp4_quality = "720"

        if user_format.endswith("p"):
            api_origin = self.url["video"]
            format_val = "1"
            mp4_quality = user_format.replace("p", "")
        elif user_format != "128k":
            api_origin = self.url["else"]
            mp3_quality = user_format.replace("k", "")

        return {
            "apiOrigin": api_origin,
            "payload": {
                "data": data,
                "format": format_val,
                "referer": referer,
                "mp3Quality": mp3_quality,
                "mp4Quality": mp4_quality,
                "userTimeZone": "-480"
            }
        }

    async def download(self, url: str, fmt: str = "128k") -> dict:
        rp_obj = self.resolve_payload(url, fmt)
        async with httpx.AsyncClient() as client:
            init_obj = await self.init(client, rp_obj)
            i, pk, s = init_obj["i"], init_obj.get("pk"), init_obj.get("s")
            if s == "C":
                return self.gen_file_url(i, pk, rp_obj)
            return await self.status_check(client, i, pk, rp_obj)
