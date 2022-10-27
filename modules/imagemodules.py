from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import time
import re
from ..logger import pjsklogger

def DisplayLen(string):
    EquivString = re.sub("[^\x00-\x7F]{1}", "**", string)
    return len(EquivString)

def AddNoise(image):
    noise = Image.effect_noise(image.size, 4).convert(mode="RGB")
    return Image.blend(image, noise, 0.1)

@pjsklogger.catch
def Txt2Img(text, withLF=False):
    if not withLF:  # Insert a line feed every 40 display characters
        cur = 0
        textWithLF = ""
        for i in text:
            if cur >= 40:
                textWithLF += "\n"
                cur = 0
            textWithLF += i
            if i.isascii():
                cur += 1
            else:
                cur += 2
        text = textWithLF
    textList = text.split("\n")
    LengthList = []
    for i in textList:
        LengthList.append(DisplayLen(i))
    width = 14 * max(LengthList) + 20 # an ASCII character is ~14 pixels wide
    height = 32 * len(LengthList) + 30 # an ASCII character is ~32 pixels high
    
    image = Image.new(mode = "RGB", size=(width, height))
    rootpath = Path(".") / "data" / "ProjectSekai"
    fontpath = rootpath / "assets" / "sarasa-mono-sc-regular.ttf"
    cacheImageName = "temp" + str(int(time.time())) + ".png"
    cachepath = rootpath / "cache" / cacheImageName
    if not fontpath.exists():
        pjsklogger.error("Font not exist. Check assets folder.")
        return
    font = ImageFont.truetype(fontpath.as_posix(), 25)
    draw = ImageDraw.Draw(image)
    draw.text((20, 20), text, font=font, encoding="UTF-8")
    image = AddNoise(image)
    image.save(fp=cachepath.resolve().as_posix())
    pjsklogger.debug("Txt2Img succeed. Image({}*{}). path: {}".format(str(width), str(height), cachepath.as_posix()))
    image.close()
    return cachepath.resolve().as_uri()

def DeleteByURI(URI: str, missing_ok=False):
    path = Path(URI.replace("file://", ""))
    try:
        path.unlink(missing_ok=missing_ok)
    except FileNotFoundError:
        pjsklogger.error(f"{URI} does not exist, please check.")
    return
