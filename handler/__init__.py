#from .config import ERROR, MESSAGE, PATH
#from .depend import static_data, parse_profile, get_class, get_response, fetch_id, get_song_id, FormatMusicID
#from .help import index
#from .bind import bind, got_bind, bind_tw, got_bind_tw, bind_en, got_bind_en
#from .profile import profile, profile_tw, profile_en
#from .rankmatch import rankmatch, rankmatch_tw, rankmatch_en
#from .alias import get_alias, got_alias
#from .chart import get_chart
#from .ycx import get_ycx
#from .line import get_line
#from ..matcher import sekai

from .admin import Init1, Init2
from .bind import Bind_jp, Got_bind_jp, Bind_tw, Got_bind_tw, Bind_en, Got_bind_en
from .profile import Parse_profile, Profile_jp, Profile_tw, Profile_en
from .chart import Get_chart
from .alias import Get_alias, Got_alias
from .line import Get_line_jp, Get_line_tw, Get_line_en
from .chartrank import Chartrank
from .ycx import Get_ycx
from .rankmatch import Rankmatch
from .help import Help
from .b30 import fcrank, pjskb30, b30single, B30_jp, B30_tw

# autotask
from nonebot import require
require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler
#import asyncio

from ..modules.downloader import Run_every_30_min, Run_every_1_day
#from ..modules.you_cannot_go_to_sleep import Its_25ji_now

scheduler.scheduled_job("cron", minute="*/30", id="pjsk1")(Run_every_30_min)
scheduler.scheduled_job("cron", day="*/1", id="pjsk2")(Run_every_1_day)
#scheduler.scheduled_job("cron", hour='1', id="pjsk3", jitter=5)(Its_25ji_now)

#loop = asyncio.get_event_loop()
#loop.run_until_complete(Run_every_30_min())
#result = loop.run_until_complete(Run_every_1_day())
#loop.close()
