from ..matcher import sekai
from nonebot.adapters.onebot.v11 import MessageSegment, Event
from nonebot.adapters.onebot.v11.message import Message
from nonebot.params import RawCommand
from nonebot.exception import MatcherException, SkippedException
from ..modules.utils import SpaceRecog, ReadConfig
from ..modules.imagemodules import Txt2Img, DeleteByURI
from ..logger import pjsklogger
from pathlib import Path
from asyncio import sleep
import json, time

@pjsklogger.catch(exclude=(MatcherException, SkippedException))
async def Get_ycx(event: Event,cmd = RawCommand()):
    TextList = event.get_plaintext().split(" ")
    if not SpaceRecog(event.get_plaintext(), cmd = cmd) or (TextList[1] not in ['ycx','预测线']):
        await sekai.skip()
    configJson = ReadConfig()
    ycxPath = Path(".") / "data" / "ProjectSekai" / "masterdb" / "ycx.json"
    if not ycxPath.exists():
        pjsklogger.error("ycx.json doesn't exist. Have you done update?")
        await sekai.finish(configJson["MESSAGE"]["ERROR"]["NO_URL"])
    with open(ycxPath.as_posix(), "r") as f:
        preLine = json.load(f)
    if preLine["status"] != "success":
        pjsklogger.error("ycx.json has some error. Please manually update or wait for next update.")
        await sekai.finish(Message(configJson["MESSAGE"]["ERROR"]["SERVER_ERROR"]))
    event_id = str(preLine['data']['eventId'])
    updatetime = time.localtime(ycxPath.stat().st_mtime)
    lines = ['1','2','3','10','20','30','40','50','100','200','300','400','500','1000','2000','3000','4000','5000','10000','20000','30000','40000','50000','100000']
    try:    # ycx of rank
        rank = TextList[2]
        if int(rank) < 100:
            await sekai.finish(Message(configJson["MESSAGE"]["YCX"]["BEFORE_100"]))
        if(rank in lines):
            text = configJson["MESSAGE"]["YCX"]["EVENT"].format(event_id = event_id, eventName = preLine['data']['eventName'])
            text = text + configJson["MESSAGE"]["YCX"]["POINT"].format(rankPoint = preLine['data'][rank], rank = rank)
            text = text + "数据来源：33-Kit.\nUpdated in " + time.strftime("%Y-%m-%d %H:%M:%S", updatetime)
            path = Txt2Img(text, withLF=True)
            await sekai.send(Message(MessageSegment.image(path)))
            await sleep(3)
            DeleteByURI(path)
            await sekai.finish()
        else:
            await sekai.finish(configJson["MESSAGE"]["YCX"]["NOT_LINE"])
    except IndexError: # full ycx
        text = configJson["MESSAGE"]["YCX"]["EVENT"].format(event_id = event_id, eventName = preLine['data']['eventName'])
        for i in preLine["data"]:
            if i not in lines:
                continue
            text = text + configJson["MESSAGE"]["YCX"]["POINT"].format(rankPoint = preLine['data'][i], rank = i)
        text = text + "数据来源：33-Kit.\nUpdated in " + time.strftime("%Y-%m-%d %H:%M:%S", updatetime)
        path = Txt2Img(text, withLF=True)
        await sekai.send(Message(MessageSegment.image(path)))
        await sleep(3)
        DeleteByURI(path)
        await sekai.finish()
