from ..matcher import sekai
from nonebot.adapters.onebot.v11 import Event, MessageSegment
from nonebot.adapters.onebot.v11.message import Message
from nonebot.exception import MatcherException, SkippedException
from nonebot.params import RawCommand
from ..logger import pjsklogger
from ..modules.utils import SpaceRecog, ReadConfig
from ..modules.imagemodules import Txt2Img, DeleteByURI
from pathlib import Path
from asyncio import sleep
import time, json

@pjsklogger.catch(exclude = (SkippedException, MatcherException))
async def Chartrank(event: Event, cmd = RawCommand()):
    # Code from Watagashi-Uni
    TextList = event.get_plaintext().split(" ")
    if not SpaceRecog(event.get_plaintext(), cmd = cmd) or (TextList[1] not in ["难度排行", "fc难度排行", "ap难度排行", "FC难度排行", "AP难度排行"]):
        await sekai.skip()
    configJson = ReadConfig()
    difficulty = ""
    try:
        level = int(TextList[3])
        alias = {"easy":["ez", "easy"], "normal":["no", "normal"], "hard":["hd", "hard"],\
            "expert":["ex", "expert"], "master":["ma", "master"]}
        for i in alias:
            if TextList[2] in alias[i]:
                difficulty = i
                break
        if difficulty == "":
            pjsklogger.warning("Chartrank got illegal arguments:"+ event.get_plaintext())
            await sekai.finish(configJson["MESSAGE"]["ERROR"]["NO_MATCH"])

    except:
        try:
            level = int(TextList[2])
            difficulty = 'master'
        except:
            pjsklogger.warning("Chartrank got illegal arguments:"+ event.get_plaintext())
            await sekai.finish(configJson["MESSAGE"]["ERROR"]["NO_MATCH"])
    fcap = 0
    if "fc" in TextList[1] or "FC" in TextList[1]:
        fcap = 1
    if "ap" in TextList[1] or "AP" in TextList[1]:
        fcap = 2
    target = []
    musicsPath = Path(".") / "data" / "ProjectSekai" / "masterdb" / "musics.json"
    if not musicsPath.exists():
        pjsklogger.error("musics.json doesn't exist. Have you done update?")
        await sekai.finish()
    musicDifficultiesPath = Path(".") / "data" / "ProjectSekai" / "masterdb" / "musicDifficulties.json"
    if not musicDifficultiesPath.exists():
        pjsklogger.error("musicDifficulties.json doesn't exist. Have you done update?")
        await sekai.finish()
    with open(musicDifficultiesPath.as_posix(), 'r', encoding='utf-8') as f:
        data = json.load(f)
    with open(musicsPath.as_posix(), 'r', encoding='utf-8') as f:
        musics = json.load(f)
    for i in data:
        if i['playLevel'] == level and i['musicDifficulty'] == difficulty:
            try:
                i['playLevelAdjust']
                target.append(i)
            except KeyError:
                pass
    if fcap == 0:
        title = f'{difficulty.upper()} {level}难度排行（仅供参考）'
        target.sort(key=lambda x: x["playLevelAdjust"], reverse=True)
    elif fcap == 1:
        title = f'{difficulty.upper()} {level}FC难度排行（仅供参考）'
        target.sort(key=lambda x: x["fullComboAdjust"], reverse=True)
    else:
        title = f'{difficulty.upper()} {level}AP难度排行（仅供参考）'
        target.sort(key=lambda x: x["fullPerfectAdjust"], reverse=True)
    text = ''
    musictitle = ''
    for i in target:
        for j in musics:
            if j['id'] == i['musicId']:
                musictitle = j['title']
                break
        if fcap == 0:
            text = text + f"{musictitle} ({round(i['playLevel'] + i['playLevelAdjust'], 1)})\n"
        elif fcap == 1:
            text = text + f"{musictitle} ({round(i['playLevel'] + i['fullComboAdjust'], 1)})\n"
        else:
            text = text + f"{musictitle} ({round(i['playLevel'] + i['fullPerfectAdjust'], 1)})\n"
    if text == '':
        await sekai.finish(configJson["MESSAGE"]["ERROR"]["NO_MATCH"])
    updatetime = time.localtime(musicDifficultiesPath.stat().st_mtime)
    text = text + '数据来源：https://profile.pjsekai.moe/\nUpdated in ' + time.strftime("%Y-%m-%d %H:%M:%S", updatetime)
    text = title + "\n" + text
    path = Txt2Img(text, withLF=True)
    await sekai.send(Message(MessageSegment.image(path)))
    await sleep(3)
    DeleteByURI(path)
    await sekai.finish()

