from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot import get_bots
from pathlib import Path
from ..logger import pjsklogger
from .ntfy import Notify
from .utils import SendMessage

@pjsklogger.catch
async def Its_25ji_now(at=False):
    imagepath = Path(".") / "data" / "ProjectSekai" / "assets" / "Sleep_not_allowed.png"
    imagepath = imagepath.resolve().as_uri()
    message = MessageSegment.image(imagepath)
    if at:
        message = MessageSegment.at("all") + message
    try:
        await SendMessage("group", int(114514), message) # Replace with the group number
        pjsklogger.success("不准睡！")
        return
    except ActionFailed as e:
        pjsklogger.error("Send sleep-not-allowed failed. Error:{}".format(e.info["msg"]))
        await Notify("Send sleep-not-allowed failed. Error:{}".format(e.info["msg"]))

