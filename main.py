import random
import asyncio
import os
import json
import datetime
import aiohttp
import urllib.parse
import logging
from PIL import Image as PILImage
from PIL import ImageDraw as PILImageDraw
from PIL import ImageFont as PILImageFont
from astrbot.api.all import AstrMessageEvent, CommandResult, Context, Image, Plain
import astrbot.api.event.filter as filter
from astrbot.api.star import register, Star

logger = logging.getLogger("astrbot")


@register("astrbot_plugin_essential", "Soulter", "", "", "")
class Main(Star):
    def __init__(self, context: Context) -> None:
        super().__init__(context)
        self.PLUGIN_NAME = "astrbot_plugin_essential"
        PLUGIN_NAME = self.PLUGIN_NAME
        path = os.path.abspath(os.path.dirname(__file__))
        self.mc_html_tmpl = open(
            path + "/templates/mcs.html", "r", encoding="utf-8"
        ).read()
        self.what_to_eat_data: list = json.loads(
            open(path + "/resources/food.json", "r", encoding="utf-8").read()
        )["data"]

        if not os.path.exists(f"data/{PLUGIN_NAME}_data.json"):
            with open(f"data/{PLUGIN_NAME}_data.json", "w", encoding="utf-8") as f:
                f.write(json.dumps({}, ensure_ascii=False, indent=2))
        with open(f"data/{PLUGIN_NAME}_data.json", "r", encoding="utf-8") as f:
            self.data = json.loads(f.read())
        self.good_morning_data = self.data.get("good_morning", {})

        # moe
        self.moe_urls = [
            "https://t.mwm.moe/pc/",
            "https://t.mwm.moe/mp",
            "https://www.loliapi.com/acg/",
            "https://www.loliapi.com/acg/pc/",
        ]

        self.search_anmime_demand_users = {}

    def time_convert(self, t):
        m, s = divmod(t, 60)
        return f"{int(m)}分{int(s)}秒"

    @filter.command("一言")
    async def hitokoto(self, message: AstrMessageEvent):
        """来一条一言"""
        url = "https://yiyan.chgr.cc"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return CommandResult().error("请求失败")
                data = await resp.json()
        return CommandResult().message(data["hitokoto"] + " —— " + data["from"])

    async def save_what_eat_data(self):
        path = os.path.abspath(os.path.dirname(__file__))
        with open(path + "/resources/food.json", "w", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    {"data": self.what_to_eat_data}, ensure_ascii=False, indent=2
                )
            )
