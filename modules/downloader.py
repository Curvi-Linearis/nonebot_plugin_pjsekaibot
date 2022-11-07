from .utils import Get_response, ReadConfig
from .ntfy import Notify
from ..logger import pjsklogger
from nonebot.utils import run_sync
from pathlib import Path
import requests, time, io, json
from PIL import Image
import httpx


def MusicIdAsTime(songId: str):
    # Code from Unibot
    dbpath = Path(".") / "data" / "ProjectSekai" / "masterdb" / "musics.json"
    if not dbpath.exists():
        pjsklogger.warning("musics.json doesn't exist. Please check [\"API\"][\"realtimeDB\"][\"pjsekai_moe\"][\"music\"] in config.json")
        return False
    songId = int(songId)
    with open(dbpath.as_posix(), 'r', encoding="utf-8") as f:
        musics = json.load(f)
    musics.sort(key = lambda x: x["publishedAt"])
    for i in range(0, len(musics)):
        if musics[i]["id"] == songId:
            return str(i + 1)
    return 0


async def GetChart_sdvxIn(songId: str, difficulty=["expert", "master"]):
    # Code from Unibot
    configJson = ReadConfig()
    timeId = MusicIdAsTime(songId).zfill(3)
    ## HANDLE STR
    url = configJson["API"]["chart"]["sdvxIn"]
    for i in difficulty:
        filename = f"{songId}_{i}_sdvxIn.png"
        chartPath = Path(".") / "data" / "ProjectSekai" / "chart" / "sdvxIn" / filename
        if chartPath.exists():
            return chartPath.as_posix()
        if i == "master":
            i = "mst"
        elif i == "expert":
            i = "exp"


        dataurl = url + f"/obj/data{timeId}{i}.png"
        bgurl = url + f"/bg/{timeId}bg.png"
        barurl = url + f"/bg/{timeId}bar.png"
        async with httpx.AsyncClient() as client:
            dataresponse = await client.get(dataurl)
            if dataresponse.status_code != 200:
                pjsklogger.warning("{dataresponse.status_code} when GET {dataurl}")
                return
            bgresponse = await client.get(bgurl)
            barresponse = await client.get(barurl)
            bgpic = Image.open(io.BytesIO(bgresponse.content))
            datapic = Image.open(io.BytesIO(dataresponse.content))
            barpic = Image.open(io.BytesIO(barresponse.content))
        
        r, g, b, mask = datapic.split()
        bgpic.paste(datapic, (0, 0), mask)
        r, g, b, mask = barpic.split()
        bgpic.paste(barpic, (0, 0), mask)
        
        if not chartPath.parent.exists():
            chartPath.parent.mkdir(parents=True)
        r, g, b, mask = bgpic.split()
        final = Image.new('RGB', bgpic.size, (0, 0, 0))
        final.paste(bgpic, (0, 0), mask)
        final.save(chartPath.as_posix())
        pjsklogger.success(f"songId: {songId}, difficulty: {i}, source: sdvxIn downloaded.")
    return None


async def GetRawFiles(filelist, urlprefix = "", pathprefix = ""):
    Client = httpx.AsyncClient(timeout=10.0)
    timeoutList = []
    for i in filelist:
        try:
            async with Client.stream("GET", urlprefix + i[0]) as response:
                if response.status_code != 200:
                    pjsklogger.warning(f"{response.status_code} when GET {urlprefix}{i[0]}")
                    continue
                with open(pathprefix + i[1], "wb") as f:
                    async for byte in response.aiter_bytes():
                        f.write(byte)
        except httpx.TimeoutException:
            timeoutList.append(i)
    for i in timeoutList:
        try:
            async with Client.stream("GET", urlprefix + i[0]) as response:
                if response.status_code != 200:
                    pjsklogger.warning(f"{response.status_code} when GET {urlprefix}{i[0]}")
                    continue
                with open(pathprefix + i[1], "wb") as f:
                    async for byte in response.aiter_bytes():
                        f.write(byte)
            timeoutList.remove(i)
        except:
            pass
    if timeoutList:
        pjsklogger.error(f"Timeout list: {timeoutList}")
        await Notify("Timeout list:\n" + str(timeoutList))


@run_sync
def GetAsset(songId: str):
    configJson = ReadConfig()
    originalId = songId
    songId = songId.zfill(3)

    # thumbnail
    filename = f"jacket_s_{songId}.png"
    url = configJson["API"]["asset"]["sekai_best"] + f"/thumbnail/music_jacket_rip/{filename}"
    assetPath = Path(".") / "data" / "ProjectSekai" / "assets" / "Sekaibest" / "thumbnail" / "music_jacket_rip"
    if not assetPath.exists():
        assetPath.mkdir(parents=True)
    assetPath = assetPath / filename
    if assetPath.exists():
        return

    pjsklogger.debug(f"Start downloading assets: {i}")
    r = requests.get(url)
    if r.status_code != 200:
        pjsklogger.warning(f"Download failed. Maybe sekai.best doesn't have this resource. url: {url}")
        return False
    with open(assetPath.as_posix(), "wb") as f:
        for chunk in r.iter_content(chunk_size = 512):
            f.write(chunk)
    pjsklogger.success(f"songId: {originalId}, thumbnail, source: sekai.best downloaded.")

    # jacket
    filename = f"jacket_s_{songId}.png"
    url = configJson["API"]["asset"]["sekai_best"] + f"/music/jacket/jacket_s_{songId}_rip/{filename}"
    assetPath = Path(".") / "data" / "ProjectSekai" / "assets" / "Sekaibest" / "music" / "jacket" / filename
    if not assetPath.exists():
        assetPath.mkdir(parents=True)
    assetPath = assetPath / filename
    r = requests.get(url)
    if r.status_code != 200:
        pjsklogger.warning(f"Download failed. Maybe sekai.best doesn't have this resource. url: {url}")
        return False
    with open(assetPath.as_posix(), "wb") as f:
        for chunk in r.iter_content(chunk_size = 512):
            f.write(chunk)
    pjsklogger.success(f"songId: {originalId}, jacket, source: sekai.best downloaded.")
    return True


