import aiohttp
import json
import re
from typing import Dict, Any, List
from bs4 import BeautifulSoup
from framework.logger import get_logger

logger = get_logger("MusicSearcher")

class MusicSearcher:
    async def _play_music(self, params: Dict[str, Any]) -> Dict[str, Any]:
        music_name = params.get("music_name")
        singer = params.get("singer", "")
        source = params.get("source", "")

        if not music_name:
            return {
                "music_url": "",
                "lyrics": "搜索音乐名称为空"
            }

        # Clean input
        if singer:
            singer = re.sub(r'\u2066|\u2067|\u2068|\u2069', '', singer)
        music_name = re.sub(r'\u2066|\u2067|\u2068|\u2069', '', music_name)

        result = await self._get_music(music_name, singer, source, True)
        return result

    async def _get_music(self, music_name: str, singer: str, source: str, repeat: bool) -> Dict[str, Any]:
        download_link = "未找到匹配的音乐"

        if not source or source != "酷美":
            types = ["netease", "qq", "kugou", "migu"]
            source_dict = {"网易": "netease", "qq": "qq", "酷狗": "kugou", "咪咕": "migu"}
            if source in source_dict:
                types.insert(0, source_dict[source])
            result = await self._search_music(music_name, singer, types)
            if result:
                music_url = result.get("url")
                lyrics = self._clean_lrc(result.get("lrc"))
                return {"music_url": music_url, "lyrics": lyrics}

        file_id = await self._get_file_id(music_name, singer)
        if file_id:
            download_link = await self._get_download_link(file_id)
            async with aiohttp.ClientSession() as session:
                async with session.get(download_link, allow_redirects=False) as response:
                    if response.status == 302:
                        lyrics = await self._get_lyrics(music_name, singer)
                        lyrics = lyrics if lyrics else "未找到歌词"
                        return {"music_url": download_link, "lyrics": lyrics}
        elif repeat:
            return await self._get_music(music_name, "", source, False)

        lyrics = await self._get_lyrics(music_name, singer)
        lyrics = lyrics if lyrics else "未找到歌词"
        return {"music_url": download_link, "lyrics": lyrics}

    @staticmethod
    def _clean_lrc(lrc_string: str) -> str:
        if not lrc_string:
            return lrc_string

        time_pattern = r'\[\d{2}:\d{2}.\d{2}\]'
        metadata_pattern = r'\[(ti|ar|al|by|offset):.+?\]'

        lines = lrc_string.split('\n')
        cleaned_lines = []

        for line in lines:
            line = re.sub(time_pattern, '', line)
            line = re.sub(metadata_pattern, '', line)
            if line.strip():
                cleaned_lines.append(line.strip())

        return '\n'.join(cleaned_lines).replace("[al:]", "").replace("[by:]", "").lstrip()

    async def _search_music(self, music_name: str, singer: str, types: List[str]) -> Dict[str, Any]:
        keyword = f"{music_name} {singer}" if singer else music_name

        if not types:
            return None

        current_type = types[0]
        url = "https://music.txqq.pro/"
        data = {
            "input": keyword,
            "filter": "name",
            "type": current_type,
            "page": 1
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=data, headers={"X-Requested-With": "XMLHttpRequest"}) as response:
                    response.raise_for_status()
                    text = await response.text()
                    json_data = json.loads(text)
                    if json_data.get("code") == 200 and json_data.get("data"):
                        for item in json_data.get("data"):
                            if item["url"]:
                                try:
                                    async with session.head(item["url"], allow_redirects=True) as resp:
                                        content_type = resp.headers.get('Content-Type', '').lower()

                                        if (music_name not in item["title"] or
                                            "钢琴版" in item["title"] or
                                            "伴奏" in item["title"]):
                                            continue

                                        if (singer and singer != "BoaT" and
                                            singer not in item["author"]):
                                            continue

                                        if ('audio' in content_type or 'mp3' in content_type):
                                            return item

                                except Exception as e:
                                    logger.error(f"Request failed: {e}")

        except Exception as e:
            logger.error(f"Error searching music: {e}")

        return await self._search_music(music_name, singer, types[1:])

    async def _get_lyrics(self, music_name: str, singer: str) -> str:
        keyword = f"{singer} {music_name}" if singer else music_name
        search_url = f"https://www.autolyric.com/zh-hans/lyrics-search?kw={keyword}"

        async with aiohttp.ClientSession() as session:
            async with session.get(search_url) as response:
                text = await response.text()
                soup = BeautifulSoup(text, 'html.parser')

                lyric_link = None
                for tr in soup.find_all('tr'):
                    a_tag = tr.find('a', href=True)
                    if a_tag:
                        lyric_link = a_tag['href']
                        break

                if not lyric_link:
                    return "未找到歌词"

                lyric_url = f"https://www.autolyric.com{lyric_link}"
                async with session.get(lyric_url) as response:
                    text = await response.text()
                    soup = BeautifulSoup(text, 'html.parser')

                    pane_contents = soup.find_all('div', class_='pane-content')
                    if len(pane_contents) < 2:
                        return "无法获取歌词内容"

                    lyrics_div = pane_contents[1]
                    lyrics = []
                    for br in lyrics_div.find_all('br'):
                        line = br.previous_sibling
                        if isinstance(line, str):
                            lyrics.append(line.strip())

                    return '\n'.join(lyrics)

    async def _get_file_id(self, music_name: str, singer: str) -> str:
        """获取酷美音乐的文件ID"""
        keyword = f"{singer} {music_name}" if singer else music_name
        url = f"https://www.kumeiwp.com/index/search/data?page=1&limit=50&word={keyword}&scope=all"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()

                if 'data' not in data:
                    return None

                max_file_downs = 0
                max_file_id = None

                for item in data['data']:
                    if item['file_downs'] > max_file_downs:
                        max_file_downs = item['file_downs']
                        max_file_id = item['file_id']

                return max_file_id

    async def _get_download_link(self, file_id: str) -> str:
        """获取酷美音乐的下载链接"""
        url = f"https://www.kumeiwp.com/file/{file_id}.html"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                text = await response.text()
                soup = BeautifulSoup(text, 'html.parser')

                for a in soup.find_all('a', href=True):
                    if '本地下载' in a.get('title', ''):
                        return a['href']

                return None
