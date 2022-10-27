from ..matcher import sekai, twsekai, ensekai
from nonebot.params import RawCommand
from nonebot.exception import MatcherException, SkippedException
from nonebot.adapters.onebot.v11 import Event, MessageSegment
from nonebot.adapters.onebot.v11.message import Message
from ..modules.utils import Fetch_id, SpaceRecog, ReadConfig
from ..modules.imagemodules import Txt2Img, DeleteByURI
import json, time, aiohttp
from ..logger import pjsklogger
from pathlib import Path
from asyncio import sleep


async def Rl_get(event_id : str, params : dict, mode = "jp"):
    configJson = ReadConfig()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url = configJson["API"]["UnipjskAPI"][mode]["getevent"].format(eventid = event_id),params=params,headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0"}) as response:
                res = await response.json()
    except:
        return False
    try:
        rank = str(res['rankings'][0]['rank'])
    except (IndexError, KeyError):
        return -1
    score = str(res['rankings'][0]['score'])
    name = res['rankings'][0]['name']
    return [rank,score,name]

@pjsklogger.catch(exclude=(MatcherException, SkippedException))
async def Get_line_jp(event: Event, cmd = RawCommand()):
    lines = ['1','2','3','10','20','30','40','50','100','200','300','400','500','1000','2000','3000','4000','5000','10000','20000','30000','40000','50000','100000']
    TextList = event.get_plaintext().split(" ")
    if not SpaceRecog(event.get_plaintext(), cmd = cmd) or (TextList[1] not in ['line','实时线','sk']):
        await sekai.skip()
    configJson = ReadConfig()
    try:
        rank = TextList[2]
    except:
        rank = ""
    eventPath = Path(".") / "data" / "ProjectSekai" / "masterdb" / "jp_events.json"
    ycxPath =  Path(".") / "data" / "ProjectSekai" / "masterdb" / "ycx.json"
    if not eventPath.exists():
        pjsklogger.error("jp_events.json doesn't exist. Have you done update?")
        sekai.finish(configJson["MESSAGE"]["ERROR"]["NO_URL"])
    if not ycxPath.exists():
        pjsklogger.error("ycx.json doesn't exist. Have you done update?")
        sekai.finish(configJson["MESSAGE"]["ERROR"]["NO_URL"])
    with open(eventPath.as_posix(), "r") as f:
        eventJson = json.load(f)
    with open(ycxPath.as_posix(), "r") as f:
        preLine = json.load(f)
    event_id = eventJson[-1]["id"]
    
    if(rank in lines):
        params = {"targetRank":rank}
        lineInfo = await Rl_get(params=params,event_id=str(event_id))
        if not lineInfo:
            pjsklogger.warning(f"failed to fetch Lineinfo, params: {params}")
            await sekai.finish(configJson["MESSAGE"]["ERROR"]["SERVER_ERROR"])
        message = configJson["MESSAGE"]["LINE"]["GET_LINE"].format(lineInfo[0],lineInfo[2],lineInfo[1])
        path = Txt2Img(message, withLF=True)
        await sekai.send(Message(MessageSegment.image(path)))
        await sleep(3)
        DeleteByURI(path)
        await sekai.finish()
    else:
        sekaiID = Fetch_id(event.get_user_id())
        try:
            params = {"targetUserId": sekaiID}
        except KeyError:
            await sekai.finish(Message(configJson["MESSAGE"]["ERROR"]["NO_BIND"]))
        lineInfo = await Rl_get(params=params, event_id=str(event_id))
        if not lineInfo:
            pjsklogger.warning(f"failed to fetch lineinfo, params: {params}")
            await sekai.finish(configJson["MESSAGE"]["ERROR"]["SERVER_ERROR"])
        elif lineInfo == -1:
            await sekai.finish(configJson["MESSAGE"]["LINE"]["NONE"])
        msg1 = configJson["MESSAGE"]["LINE"]["SELF"].format(username = lineInfo[2], score = lineInfo[1], rank = lineInfo[0])
        for i in range(len(lines)):
            if(lineInfo[0] == 1):
                msg2 = configJson["MESSAGE"]["LINE"]["EASTEREGG"]
                break
            if(int(lines[i]) > int(lineInfo[0])):
                params1 = {"targetRank":lines[i]}
                params2 = {"targetRank":lines[i-1]}
                lineInfo1 = await Rl_get(event_id=str(event_id),params=params1)
                if not lineInfo1:
                    pjsklogger.warning(f"failed to fetch lineinfo1, params: {params}")
                    await sekai.finish(configJson["MESSAGE"]["ERROR"]["SERVER_ERROR"])
                lineInfo2 = await Rl_get(event_id=str(event_id),params=params2)
                if not lineInfo2:
                    pjsklogger.warning(f"failed to fetch lineinfo2, params: {params}")
                    await sekai.finish(configJson["MESSAGE"]["ERROR"]["SERVER_ERROR"])
                hl = lineInfo2[0]
                ll = lineInfo1[0]
                msg2 = configJson["MESSAGE"]["LINE"]["LINEINFO"].format(high = hl, high_dist = str(int(lineInfo2[1]) - int(lineInfo[1])), low = ll, low_dist = str(int(lineInfo[1]) - int(lineInfo1[1])))
                msg3 = configJson["MESSAGE"]["LINE"]["PREDICTINFO"].format(high = hl, high_score = str(preLine['data'][hl]), low = ll, low_score = str(preLine['data'][ll]))
                break
            else:
                msg2 = configJson["MESSAGE"]["LINE"]["MADAMADA"]
        dist = int(eventJson[-1]["aggregateAt"] / 1000 - time.time())
        days = int(dist / 86400)
        hours = int((dist - days * 86400) / 3600)
        minutes = int((dist - (24 * days + hours) * 3600) / 60)
        seconds = int(dist - 86400 * days - 3600 * hours - 60 * minutes)
        msg4 = configJson["MESSAGE"]["LINE"]["TIME"].format(day=str(days), hour=str(hours), minute=str(minutes), second=str(seconds))
        try:
            msg = msg1 + msg2 + msg3 + msg4
        except:
            msg = msg1 + msg2 + msg4
            path = Txt2Img(msg, withLF=True)
            await sekai.send(Message(MessageSegment.image(path)))
            await sleep(3)
            DeleteByURI(path)
            await sekai.finish()
        path = Txt2Img(msg, withLF=True)
        await sekai.send(Message(MessageSegment.image(path)))
        await sleep(3)
        DeleteByURI(path)
        await sekai.finish()


