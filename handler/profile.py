from ..logger import pjsklogger
from ..matcher import sekai, twsekai, ensekai
from ..modules.utils import Get_response, Fetch_id, SpaceRecog, ReadConfig
from ..modules.imagemodules import Txt2Img, DeleteByURI
from sqlite3 import OperationalError
from nonebot.exception import SkippedException, MatcherException
from nonebot.adapters.onebot.v11 import Event, MessageSegment
from nonebot.adapters.onebot.v11.message import Message
from nonebot.params import RawCommand
from prettytable import PrettyTable, NONE
import asyncio


def Parse_profile(p_json):
    dic = {}
    status = {"clear": {"easy": [], "normal": [], "hard": [], "expert": [], "master": []}, "full_combo": {"easy": [], "normal": [], "hard": [], "expert": [], "master": []}, "full_perfect": {"easy": [], "normal": [], "hard": [], "expert": [], "master": []}}
    for i in p_json["userMusicResults"]:
        if i["musicId"] not in status[i["playResult"]][i["musicDifficulty"]]:
            status[i["playResult"]][i["musicDifficulty"]].append(i["musicId"])
    temp_word = ["easy", "normal", "hard", "expert", "master"]
    for i in temp_word:
        status["full_combo"][i].extend(status["full_perfect"][i])
        status["full_combo"][i] = list(set(status["full_combo"][i]))
        status["clear"][i].extend(status["full_combo"][i])
        status["clear"][i] = list(set(status["clear"][i]))
    for i in status:
        for j in status[i]:
            status[i][j] = len(status[i][j])
    return status

@pjsklogger.catch(exclude = (SkippedException, MatcherException))
async def Profile_jp(event: Event, cmd = RawCommand()):
    TextList = event.get_plaintext().split(" ")
    if not SpaceRecog(event.get_plaintext(), cmd = cmd) or (TextList[1] not in ['profile','prof','资料']):
        await sekai.skip()
    configJson = ReadConfig()
    qqid = event.get_user_id()

    try:
        targetUserId = Fetch_id(qqid, "jp")
    except OperationalError:
        await sekai.finish(Message(configJson["MESSAGE"]["ERROR"]["NO_BIND"]))

    try:
        url = configJson["API"]["UnipjskAPI"]["jp"]["profile"].format(targetUserId=targetUserId)
    except KeyError:
        pjsklogger.error("config.json is corrupted. Check if [\"API\"][\"UnipjskAPI\"][\"jp\"][\"profile\"] exists.")

    if url == "":
        pjsklogger.warning("Query can not finish because you didn't register profile api in config.json.")
        await sekai.finish(Message(configJson["MESSAGE"]["ERROR"]["NO_URL"]))

    try:
        response_json = await Get_response(url)
        if response_json == {}:
            pjsklogger.error(f"The response is empty. Request jp_id: {targetUserId}")
            raise Exception
    except:
        await sekai.finish(Message(configJson["MESSAGE"]["ERROR"]["SERVER_ERROR"]))


    status = Parse_profile(response_json)
    username = response_json["user"]["userGamedata"]["name"]
    userrank = response_json["user"]["userGamedata"]["rank"]

    x = PrettyTable() # https://pypi.org/project/prettytable/
    x.field_names = [" ", "EZ", "NO", "HD", "EX", "MA"]
    a = []
    for i in status:
        for j in status[i]:
            a.append(str(status[i][j]))

    x.add_row(["cl"] + a[0:5])
    x.add_row(["fc"] + a[5:10])
    x.add_row(["ap"] + a[10:15])
    x.hrules = NONE

    message = configJson["MESSAGE"]["PROFILE"]["USERDATA"].format(username=username, targetUserId=targetUserId, userrank=userrank, results=x.get_string())
    URI = Txt2Img(message, withLF=True)
    await sekai.send(MessageSegment.image(URI))
    await asyncio.sleep(3)
    DeleteByURI(URI)
    await sekai.finish()

