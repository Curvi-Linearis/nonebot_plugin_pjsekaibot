from nonebot.plugin import on_command
from nonebot.adapters.onebot.v11 import Event

async def whitelist(event: Event) -> bool:
    # white_list = ["114514", "1919180"]
    # return event.get_user_id in white_list
    return True

sekaiadmin = on_command("pjadmin",rule=whitelist, priority = 4)
sekai = on_command("pjsk", aliases = {"pj"}, priority = 5)
twsekai = on_command("twpjsk", aliases = {"twpj"}, priority = 5)
ensekai = on_command("enpjsk", aliases = {"enpj"}, priority = 5)