@pjsklogger.catch(exclude=(MatcherException, SkippedException))
async def Get_line_tw(event: Event, cmd = RawCommand()):
    lines = ['1','2','3','10','20','30','40','50','100','200','300','400','500','1000','2000','3000','4000','5000','10000','20000','30000','40000','50000','100000']
    TextList = event.get_plaintext().split(" ")
    if not SpaceRecog(event.get_plaintext(), cmd = cmd) or (TextList[1] not in ['line','实时线','sk']):
        await sekai.skip()
    configJson = ReadConfig()
    try:
        rank = TextList[2]
    except:
        rank = ""
    eventPath = Path(".") / "data" / "ProjectSekai" / "masterdb" / "tw_events.json"
    if not eventPath.exists():
        pjsklogger.error("tw_events.json doesn't exist. Have you done update?")
        sekai.finish(configJson["MESSAGE"]["ERROR"]["NO_URL"])
    with open(eventPath.as_posix(), "r") as f:
        eventJson = json.load(f)
    event_id = eventJson[-1]["id"]
    
    if(rank in lines):
        params = {"targetRank":rank}
        lineInfo = await Rl_get(params=params, event_id=str(event_id), mode="tw")
        if not lineInfo:
            pjsklogger.warning(f"failed to fetch Lineinfo, params: {params}")
            await sekai.finish(configJson["MESSAGE"]["ERROR"]["SERVER_ERROR"])
        message = configJson["MESSAGE"]["LINE"]["GET_LINE"].format(lineInfo[0],lineInfo[2],lineInfo[1])
        path = Txt2Img(message, withLF=True)
        await sekai.send(Message(MessageSegment.image(path)))
        await sleep(3)
        DeleteByURI(path)
        await sekai.finish()
    else:
        sekaiID = Fetch_id(event.get_user_id())
        try:
            params = {"targetUserId": sekaiID}
        except KeyError:
            await sekai.finish(Message(configJson["MESSAGE"]["ERROR"]["NO_BIND"]))
        lineInfo = await Rl_get(params=params, event_id=str(event_id), mode="tw")
        if not lineInfo:
            pjsklogger.warning(f"failed to fetch lineinfo, params: {params}")
            await sekai.finish(configJson["MESSAGE"]["ERROR"]["SERVER_ERROR"])
        elif lineInfo == -1:
            await sekai.finish(configJson["MESSAGE"]["LINE"]["NONE"])
        msg1 = configJson["MESSAGE"]["LINE"]["SELF"].format(username = lineInfo[2], score = lineInfo[1], rank = lineInfo[0])
        for i in range(len(lines)):
            if(lineInfo[0] == 1):
                msg2 = configJson["MESSAGE"]["LINE"]["EASTEREGG"]
                break
            if(int(lines[i]) > int(lineInfo[0])):
                params1 = {"targetRank":lines[i]}
                params2 = {"targetRank":lines[i-1]}
                lineInfo1 = await Rl_get(event_id=str(event_id),params=params1, mode="tw")
                if not lineInfo1:
                    pjsklogger.warning(f"failed to fetch lineinfo1, params: {params}")
                    await sekai.finish(configJson["MESSAGE"]["ERROR"]["SERVER_ERROR"])
                lineInfo2 = await Rl_get(event_id=str(event_id),params=params2, mode="tw")
                if not lineInfo2:
                    pjsklogger.warning(f"failed to fetch lineinfo2, params: {params}")
                    await sekai.finish(configJson["MESSAGE"]["ERROR"]["SERVER_ERROR"])
                hl = lineInfo2[0]
                ll = lineInfo1[0]
                msg2 = configJson["MESSAGE"]["LINE"]["LINEINFO"].format(high = hl, high_dist = str(int(lineInfo2[1]) - int(lineInfo[1])), low = ll, low_dist = str(int(lineInfo[1]) - int(lineInfo1[1])))
                break
            else:
                msg2 = configJson["MESSAGE"]["LINE"]["MADAMADA"]
        dist = int(eventJson[-1]["aggregateAt"] / 1000 - time.time())
        days = int(dist / 86400)
        hours = int((dist - days * 86400) / 3600)
        minutes = int((dist - (24 * days + hours) * 3600) / 60)
        seconds = int(dist - 86400 * days - 3600 * hours - 60 * minutes)
        msg4 = configJson["MESSAGE"]["LINE"]["TIME"].format(day=str(days), hour=str(hours), minute=str(minutes), second=str(seconds))
        msg = msg1 + msg2 + msg4
        path = Txt2Img(msg, withLF=True)
        await sekai.send(Message(MessageSegment.image(path)))
        await sleep(3)
        DeleteByURI(path)
        await sekai.finish()

