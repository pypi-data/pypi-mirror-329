from nonebot.plugin import require
require("nonebot_plugin_suggarchat")
from nonebot_plugin_suggarchat.on_event import on_chat,on_before_chat,on_poke,on_before_poke
from nonebot_plugin_suggarchat.event import ChatEvent,PokeEvent
from nonebot import logger
@on_poke().handle(priority_value=10)
async def _(event:PokeEvent):
    logger.info("戳了！")
    logger.info(event)
@on_before_poke().handle(priority_value=10)
async def _(event:PokeEvent):
    logger.info("现在在获取模型的回复之前！")
    logger.info(event)

@on_before_chat().handle(priority_value=10)
async def _(event:ChatEvent):
    logger.info("现在在获取模型的回复之前！")
    logger.info(event)
@on_chat().handle(priority_value=10)
async def _(event:ChatEvent):
    logger.info("收到聊天事件!")
    logger.info(event)