#@scheduler.scheduled_job("cron", minute="*/30", id="pjsk1")
@pjsklogger.catch
async def Run_every_30_min():
    configJson = ReadConfig()
    rootpath = Path(".") / "data" / "ProjectSekai"

    # ycx.json
    filepath = rootpath / "masterdb" / "ycx.json"
    url = configJson["API"]["33Kit"]["jp_ycx"]
    filelist = [(url, filepath.as_posix())]
    await GetRawFiles(filelist)


@pjsklogger.catch
async def Run_every_1_day():
    configJson = ReadConfig()
    rootpath = Path(".") / "data" / "ProjectSekai" 

    pjsekaimoeList = []
    # musics.json
    filepath = rootpath / "masterdb" / "musics.json"
    url = configJson["API"]["realtimeDB"]["pjsekai_moe"]["musics"]
    pjsekaimoeList.append((url, filepath.as_posix()))

    # musicDifficulties.json
    filepath = rootpath / "masterdb" / "musicDifficulties.json"
    url = configJson["API"]["realtimeDB"]["pjsekai_moe"]["musicDifficulties"]
    pjsekaimoeList.append((url, filepath.as_posix()))
    await GetRawFiles(pjsekaimoeList)


    # Chart
    dbpath = Path(".") / "data" / "ProjectSekai" / "masterdb" / "musics.json"
    if not dbpath.exists():
        pjsklogger.warning("musics.json doesn't exist. Please check [\"API\"][\"realtimeDB\"][\"pjsekai_moe\"][\"music\"] in config.json")
        return
    with open(dbpath.as_posix(), 'r', encoding="utf-8") as f:
        musics = json.load(f)
    SekaibestList = []
    SdvxinIDList = []
    difficulty = ["expert", "master"]
    for i in musics:
        songId = str(i["id"])
        originalId = songId
        songId = songId.zfill(4)
        for i in difficulty:
            url = configJson["API"]["chart"]["sekai_best"].format(songId=songId, difficulty=i)
            filename = f"{originalId}_{i}_Sekaibest.png"
            chartPath = Path(".") / "data" / "ProjectSekai" / "chart" / "Sekaibest" / filename
            if not chartPath.exists():
                SekaibestList.append((url, chartPath.as_posix()))
        
        for i in difficulty:
            filename = f"{originalId}_{i}_sdvxIn.png"
            chartPath = Path(".") / "data" / "ProjectSekai" / "chart" / "sdvxIn" / filename
            if not chartPath.exists():
                SdvxinIDList.append(originalId)
    await GetRawFiles(SekaibestList)
    for i in SdvxinIDList:
        await GetChart_sdvxIn(i)


    # events
    eventsList = []
    pjsklogger.debug("Getting jp_events")
    filepath = rootpath / "masterdb" / "jp_events.json"
    url = configJson["API"]["masterDB"]["sekai_world"]["events"]["jp"]
    eventsList.append((url, filepath.as_posix()))
    pjsklogger.debug("Getting tw_events")
    filepath = rootpath / "masterdb" / "tw_events.json"
    url = configJson["API"]["masterDB"]["sekai_world"]["events"]["tw"]
    eventsList.append((url, filepath.as_posix()))
    pjsklogger.debug("Getting_en_events")
    filepath = rootpath / "masterdb" / "en_events.json"
    url = configJson["API"]["masterDB"]["sekai_world"]["events"]["en"]
    eventsList.append((url, filepath.as_posix()))
    await GetRawFiles(eventsList)

    # Rankmatch
    rankmatchList = []
    pjsklogger.debug("Getting rk")
    filepath = rootpath / "masterdb" / "rankMatchClasses.json"
    url = configJson["API"]["masterDB"]["sekai_world"]["rankmatch"]["jp"]["classes"]
    rankmatchList.append((url, filepath.as_posix()))
    filepath = rootpath / "masterdb" / "rankMatchGrades.json"
    url = configJson["API"]["masterDB"]["sekai_world"]["rankmatch"]["jp"]["grades"]
    rankmatchList.append((url, filepath.as_posix()))
    filepath = rootpath / "masterdb" / "rankMatchSeasons.json"
    url = configJson["API"]["masterDB"]["sekai_world"]["rankmatch"]["jp"]["seasons"]
    rankmatchList.append((url, filepath.as_posix()))
    filepath = rootpath / "masterdb" / "rankMatchTiers.json"
    url = configJson["API"]["masterDB"]["sekai_world"]["rankmatch"]["jp"]["tiers"]
    rankmatchList.append((url, filepath.as_posix()))
    await GetRawFiles(rankmatchList)

    # Assets
    pjsklogger.debug("Getting assets")
    dbpath = Path(".") / "data" / "ProjectSekai" / "masterdb" / "musics.json"
    if not dbpath.exists():
        pjsklogger.warning("musics.json doesn't exist. Please check [\"API\"][\"realtimeDB\"][\"pjsekai_moe\"][\"music\"] in config.json")
        return
    with open(dbpath.as_posix(), 'r', encoding="utf-8") as f:
        musics = json.load(f)
    for i in musics:
        await GetAsset(str(i["id"]))
    pjsklogger.success("Updating success!")
    await Notify("Updating Success!")
