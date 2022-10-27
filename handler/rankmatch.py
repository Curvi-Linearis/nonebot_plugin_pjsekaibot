from ..matcher import sekai
from nonebot.params import RawCommand
from nonebot.adapters.onebot.v11 import Event, MessageSegment
from nonebot.adapters.onebot.v11.message import Message
from nonebot.exception import MatcherException, SkippedException
from ..modules.utils import Fetch_id, Get_response, ReadConfig, SpaceRecog
from ..modules.imagemodules import Txt2Img, DeleteByURI
from pathlib import Path
from asyncio import sleep
import json
from ..logger import pjsklogger

@pjsklogger.catch(exclude = (MatcherException, SkippedException))
async def Rankmatch(event: Event ,cmd = RawCommand()):
    TextList = event.get_plaintext().split(" ")
    if not SpaceRecog(event.get_plaintext(), cmd = cmd) or (TextList[1] not in ['rk','rankmatch','排位']):
        await sekai.skip()
    qqid = event.get_user_id()
    configJson = ReadConfig()
    try:
        segaid = Fetch_id(qqid)
    except:
        await sekai.finish(Message(configJson["MESSAGE"]["ERROR"]["NO_BIND"]))
    rootpath = Path(".") / "data" / "ProjectSekai" / "masterdb"
    classespath = rootpath / "rankMatchClasses.json"
    gradespath = rootpath / "rankMatchGrades.json"
    seasonspath = rootpath / "rankMatchSeasons.json"
    tierspath = rootpath / "rankMatchTiers.json"
    with open(seasonspath.as_posix(), "r") as f:
        seasonsJson = json.load(f)
    with open(gradespath.as_posix(), "r") as f:
        gradesJson = json.load(f)
    with open(classespath.as_posix(), "r") as f:
        classesJson = json.load(f)
    with open(tierspath.as_posix(), "r") as f:
        tiersJson = json.load(f)
    season = seasonsJson[-1]["id"]
    url = configJson["API"]["UnipjskAPI"]["jp"]["rankmatch_by_user"]
    if url == "":
        pjsklogger.warning("Please check [\"API\"][\"UnipjskAPI\"][\"jp\"][\"rankmatch_by_user\"] in confug.json")
        await sekai.finish(Message(configJson["MESSAGE"]["ERROR"]["NO_URL"]))
    url = url.format(season = season, targetUserId = segaid)
    try:
        response_json = await Get_response(url)
    except:
        await sekai.finish(Message(configJson["MESSAGE"]["ERROR"]["SERVER_ERROR"]))
    if response_json["rankings"] == []:
        await sekai.finish(Message(configJson["MESSAGE"]["RANKMATCH"]["NO_RANK"]))
    maindic = response_json["rankings"][0]
    tierid = maindic["userRankMatchSeason"]["rankMatchTierId"]
    for i in range(len(tiersJson)):
        if tiersJson[i]["id"] == tierid:
            gradeid = tiersJson[i]["rankMatchGradeId"]
            classid = tiersJson[i]["rankMatchClassId"]
    for i in range(len(gradesJson)):
        if gradesJson[i]["id"] == gradeid:
            gradename = gradesJson[i]["name"]
    for i in range(len(classesJson)):
        if classesJson[i]["id"] == classid:
            classname = classesJson[i]["name"]
    try:
        win_rate = maindic["userRankMatchSeason"]["winCount"] / (maindic["userRankMatchSeason"]["winCount"] + maindic["userRankMatchSeason"]["loseCount"])
    except:
        win_rate = "N/A"
    message = configJson["MESSAGE"]["RANKMATCH"]["USER"].format(username=maindic["name"], userid=segaid)\
        + configJson["MESSAGE"]["RANKMATCH"]["RANK"].format(gradename=gradename, classname=classname, tierpoint=maindic["userRankMatchSeason"]["tierPoint"], ranking=maindic["rank"])\
        + configJson["MESSAGE"]["RANKMATCH"]["COUNT"].format(wincount=maindic["userRankMatchSeason"]["winCount"], drawcount=maindic["userRankMatchSeason"]["drawCount"], losecount=maindic["userRankMatchSeason"]["loseCount"])\
        + configJson["MESSAGE"]["RANKMATCH"]["WINRATE"].format(win_rate=win_rate)\
        + configJson["MESSAGE"]["RANKMATCH"]["MCWC"].format(mcwc=maindic["userRankMatchSeason"]["maxConsecutiveWinCount"])
    path = Txt2Img(message, withLF=True)
    await sekai.send(Message(MessageSegment.image(path)))
    await sleep(3)
    DeleteByURI(path)
    await sekai.finish()

