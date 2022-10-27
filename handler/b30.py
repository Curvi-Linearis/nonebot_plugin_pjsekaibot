from nonebot.exception import SkippedException, MatcherException
from nonebot.adapters.onebot.v11 import Event, MessageSegment
from nonebot.adapters.onebot.v11.message import Message
from nonebot.params import RawCommand
from nonebot.utils import run_sync
from ..logger import pjsklogger
from ..matcher import sekai, twsekai
from ..modules.utils import Get_response, Fetch_id, SpaceRecog, ReadConfig
from ..modules.imagemodules import DeleteByURI
from sqlite3 import OperationalError
import requests, json, time
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
from asyncio import sleep


def fcrank(playlevel, rank):
    if playlevel <= 32:
        return rank - 1.5
    # elif rank == 33:
    #     return rank - 0.5
    else:
        return rank - 1

async def pjskb30(qqid, server = "jp"):
    # Code basd on https://github.com/watagashi-uni/Unibot
    configJson = ReadConfig()
    rootpath = Path(".") / "data" / "ProjectSekai"

    try:
        targetUserId = Fetch_id(qqid, server)
    except OperationalError:
        pjsklogger.warning(f"{qqid} not in database.")
        return

    try:
        url = configJson["API"]["UnipjskAPI"][server]["profile"].format(targetUserId=targetUserId)
    except KeyError:
        pjsklogger.error(f"config.json is corrupted. Check if [\"API\"][\"UnipjskAPI\"][{server}][\"profile\"] exists.")
        return

    if url == "":
        pjsklogger.error("Query can not finish because you didn't register profile api in config.json.")
        return

    try:
        response_json = await Get_response(url)
        if response_json == {}:
            pjsklogger.warning(f"The response is empty. Request {server}_id: {targetUserId}")
            raise Exception
    except:
        pjsklogger.warning(f"Server error when handling b30 of {qqid}")
        return

    data = response_json
    name = data['user']['userGamedata']['name']
    userProfileHonors = data['userProfileHonors']
    rank = data['user']['userGamedata']['rank']
    userDecks = [0, 0, 0, 0, 0]
    special_training = [False, False, False, False, False]
    for i in range(0, 5):
        userDecks[i] = data['userDecks'][0][f'member{i + 1}']
        for userCards in data['userCards']:
            if userCards['cardId'] != userDecks[i]:
                continue
            if userCards['defaultImage'] == "special_training":
                special_training[i] = True

    b30path = rootpath / "assets" / "Unipjsk" / "b30.png"
    pic = Image.open(b30path.as_posix())
    try:
        with open('masterdata/cards.json', 'r', encoding='utf-8') as f:
            cards = json.load(f)
    except:
        # 摸了
        pass
    try:
        assetbundleName = ''
        for i in cards:
            if i['id'] == userDecks[0]:
                assetbundleName = i['assetbundleName']
        if special_training[0]:
            cardimg = Image.open(f'{assetpath}/startapp/thumbnail/chara/{assetbundleName}_after_training.png')
            cutoutimg = Image.open(f'{assetpath}/startapp/character/member_cutout_trm/{assetbundleName}/after_training.png')
        else:
            cardimg = Image.open(f'{assetpath}/startapp/thumbnail/chara/{assetbundleName}_normal.png')
            cutoutimg = Image.open(f'{assetpath}/startapp/character/member_cutout_trm/{assetbundleName}/normal.png')
        cutoutimg = cutoutimg.resize((int(cutoutimg.size[0]*0.47), int(cutoutimg.size[1]*0.47)))
        r, g, b, mask = cutoutimg.split()
        pic.paste(cutoutimg, (770, 15), mask)

        cardimg = cardimg.resize((116, 116))
        r, g, b, mask = cardimg.split()
        pic.paste(cardimg, (68, 70), mask)
    except:
        pass
    draw = ImageDraw.Draw(pic)
    
    fontpath = rootpath / "assets"
    
    font_style = ImageFont.truetype((fontpath / "SourceHanSansCN-Bold.otf").as_posix(), 35)
    draw.text((215, 65), name, fill=(0, 0, 0), font=font_style)
    font_style = ImageFont.truetype((fontpath / "FOT-RodinNTLGPro-DB.ttf").as_posix(), 15)
    draw.text((218, 118), 'id:' + targetUserId, fill=(0, 0, 0), font=font_style)
    font_style = ImageFont.truetype((fontpath / "FOT-RodinNTLGPro-DB.ttf").as_posix(), 28)
    draw.text((314, 150), str(rank), fill=(255, 255, 255), font=font_style)

    try:
        for i in userProfileHonors:
            if i['seq'] == 1:
                try:
                    honorpic = generatehonor(i, True, server)
                    honorpic = honorpic.resize((226, 48))
                    r, g, b, mask = honorpic.split()
                    pic.paste(honorpic, (59, 226), mask)
                except:
                    pass
    
        for i in userProfileHonors:
            if i['seq'] == 2:
                try:
                    honorpic = generatehonor(i, False, server)
                    honorpic = honorpic.resize((107, 48))
                    r, g, b, mask = honorpic.split()
                    pic.paste(honorpic, (290, 226), mask)
                except:
                    pass

        for i in userProfileHonors:
            if i['seq'] == 3:
                try:
                    honorpic = generatehonor(i, False, server)
                    honorpic = honorpic.resize((107, 48))
                    r, g, b, mask = honorpic.split()
                    pic.paste(honorpic, (403, 226), mask)
                except:
                    pass
    except:
        # 摸了
        pass

    
    with open((rootpath /  "masterdb" / "musicDifficulties.json").as_posix(), 'r', encoding='utf-8') as f:
        diff = json.load(f)
    for i in range(0, len(diff)):
        try:
            diff[i]['playLevelAdjust']
        except KeyError:
            diff[i]['playLevelAdjust'] = 0
            diff[i]['fullComboAdjust'] = 0
            diff[i]['fullPerfectAdjust'] = 0
    for i in range(0, len(diff)):
        diff[i]['result'] = 0
        diff[i]['rank'] = 0
        diff[i]['fclevel+'] = diff[i]['playLevel'] + diff[i]['fullComboAdjust']
        diff[i]['aplevel+'] = diff[i]['playLevel'] + diff[i]['fullPerfectAdjust']
    if server == 'jp':
        diff.sort(key=lambda x: x["aplevel+"], reverse=True)
        highest = 0
        for i in range(0, 30):
            highest = highest + diff[i]['aplevel+']
        highest = round(highest / 30, 2)
    with open((rootpath / "masterdb" / 'musics.json').as_posix(), 'r', encoding='utf-8') as f:
        musics = json.load(f)
    for music in data['userMusicResults']:
        playResult = music['playResult']
        musicId = music['musicId']
        musicDifficulty = music['musicDifficulty']
        i = 0
        found = False
        for i in range(0, len(diff)):
            if diff[i]['musicId'] == musicId and diff[i]['musicDifficulty'] == musicDifficulty:
                found = True
                break
        if found:
            if playResult == 'full_perfect':
                diff[i]['result'] = 2
                diff[i]['rank'] = diff[i]['aplevel+']
            elif playResult == 'full_combo':
                if diff[i]['result'] < 1:
                    diff[i]['result'] = 1
                    diff[i]['rank'] = fcrank(diff[i]['playLevel'], diff[i]['fclevel+'])

    diff.sort(key=lambda x: x["rank"], reverse=True)
    rank = 0
    shadow = Image.new("RGBA", (320, 130), (0, 0, 0, 0))
    shadow.paste(Image.new("RGBA", (310, 120), (0, 0, 0, 50)), (5, 5))
    shadow = shadow.filter(ImageFilter.GaussianBlur(3))
    #if server == 'en':
    #    with open('../enapi/masterdata/musics.json', 'r', encoding='utf-8') as f:
    #        musics = json.load(f)
    for i in range(0, 30):
        rank = rank + diff[i]['rank']
        single = b30single(diff[i], musics)
        r, g, b, mask = shadow.split()
        pic.paste(shadow, ((int(52 + (i % 3) * 342)), int(307 + int(i / 3) * 142)), mask)
        pic.paste(single, ((int(53+(i%3)*342)), int(309+int(i/3)*142)))
    rank = round(rank / 30, 2)

    font_style = ImageFont.truetype((fontpath / "SourceHanSansCN-Medium.otf").as_posix(), 16)
    if server == 'jp':
        textadd = f'，当前理论值为{highest}'
    else:
        textadd = ''
    draw.text((50, 1722), f'注：33+FC权重减1，其他减1.5，非官方算法，仅供参考娱乐{textadd}', fill='#00CCBB',
              font=font_style)
    draw.text((50, 1752), '定数来源：https://profile.pjsekai.moe/  ※定数每次统计时可能会改变', fill='#00CCBB',
              font=font_style)
    rankimg = Image.new("RGBA", (120, 55), (100, 110, 180, 0))
    draw = ImageDraw.Draw(rankimg)
    font_style = ImageFont.truetype((fontpath / "SourceHanSansCN-Bold.otf").as_posix(), 35)
    text_width = font_style.getsize(str(rank))
    # 硬核画文字边框
    draw.text((int(60 - text_width[0] / 2) + 3, int(20 - text_width[1] / 2)), str(rank), fill=(61, 74, 162, 210),
              font=font_style)
    draw.text((int(60 - text_width[0] / 2) - 3, int(20 - text_width[1] / 2)), str(rank), fill=(61, 74, 162, 210),
              font=font_style)
    draw.text((int(60 - text_width[0] / 2), int(20 - text_width[1] / 2) + 3), str(rank), fill=(61, 74, 162, 210),
              font=font_style)
    draw.text((int(60 - text_width[0] / 2), int(20 - text_width[1] / 2) - 3), str(rank), fill=(61, 74, 162, 210),
              font=font_style)
    draw.text((int(60 - text_width[0] / 2) - 2, int(20 - text_width[1] / 2) - 2), str(rank), fill=(61, 74, 162, 210),
              font=font_style)
    draw.text((int(60 - text_width[0] / 2) + 2, int(20 - text_width[1] / 2) + 2), str(rank), fill=(61, 74, 162, 210),
              font=font_style)
    draw.text((int(60 - text_width[0] / 2) - 2, int(20 - text_width[1] / 2) + 2), str(rank), fill=(61, 74, 162, 210),
              font=font_style)
    draw.text((int(60 - text_width[0] / 2) + 2, int(20 - text_width[1] / 2) - 2), str(rank), fill=(61, 74, 162, 210),
              font=font_style)
    rankimg = rankimg.filter(ImageFilter.GaussianBlur(1.2))
    draw = ImageDraw.Draw(rankimg)
    draw.text((int(60 - text_width[0] / 2), int(20 - text_width[1] / 2)), str(rank), fill=(255, 255, 255), font=font_style)
    r, g, b, mask = rankimg.split()
    pic.paste(rankimg, (565, 142), mask)
    # pic.show()
    pic = pic.convert("RGB")
    cacheImageName = "temp" + str(int(time.time())) + ".png"
    cachepath = rootpath / "cache" / cacheImageName
    pic.save(fp=cachepath.resolve().as_posix())
    pjsklogger.debug("B30 generation succeed. path: {}".format(cachepath.as_posix()))
    pic.close()
    return cachepath.resolve().as_uri()


