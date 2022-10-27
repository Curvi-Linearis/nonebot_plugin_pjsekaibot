from ..matcher import sekai
from ..modules.utils import ReadConfig, Get_song_id, SpaceRecog
from nonebot.adapters.onebot.v11 import Event, MessageSegment
from nonebot.exception import MatcherException, SkippedException
from nonebot.params import RawCommand
from nonebot.adapters.onebot.v11.message import Message
from ..logger import pjsklogger
from pathlib import Path

@pjsklogger.catch(exclude = (MatcherException, SkippedException))
async def Get_chart(event: Event,cmd = RawCommand()):
    TextList = event.get_plaintext().split(" ")
    if not SpaceRecog(event.get_plaintext(),cmd = cmd) or TextList[1] != "chart":
        await sekai.skip()
    configJson = ReadConfig()
    if configJson is None:
        await sekai.finish()
    songname = event.get_plaintext()[10:]
    difficulty = "ma"
    lastword = TextList[-1].lower()
    if lastword == "ex":
        difficulty = "ex"
        songname = songname[:-3]
    alias = {"easy":["ez", "easy"], "normal":["no", "normal"], "hard":["hd", "hard"],\
            "expert":["ex", "expert"], "master":["ma", "master"]}
    for i in alias:
        if difficulty in alias[i]:
            difficultyStr = i
            break
    try:
        pjsklogger.debug(f"Get_chart got arguments: {songname}, {difficulty}")
        title, songId, match = await Get_song_id(songname)
    except:
        pjsklogger.warning(f"Get_chart with arguments {songname} and {difficulty} did not retrieve a valid response.")
        await sekai.finish(Message(configJson["MESSAGE"]["ERROR"]["NO_MATCH"]))
    chartRoot = Path(".") / "data" / "ProjectSekai" / "chart"
    chartPath = chartRoot / "Sekaibest" / f"{songId}_{difficultyStr}_Sekaibest.png" 
    if not chartPath.exists():
        chartPath = chartRoot / "sdvxIn" / f"{songId}_{difficultyStr}_sdvxIn.png"
        if not chartPath.exists():
            await sekai.finish(Message(configJson["MESSAGE"]["CHART"]["WAIT_FOR_UPDATE"]))
    await sekai.finish(MessageSegment.text(f"{title}\n") + MessageSegment.image(chartPath.resolve().as_uri()))
