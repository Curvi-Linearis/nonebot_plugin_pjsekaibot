from ..matcher import sekai, twsekai, ensekai
from ..logger import pjsklogger
from nonebot.matcher import Matcher
from ..modules.utils import SpaceRecog, Get_response
from ..modules.imagemodules import Txt2Img, DeleteByURI
from ..modules.utils import ReadConfig
from nonebot.params import ArgPlainText, RawCommand
from nonebot.exception import MatcherException, SkippedException
from nonebot.adapters.onebot.v11 import Event, MessageSegment
from nonebot.adapters.onebot.v11.message import Message
import re
import json
import sqlite3
import asyncio
from pathlib import Path

@pjsklogger.catch(exclude = (SkippedException, MatcherException))
async def Bind_jp(event: Event,matcher : Matcher, cmd = RawCommand()):
    TextList = event.get_plaintext().split(" ")
    if not SpaceRecog(event.get_plaintext(), cmd = cmd) or (TextList[1] not in ['bind','绑定']):
        matcher.set_arg("id",Message(""))
        await sekai.skip()
    try:
        segaid = TextList[2]
        pjsklogger.debug("Calling func Bind_jp, arg:[\"{}\"]".format(segaid))
        matcher.set_arg("id",Message(segaid))
        pjsklogger.success("Bind_jp Success.")
    except:
        pjsklogger.warning("Bind_jp failed, arg:[\"{}\"]".format(segaid))
        pass

@pjsklogger.catch(exclude = (MatcherException, SkippedException))
async def Got_bind_jp(event : Event,id: str = ArgPlainText("id")):
    if id == "":
        await sekai.skip()
    pjsklogger.debug("Calling func Got_bind_jp, arg:[\"{}\"]".format(id))
    configJson = ReadConfig()
    if(bool(re.match(r"^\d{10,}$",id)) == False):
        pjsklogger.warning(f"Id {id} is not a valid jp_sekaiID.")
        await sekai.finish(configJson["MESSAGE"]["ERROR"]["NO_MATCH"])

    try:
        url = configJson["API"]["UnipjskAPI"]["jp"]["profile"]
        if url == "":
            pjsklogger.error("Please check [\"API\"][\"UnipjskAPI\"][\"jp\"][\"profile\"] in config.json")
            await sekai.finish(Message(configJson["MESSAGE"]["ERROR"]["NO_URL"]))
        response_json = await Get_response(url.format(targetUserId = id))
    except KeyError:
        pjsklogger.error("<profile> API may be incorrect in config.json.")
        await sekai.finish(Message(configJson["MESSAGE"]["ERROR"]["NO_URL"]))
    try:
        username = response_json["user"]["userGamedata"]["name"]
    except KeyError:
        pjsklogger.warning(f"jp_ID {id} did not retrieve a valid response. Maybe the ID is incorrect.")
        await sekai.finish(Message(configJson["MESSAGE"]["ERROR"]["NO_MATCH"]))
    except:
        pjsklogger.error(f"The response seems not right. The request jp_ID is {id}.")
        await sekai.finish(Message(configJson["MESSAGE"]["ERROR"]["SERVER_ERROR"]))
    qqid = event.get_user_id()
    DBPath = Path(".") / "data" / "ProjectSekai" / "pjsk.db"
    con = sqlite3.connect(DBPath.as_posix())
    cur = con.cursor()
    cur.execute("SELECT jpSekaiID FROM account WHERE qqID = ?", (qqid,))
    record = cur.fetchone()
    if record is None:
        cur.execute("INSERT INTO account (qqID, jpSekaiID) VALUES (?, ?)", (qqid, id))
    else:
        cur.execute("UPDATE account SET jpSekaiID = ? WHERE qqID = ?", (id, qqid))
    con.commit()
    con.close()
    pjsklogger.success(f"Successfully binded. jp_ID={id}")

    text = configJson["MESSAGE"]["BIND"]["BIND_SUCCESS"].format(bindid = id,username = username)
    URI = Txt2Img(text)
    await sekai.send(Message(MessageSegment.image(URI)))
    await asyncio.sleep(3)
    DeleteByURI(URI)
    await sekai.finish()

@pjsklogger.catch(exclude = SkippedException)
async def Bind_tw(event: Event,matcher : Matcher, cmd = RawCommand()):
    TextList = event.get_plaintext().split(" ")
    if not SpaceRecog(event.get_plaintext(), cmd = cmd) or (TextList[1] not in ['bind','绑定']):
        matcher.set_arg("twid",Message(""))
        await sekai.skip()
    try:
        segaid = TextList[2]
        pjsklogger.debug("Calling func Bind_tw, arg[\"{}\"]".format(segaid))
        matcher.set_arg("twid",Message(segaid))
        pjsklogger.success("Bind_tw Success.")
    except:
        pass