def b30single(diff, musics):
    color = {
        'master': (187, 51, 238),
        'expert': (238, 67, 102),
        'hard': (254, 170, 0),
        'normal': (51, 187, 238),
        'easy': (102, 221, 17),
    }
    musictitle = ''
    rootpath = Path(".") / "data" / "ProjectSekai"
    fontpath = rootpath / "assets" 
    thumbnailpath = rootpath / "assets" / "Sekaibest" / "thumbnail" / "music_jacket_rip"
    for j in musics:
        if j['id'] == diff['musicId']:
            musictitle = j['title']
    pic = Image.new("RGB", (620, 240), (255, 255, 255))
    if diff['result'] == 2 or diff['result'] == 1:
        draw = ImageDraw.Draw(pic)
        font = ImageFont.truetype((fontpath / 'YuGothicUI-Semibold.ttf').as_posix(), 48)
        size = font.getsize(musictitle)
        if size[0] > 365:
            musictitle = musictitle[:int(len(musictitle)*(345/size[0]))] + '...'
        draw.text((238, 84), musictitle, '#000000', font)
        # print(musictitle, font.getsize(musictitle))

        thumbnailpath = Path('./data/ProjectSekai/assets/Sekaibest/thumbnail/music_jacket_rip/jacket_s_{str(diff["musicId"]).zfill(3)}.png')
        pjsklogger.warning(thumbnailpath.exists())
        jacket = Image.open(thumbnailpath.as_posix())
        jacket = jacket.resize((186, 186))
        pic.paste(jacket, (32, 28))

        draw.ellipse((5, 5, 5+60, 5+60), fill=color[diff['musicDifficulty']])
        font = ImageFont.truetype((fontpath / 'SourceHanSansCN-Bold.otf').as_posix(), 38)
        text_width = font.getsize(str(diff['playLevel']))
        text_coordinate = (int(36 - text_width[0] / 2), int(28 - text_width[1] / 2))
        draw.text(text_coordinate, str(diff['playLevel']), (255, 255, 255), font)

        draw.ellipse((242, 32, 286, 76), fill=color[diff['musicDifficulty']])
        draw.rectangle((262, 32, 334, 76), fill=color[diff['musicDifficulty']])
        draw.ellipse((312, 32, 356, 76), fill=color[diff['musicDifficulty']])


        picpath = rootpath / "assets" /"Unipjsk"
        if diff['playLevelAdjust'] != 0:
            if diff['result'] == 2:
                resultpic = Image.open((picpath / 'AllPerfect.png').as_posix())
                draw.text((259, 24), str(round(diff['aplevel+'], 1)), (255, 255, 255), font)
                draw.text((370, 24), '→ ' + str(round(diff['aplevel+'], 1)), (0, 0, 0), font)
            if diff['result'] == 1:
                resultpic = Image.open((picpath / 'FullCombo.png').as_posix())

                draw.text((259, 24), str(round(diff['fclevel+'], 1)), (255, 255, 255), font)
                draw.text((370, 24), '→ ' + str(round(fcrank(diff['playLevel'], diff["fclevel+"]), 1)), (0, 0, 0), font)
        else:
            if diff['result'] == 2:
                resultpic = Image.open((picpath / 'AllPerfect.png').as_posix())
                draw.text((259, 24), f'{round(diff["aplevel+"], 1)}.?', (255, 255, 255), font)
                draw.text((370, 24), f'→ {round(diff["aplevel+"], 1)}.0', (0, 0, 0), font)
            if diff['result'] == 1:
                resultpic = Image.open((picpath / 'FullCombo.png').as_posix())
                draw.text((259, 24), f'{round(diff["fclevel+"], 1)}.?', (255, 255, 255), font)
                draw.text((370, 24), f'→ {round(fcrank(diff["playLevel"], diff["fclevel+"]), 1)}', (0, 0, 0), font)
        r, g, b, mask = resultpic.split()
        pic.paste(resultpic, (238, 154), mask)
    pic = pic.resize((310, 120))
    return pic

