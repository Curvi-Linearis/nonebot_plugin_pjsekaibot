from ..matcher import sekaiadmin
from nonebot.adapters.onebot.v11 import Event, MessageSegment
from nonebot.adapters.onebot.v11.message import Message
from nonebot.exception import ActionFailed, MatcherException, SkippedException
from nonebot.params import RawCommand
from ..logger import pjsklogger
from ..modules.init import CreatePath, CreateDatabase, CreateURLjson
from ..modules.imagemodules import Txt2Img, DeleteByURI
from ..modules.utils import SpaceRecog
from asyncio import sleep
from pathlib import Path

@pjsklogger.catch(exclude = (MatcherException, SkippedException))
async def Init1(event: Event, cmd = RawCommand()):
    TextList = event.get_plaintext().split(" ")
    if not SpaceRecog(event.get_plaintext(), cmd = cmd) or TextList[1] != "init1":
        await sekaiadmin.skip()
    pjsklogger.debug("Calling func Init1.")
    CreatePath()
    CreateDatabase()
    CreateURLjson()
    path = Txt2Img("Init1:\n Finished.")
    try:
        await sekaiadmin.send(Message(MessageSegment(type="Image", data={"file": path})))
    except ActionFailed:
        await sekaiadmin.send(Message(MessageSegment.image(path)))
    await sleep(3)
    DeleteByURI(path)
    pjsklogger.success("Init1 Success.")
    await sekaiadmin.finish()

@pjsklogger.catch(exclude = (MatcherException, SkippedException))
async def Init2(event: Event, cmd = RawCommand()):
    TextList = event.get_plaintext().split(" ")
    if not SpaceRecog(event.get_plaintext(), cmd = cmd) or TextList[1] != "update":
        await sekaiadmin.skip()
    pjsklogger.debug("Calling func Init2.")
    from ..modules.downloader import Run_every_30_min, Run_every_1_day
    await Run_every_30_min()
    await Run_every_1_day()
    path = Txt2Img("Update:\n Success.")
    try:
        await sekaiadmin.send(Message(MessageSegment(type="Image", data={"file": path})))
    except ActionFailed:
        await sekaiadmin.send(Message(MessageSegment.image(path)))
    await sleep(3)
    DeleteByURI(path)
    pjsklogger.success("Init2 Success.")
    await sekaiadmin.finish()
