from nonebot.plugin import require
require("nonebot_plugin_suggarchat")
from nonebot_plugin_suggarchat.on_event import on_chat
from nonebot_plugin_suggarchat.event import ChatEvent
from nonebot import logger
@on_chat().handle()
async def _(event:ChatEvent):
    logger.info("收到聊天事件!")
    logger.info(event)