@pjsklogger.catch(exclude = (SkippedException, MatcherException))
async def B30_jp(event: Event, cmd = RawCommand()):
    TextList = event.get_plaintext().split(" ")
    if not SpaceRecog(event.get_plaintext(), cmd = cmd) or (TextList[1] not in ["b30"]):
        await sekai.skip()
    configJson = ReadConfig()
    qqid = event.get_user_id()
    pjsklogger.debug("Calling func B30_jp, qqid:[\"{qqid}\"]")
    URI = await pjskb30(qqid)
    await sekai.send(MessageSegment.image(URI))
    await sleep(3)
    DeleteByURI(URI)
    pjsklogger.success("B30_jp Success.")
    await sekai.finish()

@pjsklogger.catch(exclude = (SkippedException, MatcherException))
async def B30_tw(event: Event, cmd = RawCommand()):
    TextList = event.get_plaintext().split(" ")
    if not SpaceRecog(event.get_plaintext(), cmd = cmd) or (TextList[1] not in ["b30"]):
        await twsekai.skip()
    configJson = ReadConfig()
    qqid = event.get_user_id()
    pjsklogger.debug("Calling func B30_tw, qqid:[\"{qqid}\"]")
    URI = await pjskb30(qqid, server="tw")
    await twsekai.send(MessageSegment.image(URI))
    await sleep(10)
    DeleteByURI(URI)
    pjsklogger.success("B30_tw Success.")
    await twsekai.finish()
