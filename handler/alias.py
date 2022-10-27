from ..matcher import sekai
from nonebot.params import CommandArg, ArgPlainText , RawCommand
from nonebot.adapters.onebot.v11 import Event, MessageSegment
from nonebot.adapters.onebot.v11.message import Message
from nonebot.exception import MatcherException, SkippedException
from nonebot.matcher import Matcher
from ..modules.utils import Get_response, Get_song_id, SpaceRecog, ReadConfig
from ..modules.imagemodules import Txt2Img, DeleteByURI
from ..logger import pjsklogger
from asyncio import sleep

@pjsklogger.catch(exclude=(SkippedException, MatcherException))
async def Get_alias(matcher: Matcher,event: Event, cmd = RawCommand()):
    TextList = event.get_plaintext().split(" ")
    if (not SpaceRecog(event.get_plaintext(),cmd = cmd)) or (TextList[1] not in ["alias","别称"]):
        matcher.set_arg("name",Message(""))
        await sekai.skip()
    try:
        pjsklogger.debug("Calling func Get_alias, arg:[\"{}\"]".format(event.get_plaintext()[10:]))
        matcher.set_arg("name",Message(event.get_plaintext()[10:]))
        pjsklogger.success("Get_alias Success.")
    except:
        pjsklogger.warning("Get_alias failed, arg:[\"{}\"]".format(event.get_plaintext()[10:]))
        pass
        #await sekai.finish(Message(message))

@pjsklogger.catch(exclude=(MatcherException, SkippedException))
async def Got_alias(name: str = ArgPlainText("name")):
    if name == "":
        sekai.skip()
    pjsklogger.debug(f"Calling func Got_alias, arg: {name}")
    configJson = ReadConfig()
    if configJson["API"]["UnipjskAPI"]["jp"]["getsongid"] == "" or\
        configJson["API"]["UnipjskAPI"]["jp"]["getalias2"] == "":
        pjsklogger.error("Please check [\"API\"][\"UnipjskAPI\"][\"jp\"][\"getsongid\"] and [\"API\"][\"UnipjskAPI\"][\"jp\"][\"getalias2\"] in config.json")
        sekai.finish(configJson["MESSAGE"]["ERROR"]["NO_URL"])
    try:
        title, songId, match = await Get_song_id(name)
    except:
        await sekai.finish(Message(configJson["MESSAGE"]["ERROR"]["NO_MATCH"]))
    url = configJson["API"]["UnipjskAPI"]["jp"]["getalias2"].format(alias=songId)
    try:
        response = await Get_response(url)
    except:
        await sekai.finish(Message(configJson["MESSAGE"]["ERROR"]["SERVER_ERROR"]))
    aliasString = title
    for i in response:
        aliasString = aliasString + ", {}".format(i["alias"])
    message = configJson["MESSAGE"]["ALIAS"]["GET_ALIAS"].format(title = title, match = match) + aliasString
    path = Txt2Img(message)
    await sekai.send(Message(MessageSegment.image(path)))
    await sleep(3)
    DeleteByURI(path)
    pjsklogger.success(f"Got_alias Success, arg:[\"{title}\"].")
    await sekai.finish()