@pjsklogger.catch(exclude=(MatcherException, SkippedException))
async def Get_line_en(event: Event, cmd = RawCommand()):
    lines = ['1','2','3','10','20','30','40','50','100','200','300','400','500','1000','2000','3000','4000','5000','10000','20000','30000','40000','50000','100000']
    TextList = event.get_plaintext().split(" ")
    if not SpaceRecog(event.get_plaintext(), cmd = cmd) or (TextList[1] not in ['line','实时线','sk']):
        await sekai.skip()
    configJson = ReadConfig()
    try:
        rank = TextList[2]
    except:
        rank = ""
    eventPath = Path(".") / "data" / "ProjectSekai" / "masterdb" / "en_events.json"
    if not eventPath.exists():
        pjsklogger.error("en_events.json doesn't exist. Have you done update?")
        sekai.finish(configJson["MESSAGE"]["ERROR"]["NO_URL"])
    with open(eventPath.as_posix(), "r") as f:
        eventJson = json.load(f)
    event_id = eventJson[-1]["id"]
    
    if(rank in lines):
        params = {"targetRank":rank}
        lineInfo = await Rl_get(params=params, event_id=str(event_id), mode="en")
        if not lineInfo:
            pjsklogger.warning(f"failed to fetch Lineinfo, params: {params}")
            await sekai.finish(configJson["MESSAGE"]["ERROR"]["SERVER_ERROR"])
        message = configJson["MESSAGE"]["LINE"]["GET_LINE"].format(lineInfo[0],lineInfo[2],lineInfo[1])
        path = Txt2Img(message, withLF=True)
        await sekai.send(Message(MessageSegment.image(path)))
        await sleep(3)
        DeleteByURI(path)
        await sekai.finish()
    else:
        sekaiID = Fetch_id(event.get_user_id())
        try:
            params = {"targetUserId": sekaiID}
        except KeyError:
            await sekai.finish(Message(configJson["MESSAGE"]["ERROR"]["NO_BIND"]))
        lineInfo = await Rl_get(params=params, event_id=str(event_id), mode="en")
        if not lineInfo:
            pjsklogger.warning(f"failed to fetch lineinfo, params: {params}")
            await sekai.finish(configJson["MESSAGE"]["ERROR"]["SERVER_ERROR"])
        elif lineInfo == -1:
            await sekai.finish(configJson["MESSAGE"]["LINE"]["NONE"])
        msg1 = configJson["MESSAGE"]["LINE"]["SELF"].format(username = lineInfo[2], score = lineInfo[1], rank = lineInfo[0])
        for i in range(len(lines)):
            if(lineInfo[0] == 1):
                msg2 = configJson["MESSAGE"]["LINE"]["EASTEREGG"]
                break
            if(int(lines[i]) > int(lineInfo[0])):
                params1 = {"targetRank":lines[i]}
                params2 = {"targetRank":lines[i-1]}
                lineInfo1 = await Rl_get(event_id=str(event_id),params=params1, mode="en")
                if not lineInfo1:
                    pjsklogger.warning(f"failed to fetch lineinfo1, params: {params}")
                    await sekai.finish(configJson["MESSAGE"]["ERROR"]["SERVER_ERROR"])
                lineInfo2 = await Rl_get(event_id=str(event_id),params=params2, mode="en")
                if not lineInfo2:
                    pjsklogger.warning(f"failed to fetch lineinfo2, params: {params}")
                    await sekai.finish(configJson["MESSAGE"]["ERROR"]["SERVER_ERROR"])
                hl = lineInfo2[0]
                ll = lineInfo1[0]
                msg2 = configJson["MESSAGE"]["LINE"]["LINEINFO"].format(high = hl, high_dist = str(int(lineInfo2[1]) - int(lineInfo[1])), low = ll, low_dist = str(int(lineInfo[1]) - int(lineInfo1[1])))
                break
            else:
                msg2 = configJson["MESSAGE"]["LINE"]["MADAMADA"]
        dist = int(eventJson[-1]["aggregateAt"] / 1000 - time.time())
        days = int(dist / 86400)
        hours = int((dist - days * 86400) / 3600)
        minutes = int((dist - (24 * days + hours) * 3600) / 60)
        seconds = int(dist - 86400 * days - 3600 * hours - 60 * minutes)
        msg4 = configJson["MESSAGE"]["LINE"]["TIME"].format(day=str(days), hour=str(hours), minute=str(minutes), second=str(seconds))
        msg = msg1 + msg2 + msg4
        path = Txt2Img(msg, withLF=True)
        await sekai.send(Message(MessageSegment.image(path)))
        await sleep(3)
        DeleteByURI(path)
        await sekai.finish()
