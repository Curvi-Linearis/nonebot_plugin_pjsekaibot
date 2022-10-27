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
            "NO_MATCH": "请检查输入内容是否有误哦",
            "NO_BIND": "没有绑定到sekai ID。",
            "SERVER_ERROR": "服务器错误",
            "TO_BE_CONRINUED": "开发中",
            "NO_URL": "Bot主人对此功能的配置错误或还未完成配置"
        },
        "ALIAS":
        {
            "GET_ALIAS": "Music: {title}\\nMatch:{match:.3f}\\nAlias:\\n"
        },
        "BIND":
        {
            "BIND_SUCCESS": "{bindid} - {username}绑定成功！"
        },
        "CHART":
        {
            "NO_DIFF": "Chart command:\\n/pjsk chart <song> (<difficulty>)",
            "WAIT_FOR_UPDATE": "谱面还没有准备好，请等待更新~"
        },
        "LINE":
        {
            "GET_LINE": "第{0}名为：{1}，{2} P",
            "SELF": "{username}:\\n你的分数为：{score} P\\n你的排名为：{rank}\\n",
            "EASTEREGG": "我超，榜一佬！\\n",
            "LINEINFO": "距离{high}名线还有{high_dist} P\\n已超过{low}名线{low_dist} P\\n",
            "PREDICTINFO": "预测{high}名线为：{high_score} P\\n预测{low}名线为：{low_score} P\\n",
            "MADAMADA": "再加把劲！牌牌马上就到你身边！\\n",
            "TIME": "距离活动结束还有：{day}天{hour}小时{minute}分{second}秒\\n",
            "NONE": "你似乎还没打活动呢"
        },
        "PROFILE":
        {
            "USERDATA": "User: {username}\\n - {targetUserId}\\nRank: {userrank}\\nMusic Results:\\n{results}"
        },
        "RANKMATCH":
        {
            "NO_RANK": "没有查询到排位信息。",
            "USER": "User: {username} - {userid}\\n",
            "RANK": "{gradename} {classname} ({tierpoint})\\nRank: {ranking}\\n",
            "COUNT": "Win {wincount} | Draw {drawcount} | Lose {losecount}\\n",
            "WINRATE": "Winning rate: {win_rate}\\n",
            "MCWC": "max Consecutive Win Count: {mcwc}\\n"
        },
        "YCX":
        {
            "BEFORE_100": "100以前的排名没有提供预测线。",
            "NOT_LINE": "请求不是合法的榜线。",
            "EVENT": "第{event_id}期活动\\n - {eventName}\\n",
            "POINT": "{rank}名预测线为：{rankPoint} P\\n",
        }
    }
}
"""
    jsonfile.write_text(text)
    pjsklogger.success("\"config.json\" successfully generated.")
