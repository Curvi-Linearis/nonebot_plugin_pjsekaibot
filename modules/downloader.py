from .utils import Get_response, ReadConfig
from ..logger import pjsklogger
from nonebot.utils import run_sync
from pathlib import Path
import requests, time, io, json
from types import LambdaType
from PIL import Image

@run_sync
def GetChart_Sekaibest(songId: str, difficulty=["expert", "master"]):
    configJson = ReadConfig()
    originalId = songId
    songId = songId.zfill(4)
    for i in difficulty:
        url = configJson["API"]["chart"]["sekai_best"].format(songId=songId, difficulty=i)
        filename = f"{originalId}_{i}_Sekaibest.png"
        chartPath = Path(".") / "data" / "ProjectSekai" / "chart" / "Sekaibest" / filename
        if chartPath.exists():
            continue
        r = requests.get(url)
        if r.status_code != 200:
            pjsklogger.warning(f"Download failed. Maybe sekai.best doesn't have this resource. url: {url}")
            return False
        with open(chartPath.as_posix(), "wb") as f:
            for chunk in r.iter_content(chunk_size = 512):
                f.write(chunk)
        pjsklogger.success(f"songId: {originalId}, difficulty: {i}, source: sekai.best downloaded.")
    return True


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


@run_sync
def GetChart_sdvxIn(songId: str, difficulty=["expert", "master"]):
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
        data = requests.get(url + f"/obj/data{timeId}{i}.png")
        if data.status_code != 200:
            # pjsklogger.warning(f"Download failed. Maybe sekai.best doesn't have this resource. url: {url}")
            return songId
        bg = requests.get(url + f"/bg/{timeId}bg.png")
        bar = requests.get(url + f"/bg/{timeId}bar.png") 
        
        bgpic = Image.open(io.BytesIO(bg.content))
        datapic = Image.open(io.BytesIO(data.content))
        barpic = Image.open(io.BytesIO(bar.content))
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

def get_musics_json():
    # will be replaced by get_raw_file
    configJson = ReadConfig()
    url = configJson["API"]["realtimeDB"]["pjsekai_moe"]["musics"]
    dbpath = Path(".") / "data" / "ProjectSekai" / "masterdb" / "musics.json" 
    r = requests.get(url)
    if r.status_code != 200:
        pjsklogger.warning(f"Download failed. url: {url}")
        return False
    with open(dbpath.as_posix(), "wb") as f:
        for chunk in r.iter_content(chunk_size = 512):
            f.write(chunk)
    pjsklogger.success(f"musics.json downloaded.")

@run_sync
def get_raw_file(IndexToURL: LambdaType, filepath: str):
    pjsklogger.debug("Start " + filepath)
    configJson = ReadConfig()
    # url = configJson["API"]["realtimeDB"]["pjsekai_moe"]["musics"]
    url = IndexToURL(configJson)
    r = requests.get(url)
    if r.status_code != 200:
        pjsklogger.warning(f"Download failed. url: {url}")
        return False
    with open(filepath, "wb") as f:
        for chunk in r.iter_content(chunk_size = 512):
            f.write(chunk)
    pjsklogger.success(f"Downloaded. path: {filepath}")
    
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
async def Run_every_30_min():
    configJson = ReadConfig()
    rootpath = Path(".") / "data" / "ProjectSekai"

    # ycx.json
    filepath = rootpath / "masterdb" / "ycx.json"
    IndexToURL = lambda x: x["API"]["33Kit"]["jp_ycx"]
    await get_raw_file(IndexToURL, filepath.as_posix())

#@scheduler.scheduled_job("cron", hour="*/24", id="pjsk2")
async def Run_every_1_day():
    configJson = ReadConfig()
    rootpath = Path(".") / "data" / "ProjectSekai" 

    # musics.json
    filepath = rootpath / "masterdb" / "musics.json"
    IndexToURL = lambda x: x["API"]["realtimeDB"]["pjsekai_moe"]["musics"]
    await get_raw_file(IndexToURL, filepath.as_posix())

    # musicDifficulties.json
    filepath = rootpath / "masterdb" / "musicDifficulties.json"
    IndexToURL = lambda x: x["API"]["realtimeDB"]["pjsekai_moe"]["musicDifficulties"]
    await get_raw_file(IndexToURL, filepath.as_posix())

    # Chart
    dbpath = Path(".") / "data" / "ProjectSekai" / "masterdb" / "musics.json"
    if not dbpath.exists():
        pjsklogger.warning("musics.json doesn't exist. Please check [\"API\"][\"realtimeDB\"][\"pjsekai_moe\"][\"music\"] in config.json")
        return
    with open(dbpath.as_posix(), 'r', encoding="utf-8") as f:
        musics = json.load(f)
    for i in musics:
        await GetChart_Sekaibest(str(i["id"]))
        await GetChart_sdvxIn(str(i["id"]))

    # events
    pjsklogger.debug("Getting jp_events")
    filepath = rootpath / "masterdb" / "jp_events.json"
    IndexToURL = lambda x: x["API"]["masterDB"]["sekai_world"]["events"]["jp"]
    await get_raw_file(IndexToURL, filepath.as_posix())
    pjsklogger.debug("Getting tw_events")
    filepath = rootpath / "masterdb" / "tw_events.json"
    IndexToURL = lambda x: x["API"]["masterDB"]["sekai_world"]["events"]["tw"]
    await get_raw_file(IndexToURL, filepath.as_posix())
    pjsklogger.debug("Getting_en_events")
    filepath = rootpath / "masterdb" / "en_events.json"
    IndexToURL = lambda x: x["API"]["masterDB"]["sekai_world"]["events"]["en"]
    await get_raw_file(IndexToURL, filepath.as_posix())

    # Rankmatch
    pjsklogger.debug("Getting rk")
    filepath = rootpath / "masterdb" / "rankMatchClasses.json"
    IndexToURL = lambda x: x["API"]["masterDB"]["sekai_world"]["rankmatch"]["jp"]["classes"]
    await get_raw_file(IndexToURL, filepath.as_posix())
    filepath = rootpath / "masterdb" / "rankMatchGrades.json"
    IndexToURL = lambda x: x["API"]["masterDB"]["sekai_world"]["rankmatch"]["jp"]["grades"]
    await get_raw_file(IndexToURL, filepath.as_posix())
    filepath = rootpath / "masterdb" / "rankMatchSeasons.json"
    IndexToURL = lambda x: x["API"]["masterDB"]["sekai_world"]["rankmatch"]["jp"]["seasons"]
    await get_raw_file(IndexToURL, filepath.as_posix())
    filepath = rootpath / "masterdb" / "rankMatchTiers.json"
    IndexToURL = lambda x: x["API"]["masterDB"]["sekai_world"]["rankmatch"]["jp"]["tiers"]
    await get_raw_file(IndexToURL, filepath.as_posix())

    # Assets
    pjsklogger.debug("Getting assets")
    dbpath = Path(".") / "data" / "ProjectSekai" / "masterdb" / "musics.json"
    if not dbpath.exists():
        pjsklogger.warning("musics.json doesn't exist. Please check [\"API\"][\"realtimeDB\"][\"pjsekai_moe\"][\"music\"] in config.json")
        return
    with open(dbpath.as_posix(), 'r', encoding="utf-8") as f:
        musics = json.load(f)
    for i in musics:
        pjsklogger.debug(f"Start downloading assets: {i}")
        await GetAsset(str(i["id"]))
