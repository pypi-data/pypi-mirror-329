from typing import Any, Dict, List, Optional, Annotated
from framework.workflow.core.block import Block
from framework.workflow.core.block.input_output import Input, Output
from framework.im.message import IMMessage, TextMessage, VoiceMessage
from framework.im.sender import ChatSender
from .music_searcher import MusicSearcher
import asyncio
from framework.logger import get_logger
from framework.ioc.container import DependencyContainer

logger = get_logger("MusicSearch")

class MusicSearchBlock(Block):
    """音乐搜索Block"""
    name = "music_search"

    inputs = {
        "music_name": Input(name="music_name", label="歌曲名", data_type=str, description="歌曲名称"),
        "singer": Input(name="singer", label="歌手", data_type=str, description="歌手名称", nullable=True, default=""),
    }

    outputs = {
        "music_url": Output(name="music_url", label="音乐URL", data_type=str, description="音乐URL"),
        "lyrics": Output(name="lyrics", label="歌词", data_type=str, description="歌词")
    }

    def __init__(self, source: str = None):
        super().__init__()
        self.searcher = MusicSearcher()
        self.source = source

    def execute(self, **kwargs) -> Dict[str, Any]:
        music_name = kwargs.get("music_name", "")
        singer = kwargs.get("singer", "")
        source = self.source

        try:
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            result = loop.run_until_complete(
                self.searcher._play_music({
                    "music_name": music_name,
                    "singer": singer,
                    "source": source
                })
            )
            return {
                "music_url": result["music_url"],
                "lyrics": result["lyrics"]
            }
        except Exception as e:
            return {
                "music_url": "",
                "lyrics": f"搜索失败: {str(e)}"
            }

class MusicUrlToIMMessage(Block):
    """音乐URL转IMMessage"""
    name = "music_url_to_im_message"
    container: DependencyContainer
    inputs = {
        "music_url": Input("music_url", "音乐URL", str, "音乐URL"),
        "lyrics": Input("lyrics", "歌词", str, "歌词")
    }
    outputs = {"msg": Output("msg", "IM消息", IMMessage, "IM消息")}
    def __init__(self):
        self.split_by = ","
    def execute(self, music_url: str, lyrics: str) -> Dict[str, Any]:
        message_elements = []
        if music_url and music_url.startswith("http"):
            message_elements.append(VoiceMessage(music_url))
        if lyrics:
            message_elements.append(TextMessage(f"歌词:\n{lyrics}"))
        
        return {"msg": IMMessage(sender=ChatSender.get_bot_sender(), message_elements=message_elements)}