@pjsklogger.catch(exclude = (MatcherException, SkippedException))
async def Got_bind_tw(event : Event,id: str = ArgPlainText("twid")):
    if id == "":
        await sekai.skip()
    configJson = ReadConfig()
    if(bool(re.match(r"^\d{10,}$",id)) == False):
        pjsklogger.error(f"Id {id} is not a valid tw_sekaiID.")
        await sekai.finish(Message(configJson["MESSAGE"]["ERROR"]["NO_MATCH"]))

    try:
        url = configJson["API"]["UnipjskAPI"]["tw"]["profile"]
        if url == "":
            pjsklogger.warning("Please check [\"API\"][\"UnipjskAPI\"][\"tw\"][\"profile\"] in config.json")
            await sekai.finish(Message(configJson["MESSAGE"]["ERROR"]["NO_URL"]))
        response_json = await Get_response(url.format(targetUserId = id))
    except KeyError:
        pjsklogger.error("Please check your API in config.json.")
        await sekai.finish(Message(configJson["MESSAGE"]["ERROR"]["NO_URL"]))
    try:
        username = response_json["user"]["userGamedata"]["name"]
    except KeyError:
        pjsklogger.error(f"tw_ID {id} did not retrieve a valid response. Maybe the ID is incorrect.")
        await sekai.finish(Message(configJson["MESSAGE"]["ERROR"]["NO_MATCH"]))
    except:
        pjsklogger.error(f"The response seems not right. The request tw_ID is {id}.")
        await sekai.finish(Message(configJson["MESSAGE"]["ERROR"]["SERVER_ERROR"]))
    qqid = event.get_user_id()
    DBPath = Path(".") / "data" / "ProjectSekai" / "pjsk.db"
    con = sqlite3.connect(DBPath.as_posix())
    cur = con.cursor()
    cur.execute("SELECT twSekaiID FROM account WHERE qqID = ?", (qqid,))
    record = cur.fetchone()
    if record is None:
        cur.execute("INSERT INTO account (qqID, twSekaiID) VALUES (?, ?)", (qqid, id))
    else:
        cur.execute("UPDATE account SET twSekaiID = ? WHERE qqID = ?", (id, qqid))
    con.commit()
    con.close()
    pjsklogger.success(f"Successfully binded. tw_ID={id}")

    text = configJson["MESSAGE"]["BIND"]["BIND_SUCCESS"].format(bindid = id,username = username)
    URI = Txt2Img(text)
    await sekai.send(Message(MessageSegment.image(URI)))
    await asyncio.sleep(3)
    DeleteByURI(URI)
    await sekai.finish()


@pjsklogger.catch(exclude = SkippedException)
async def Bind_en(event: Event,matcher : Matcher, cmd = RawCommand()):
    TextList = event.get_plaintext().split(" ")
    if not SpaceRecog(event.get_plaintext(), cmd = cmd) or (TextList[1] not in ['bind','绑定']):
        matcher.set_arg("enid",Message(""))
        await sekai.skip()
    try:
        segaid = TextList[2]
        matcher.set_arg("enid",Message(segaid))
        pjsklogger.debug(f"Bind_en got an argument {enid}")
    except:
        pass

@pjsklogger.catch(exclude = (MatcherException, SkippedException))
async def Got_bind_en(event : Event,id: str = ArgPlainText("enid")):
    if id == "":
        await sekai.skip()
    configJson = ReadConfig()
    if(bool(re.match(r"^\d{10,}$",id)) == False):
        pjsklogger.error(f"Id {id} is not a valid en_sekaiID.")
        await sekai.finish(Message(configJson["MESSAGE"]["ERROR"]["NO_MATCH"]))

    try:
        url = configJson["API"]["UnipjskAPI"]["en"]["profile"]
        if url == "":
            pjsklogger.warning("Please check [\"API\"][\"UnipjskAPI\"][\"en\"][\"profile\"] in config.json")
            await sekai.finish(Message(configJson["MESSAGE"]["ERROR"]["NO_URL"]))
        response_json = await Get_response(url.format(targetUserId = id))
    except KeyError:
        pjsklogger.error("Please check your API in config.json.")
        await sekai.finish(Message(configJson["MESSAGE"]["ERROR"]["NO_URL"]))
    try:
        username = response_json["user"]["userGamedata"]["name"]
    except KeyError:
        pjsklogger.error(f"en_ID {id} did not retrieve a valid response. Maybe the ID is incorrect.")
        await sekai.finish(configJson["MESSAGE"]["ERROR"]["NO_MATCH"])
    except:
        pjsklogger.error(f"The response seems not right. The request en_ID is {id}.")
        await sekai.finish(Message(configJson["MESSAGE"]["ERROR"]["SERVER_ERROR"]))
    qqid = event.get_user_id()
    DBPath = Path(".") / "data" / "ProjectSekai" / "pjsk.db"
    con = sqlite3.connect(DBPath.as_posix())
    cur = con.cursor()
    cur.execute("SELECT enSekaiID FROM account WHERE qqID = ?", (qqid,))
    record = cur.fetchone()
    if record is None:
        cur.execute("INSERT INTO account (qqID, enSekaiID) VALUES (?, ?)", (qqid, id))
    else:
        cur.execute("UPDATE account SET enSekaiID = ? WHERE qqID = ?", (id, qqid))
    con.commit()
    con.close()
    pjsklogger.success(f"Successfully binded. en_ID={id}")

    text = configJson["MESSAGE"]["BIND"]["BIND_SUCCESS"].format(bindid = id,username = username)
    URI = Txt2Img(text)
    await sekai.send(Message(MessageSegment.image(URI)))
    await asyncio.sleep(3)
    DeleteByURI(URI)
    await sekai.finish()