@pjsklogger.catch(exclude = (SkippedException, MatcherException))
async def Profile_tw(event: Event, cmd = RawCommand()):
    TextList = event.get_plaintext().split(" ")
    if not SpaceRecog(event.get_plaintext(), cmd = cmd) or (TextList[1] not in ['profile','prof','资料']):
        await twsekai.skip()
    configJson = ReadConfig()
    qqid = event.get_user_id()

    try:
        targetUserId = Fetch_id(qqid, "tw")
    except OperationalError:
        await twsekai.finish(Message(configJson["MESSAGE"]["ERROR"]["NO_BIND"]))

    try:
        url = configJson["API"]["UnipjskAPI"]["tw"]["profile"].format(targetUserId=targetUserId)
    except KeyError:
        pjsklogger.error("config.json is corrupted. Check if [\"API\"][\"UnipjskAPI\"][\"tw\"][\"profile\"] exists.")

    if url == "":
        pjsklogger.warning("Query can not finish because you didn't register profile api in config.json.")
        await twsekai.finish(Message(configJson["MESSAGE"]["ERROR"]["NO_URL"]))

    try:
        response_json = await Get_response(url)
        if response_json == {}:
            pjsklogger.error(f"The response is empty. Request tw_id: {targetUserId}")
            raise Exception
    except:
        await twsekai.finish(Message(configJson["MESSAGE"]["ERROR"]["SERVER_ERROR"]))


    status = Parse_profile(response_json)
    username = response_json["user"]["userGamedata"]["name"]
    userrank = response_json["user"]["userGamedata"]["rank"]

    x = PrettyTable() # https://pypi.org/project/prettytable/
    x.field_names = [" ", "EZ", "NO", "HD", "EX", "MA"]
    a = []
    for i in status:
        for j in status[i]:
            a.append(str(status[i][j]))

    x.add_row(["cl"] + a[0:5])
    x.add_row(["fc"] + a[5:10])
    x.add_row(["ap"] + a[10:15])
    x.hrules = NONE

    message = configJson["MESSAGE"]["PROFILE"]["USERDATA"].format(username=username, targetUserId=targetUserId, userrank=userrank, results=x.get_string())
    URI = Txt2Img(message, withLF=True)
    await twsekai.send(MessageSegment.image(URI))
    await asyncio.sleep(3)
    DeleteByURI(URI)
    await twsekai.finish()

@pjsklogger.catch(exclude = (SkippedException, MatcherException))
async def Profile_en(event: Event, cmd = RawCommand()):
    TextList = event.get_plaintext().split(" ")
    if not SpaceRecog(event.get_plaintext(), cmd = cmd) or (TextList[1] not in ['profile','prof','资料']):
        await ensekai.skip()
    configJson = ReadConfig()
    qqid = event.get_user_id()

    try:
        targetUserId = Fetch_id(qqid, "en")
    except OperationalError:
        await ensekai.finish(Message(configJson["MESSAGE"]["ERROR"]["NO_BIND"]))

    try:
        url = configJson["API"]["UnipjskAPI"]["en"]["profile"].format(targetUserId=targetUserId)
    except KeyError:
        pjsklogger.error("config.json is corrupted. Check if [\"API\"][\"UnipjskAPI\"][\"en\"][\"profile\"] exists.")

    if url == "":
        pjsklogger.warning("Query can not finish because you didn't register profile api in config.json.")
        await ensekai.finish(Message(configJson["MESSAGE"]["ERROR"]["NO_URL"]))

    try:
        response_json = await Get_response(url)
        if response_json == {}:
            pjsklogger.error(f"The response is empty. Request en_id: {targetUserId}")
            raise Exception
    except:
        await ensekai.finish(Message(configJson["MESSAGE"]["ERROR"]["SERVER_ERROR"]))


    status = Parse_profile(response_json)
    username = response_json["user"]["userGamedata"]["name"]
    userrank = response_json["user"]["userGamedata"]["rank"]

    x = PrettyTable() # https://pypi.org/project/prettytable/
    x.field_names = [" ", "EZ", "NO", "HD", "EX", "MA"]
    a = []
    for i in status:
        for j in status[i]:
            a.append(str(status[i][j]))

    x.add_row(["cl"] + a[0:5])
    x.add_row(["fc"] + a[5:10])
    x.add_row(["ap"] + a[10:15])
    x.hrules = NONE

    message = configJson["MESSAGE"]["PROFILE"]["USERDATA"].format(username=username, targetUserId=targetUserId, userrank=userrank, results=x.get_string())
    URI = Txt2Img(message, withLF=True)
    await ensekai.send(MessageSegment.image(URI))
    await asyncio.sleep(3)
    DeleteByURI(URI)
    await ensekai.finish()
