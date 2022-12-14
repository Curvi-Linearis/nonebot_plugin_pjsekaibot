import sqlite3
from pathlib import Path
from ..logger import pjsklogger

@pjsklogger.catch
def CreatePath():
    if not Path("./bot.py").exists():
        pjsklogger.ERROR("Work directory is incorrect. \"bot.py\" should be in work directory.")
        # error message
    rootpath = Path(".")
    datapath = rootpath / "data" / "ProjectSekai"
    datapath.mkdir(parents=True, exist_ok=True)
    assetspath = datapath / "assets"
    assetspath.mkdir(parents=True, exist_ok=True)
    cachepath = datapath / "cache"
    cachepath.mkdir(parents=True, exist_ok=True)
    chartpath1 = datapath / "chart" / "moe"
    chartpath1.mkdir(parents=True, exist_ok=True)
    chartpath2 = datapath / "chart" / "Sekaibest"
    chartpath2.mkdir(parents=True, exist_ok=True)
    chartpath3 = datapath / "chart" / "sdvxIn"
    chartpath3.mkdir(parents=True, exist_ok=True)
    dbpath = datapath / "masterdb"
    dbpath.mkdir(parents=True, exist_ok=True)
    logpath = datapath / "log"
    logpath.mkdir(parents=True, exist_ok=True)
    pjsklogger.success("Directories successfully created.")

@pjsklogger.catch
def CreateDatabase():
    con = sqlite3.connect("./data/ProjectSekai/pjsk.db")
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS account (
qqid VARCHAR(11) PRIMARY KEY NOT NULL,
jpSekaiID VARCHAR(20),
twSekaiID VARCHAR(20),
enSekaiID VARCHAR(20)
)""")
    con.commit()
    con.close()
    pjsklogger.success("Database successfully created.")

@pjsklogger.catch
def CreateURLjson():
    jsonfile = Path("./data/ProjectSekai/config.json")
    try:
        jsonfile.touch(exist_ok=False)
    except FileExistsError:
        pjsklogger.error("\"config.json\" already exists. If you really want to reinitialize, please remove it manually.")
        # error message
        return
    text = """{
    "API":
    {
        "UnipjskAPI":
        {
            "jp":
            {
                "getsongid": "",
                "getalias2": "",
                "getevent": "",
                "rankmatch_by_user": "",
                "rankmatch_by_user": "",
                "profile": ""
            },
            "tw":
            {
                "getevent": "",
                "getevent_by_rank": "",
                "rankmatch_by_user": "",
                "rankmatch_by_user": "",
                "profile": ""
            },
            "en":
            {
                "getevent": "",
                "getevent_by_rank": "",
                "rankmatch_by_user": "",
                "rankmatch_by_user": "",
                "profile": ""
            }
        },
        "33Kit":
        {
            "jp_ycx": ""
        },
        "chart":
        {
            "sdvxIn": "",
            "sekai_best": ""
        },
        "masterDB":
        {
            "sekai_world":
            {
                "events":
                {
                    "jp": "",
                    "tw": "",
                    "en": ""
                },
                "rankmatch":{
                    "jp":
                    {
                        "seasons": "",
                        "grades": "",
                        "classes": "",
                        "tiers": ""
                    }
                }
            }
        },
        "realtimeDB":{
            "pjsekai_moe":
            {
                "musics": "",
                "musicDifficulties": ""
            }
        },
        "asset":{
            "sekai_best": ""
        }
    },
    "MESSAGE":
    {
        "ERROR":
        {
            "NO_MATCH": "????????????????????????????????????",
            "NO_BIND": "???????????????sekai ID???",
            "SERVER_ERROR": "???????????????",
            "TO_BE_CONRINUED": "?????????",
            "NO_URL": "Bot??????????????????????????????????????????????????????"
        },
        "ALIAS":
        {
            "GET_ALIAS": "Music: {title}\\nMatch:{match:.3f}\\nAlias:\\n"
        },
        "BIND":
        {
            "BIND_SUCCESS": "{bindid} - {username}???????????????"
        },
        "CHART":
        {
            "NO_DIFF": "Chart command:\\n/pjsk chart <song> (<difficulty>)",
            "WAIT_FOR_UPDATE": "??????????????????????????????????????????~"
        },
        "LINE":
        {
            "GET_LINE": "???{0}?????????{1}???{2} P",
            "SELF": "{username}:\\n??????????????????{score} P\\n??????????????????{rank}\\n",
            "EASTEREGG": "?????????????????????\\n",
            "LINEINFO": "??????{high}????????????{high_dist} P\\n?????????{low}??????{low_dist} P\\n",
            "PREDICTINFO": "??????{high}????????????{high_score} P\\n??????{low}????????????{low_score} P\\n",
            "MADAMADA": "?????????????????????????????????????????????\\n",
            "TIME": "???????????????????????????{day}???{hour}??????{minute}???{second}???\\n",
            "NONE": "???????????????????????????"
        },
        "PROFILE":
        {
            "USERDATA": "User: {username}\\n - {targetUserId}\\nRank: {userrank}\\nMusic Results:\\n{results}"
        },
        "RANKMATCH":
        {
            "NO_RANK": "??????????????????????????????",
            "USER": "User: {username} - {userid}\\n",
            "RANK": "{gradename} {classname} ({tierpoint})\\nRank: {ranking}\\n",
            "COUNT": "Win {wincount} | Draw {drawcount} | Lose {losecount}\\n",
            "WINRATE": "Winning rate: {win_rate}\\n",
            "MCWC": "max Consecutive Win Count: {mcwc}\\n"
        },
        "YCX":
        {
            "BEFORE_100": "100???????????????????????????????????????",
            "NOT_LINE": "??????????????????????????????",
            "EVENT": "???{event_id}?????????\\n - {eventName}\\n",
            "POINT": "{rank}??????????????????{rankPoint} P\\n",
        }
    }
}
"""
    jsonfile.write_text(text)
    pjsklogger.success("\"config.json\" successfully generated.")
