from ..matcher import sekai
from nonebot.adapters.onebot.v11 import Event, MessageSegment
from nonebot.params import RawCommand
from nonebot.adapters.onebot.v11.message import Message
from nonebot.exception import SkippedException, MatcherException
from ..modules.utils import SpaceRecog
from ..modules.imagemodules import Txt2Img, DeleteByURI
from ..logger import pjsklogger
from asyncio import sleep

@pjsklogger.catch(exclude=(SkippedException, MatcherException))
async def Help(event: Event,cmd = RawCommand()):
    TextList = event.get_plaintext().split(" ")
    if not SpaceRecog(event.get_plaintext(), cmd=cmd) or TextList[1] != "help":
        await sekai.skip()
    text = """
    /pj alias   # 获取歌曲的别名
    /pj bind <id>   # 绑定您的sekai id
    /pj chart <song> (ex)   # 获取谱面
    /pj (fc/ap)难度排行 <level> # 获取定数表
    /pj help    # 获取帮助
    /pj sk  # 获取当期活动信息
    /pj profile # 获取个人信息
    /pj rk  # 获取排位信息
    /pj ycx # 获取预测线
    """
    path = Txt2Img(text, withLF=True)
    await sekai.send(MessageSegment.image(path) + MessageSegment.text("项目地址：\nhttps://github.com/Curvi-Linearis/nonebot_plugin_pjsekaibot/"))
    await sleep(3)
    DeleteByURI(path)
    await sekai.finish()
