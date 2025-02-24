import requests
import re
import base64
import orjson
import sys
from bs4 import BeautifulSoup
from typing import Tuple

class Discord:
    _token = None

    @classmethod
    def _get_meta_ver(cls) -> int:
        try:
            meta_url = "https://updates.discord.com/distributions/app/manifests/latest"
            meta_params = {"channel": "stable", "platform": "win", "arch": "x86"}
            meta_headers = {"User-Agent": "Discord-Updater/1"}
            
            meta_data = requests.get(meta_url, params=meta_params, headers=meta_headers)
            return int(meta_data.json()["metadata_version"])
        except:
            return 0

    @classmethod
    def _get_stable_ver(cls) -> str:
        try:
            stable_url = f"https://discord.com/api/downloads/distributions/app/installers/latest"
            stable_params = {"platform": "win", "arch": "x86"}
            
            stable_data = requests.get(stable_url, params=stable_params, allow_redirects=False)
            return re.search(r"x86/(.*?)/", stable_data.text).group(1)
        except:
            return "0"

    @classmethod
    def get_build_number(cls) -> int:
        try:
            login_data = requests.get("https://discord.com/login")
            js_pattern = r'<script\s+src="([^"]+\.js)"\s+defer>\s*</script>'
            js_files = re.findall(js_pattern, login_data.text)
            
            for js_path in js_files:
                js_url = f"https://discord.com{js_path}"
                js_content = requests.get(js_url)
                
                if "buildNumber" in js_content.text:
                    build_num = js_content.text.split('build_number:"')[1].split('"')[0]
                    return int(build_num)
            
            return build_num
        except Exception:
            return 358711
    
    @classmethod
    def get_native_ver(cls) -> int:
        response = requests.get(
            "https://updates.discord.com/distributions/app/manifests/latest",
            params={
                "install_id": "0",
                "channel": "stable", 
                "platform": "win",
                "arch": "x86",
            },
            headers={
                "user-agent": "Discord-Updater/1",
                "accept-encoding": "gzip",
            },
            timeout=10,
        ).json()
        
        return int(response["metadata_version"])    
    
    @classmethod
    def get_main_version(cls) -> str:
        response = requests.get(
            "https://discord.com/api/downloads/distributions/app/installers/latest",
            params={
                "channel": "stable",
                "platform": "win",
                "arch": "x86",
            },
            allow_redirects=False,
            timeout=10,
        ).text
        return re.search(r"x86/(.*?)/", response).group(1)

    @classmethod
    def _get_versions(cls) -> Tuple[int, str, int]:
        return (
            cls.get_build_number(),
            cls._get_stable_ver(),
            cls._get_meta_ver()
        )

    @classmethod
    def get_x_super_properties(cls) -> str:
        agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
        build, stable, meta = cls._get_versions()
        browser_ver = re.search(r"Chrome/(\d+\.[\d.]+)", agent).group(1)
        
        props = {
            "os": "Windows",
            "browser": "Chrome",
            "device": "",
            "system_locale": "en-US",
            "browser_user_agent": agent,
            "browser_version": browser_ver,
            "os_version": "10",
            "referrer": "",
            "referring_domain": "",
            "referrer_current": f"https://discord.com/",
            "referring_domain_current": "discord.com",
            "release_channel": "stable",
            "client_build_number": build,
            "native_build_number": meta,
            "client_event_source": None
        }
        
        return base64.b64encode(orjson.dumps(props)).decode()
    
    @classmethod
    def _fetch_cookies(cls) -> dict:
        try:
            response = requests.get('https://discord.com')
            return {cookie.name: cookie.value for cookie in response.cookies 
                if cookie.name.startswith('__') and cookie.name.endswith('uid')}
        except:
            return {}


    @classmethod
    def _fetch_session_id(cls, token: str) -> str:
        import websocket
        import json
        
        ws = websocket.WebSocket()
        try:
            ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
            recv = json.loads(ws.recv())
            
            ws.send(json.dumps({
                "op": 2,
                "d": {
                    "token": token,
                    "properties": {
                        "$os": "Windows"
                    },
                },
            }))
            
            r = json.loads(ws.recv())
            
            if r.get("t") == "READY":
                return r["d"]["session_id"]
            if r.get("op") == 9:
                return "Invalid Token"
            if r.get("op") == 429:
                return "429"
            return "Unknown Error"
            
        except websocket.WebSocketException as e:
            return f"ws error -> {e}"
        except json.JSONDecodeError as e:
            return f"json error -> {e}"
