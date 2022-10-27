from .logger import pjsklogger
from .matcher import sekaiadmin, sekai, twsekai, ensekai
from .handler_new import(
    Init1, Init2,
    Bind_jp, Got_bind_jp, Bind_tw, Got_bind_tw, Bind_en, Got_bind_en,
    Parse_profile, Profile_jp, Profile_tw, Profile_en,
    Get_chart,
    Get_alias, Got_alias,
    Get_line_jp, Get_line_tw, Get_line_en,
    Chartrank,
    Get_ycx,
    Rankmatch,
    Help,
    B30_jp, B30_tw,
        )
sekaiadmin.handle()(Init1)
sekaiadmin.handle()(Init2)
sekai.handle()(Get_alias)
sekai.got("name", prompt="请输入您要查找的歌名")(Got_alias)
sekai.handle()(Get_chart)
sekai.handle()(Chartrank)
sekai.handle()(Get_ycx)
sekai.handle()(Rankmatch)
sekai.handle()(Help)

sekai.handle()(Bind_jp)
sekai.got("id",prompt="请输入你的ID：")(Got_bind_jp)
sekai.handle()(Profile_jp)
sekai.handle()(Get_line_jp)
sekai.handle()(B30_jp)
twsekai.handle()(Bind_tw)
twsekai.got("twid",prompt="请输入你的ID：")(Got_bind_tw)
twsekai.handle()(Profile_tw)
twsekai.handle()(Get_line_tw)
twsekai.handle()(B30_tw)
ensekai.handle()(Bind_en)
ensekai.got("enid",prompt="请输入你的ID：")(Got_bind_en)
ensekai.handle()(Profile_en)
ensekai.handle()(Get_line_en)
