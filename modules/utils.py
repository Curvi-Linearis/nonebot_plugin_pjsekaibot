import json, re, asyncio, sqlite3, aiohttp
from pathlib import Path
from ..logger import pjsklogger

    
async def Get_response(url, headers=None):
    if headers == None:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                pjsklogger.warning(f"status code: {response.status}")
                return
            try:
                response_json = await response.json()
                pjsklogger.success(f"Got a valid json response.")
                return response_json
            except (json.decoder.JSONDecodeError):
                pjsklogger.warning("Response is not in json format.")
                raise json.decoder.JSONDecodeError
                return 


def Fetch_id(qqid, mode="jp"):
    DBPath = Path(".") / "data" / "ProjectSekai" / "pjsk.db"
    con = sqlite3.connect(DBPath.as_posix())
    cur = con.cursor()
    cur.execute(f"SELECT {mode}SekaiID FROM account WHERE qqid = ?", (qqid,))
    record = cur.fetchone()
    if record is None:
        pjsklogger.debug(f"{qqid} isn't in the database.")
        raise sqlite3.OperationalError(f"{qqid} not in database.")
    else:
        pjsklogger.success(f"Successfully retrieved data. Key: {qqid}")
        return record[0]

async def Get_song_id(nickname):
    configJson = ReadConfig()
    if configJson is None:
        return
    url = configJson["API"]["UnipjskAPI"]["jp"]["getsongid"]
    if url == "":
        pjsklogger.error("Please check [\"API\"][\"UnipjskAPI\"][\"jp\"][\"getsongid\"] in config.json")
        return
    url = url.format(musicId=nickname)
    response = await Get_response(url)
    if response["status"] == "success":
        pjsklogger.success("Get song id success, {musicId}: {title}".format(musicId=response["musicId"], title=response["title"]))
        return response["title"], response["musicId"], response["match"]
    else:
        return False


def SpaceRecog(text:str,cmd:str):
    if len(text.split(cmd + " ")) == 1 and text != cmd:
        return False
    else:
        return True

def ReadConfig():
    configPath = Path(".") / "data" / "ProjectSekai" / "config.json"
    try:
        with configPath.open() as f:
            configJson = json.load(f)
    except FileNotFoundError:
        pjsklogger.error("config.json file not found. Have you initialized the pjsekaibot plugin? Check the documentation to init.")
        return
    except json.decoder.JSONDecodeError:
        pjsklogger.error("config.json can't be decoded as json. Please check your syntax in config.json.")
        return
    return configJson


