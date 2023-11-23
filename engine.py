import json
import time, tkinter, random
from tkinter import filedialog as fd
from fuzzywuzzy import fuzz
from PIL.Image import Image
from PIL import ImageFont, ImageDraw, ImageFilter, ImageOps

_sure_list = [
    [
        "да",
        "lf",
        "дап",
        "да\""
        "yes"
        "неы"
    ],
    [
        "нет",
        "ytn",
        "нет\\",
        "нетп"
        "no"
        "тщ"
    ],
    [
        "1",
        "russian",
        "русский"
        "ru",
        "ру",
        "кг",
        "he"
    ],
    [
        "2",
        "англиский",
        "русский"
        "en"
        "ен"
        "ty",
        "ут"
    ]
]


class Console:
    def bold(self):
        pass

    def color(self, color_text: str):
        colors = {
            "BLACK": "\u001b[30;1m",
            "RED": "\u001b[31;1m",
            "GREEN": "\u001b[32;1m",
            "YELLOW": "\u001b[33;1m",
            "BLUE": "\u001b[34;1m",
            "PURPLE": "\u001b[35;1m",
            "LIGHT_BLUE": "\u001b[36;1m",
            "WHITE": "\u001b[37;1m",
            "CLEAR": "\u001b[0m",
        }
        return colors[color_text.upper()]

    def clear(self):
        print("\u001b[2A")

    def writeN(self, text: str):
        print(text + self.color("clear"))

    def sleep_typing(self, text: str, time_sleep: int):
        now = ""
        _time = 0
        for word in text:
            if _time != len(text) - 1:
                print(word, end="")
            else:
                print(word, end="\n" + self.color("CLEAR"))
            _time += 1
            now += word
            time.sleep(time_sleep / 1000)

    def openFileDialog(self):
        tk = tkinter.Tk()
        tk.geometry("1x1")
        data = fd.askopenfilename()
        tk.destroy()
        return data

    def saveFileDialog(self):
        tk = tkinter.Tk()
        tk.geometry("1x1")
        data = fd.asksaveasfile(mode='w', defaultextension=".jpg")
        tk.destroy()
        return data

    def getString(self, text: str, ban_list_id: int, percent: int):
        for wold in _sure_list[ban_list_id]:
            if fuzz.ratio(text, wold) > percent:
                return True
        return False

    def sure(self, _lang):
        is_sure = input(self.color("red")+_lang["choice_sure"]+self.color("clear"))
        is_sure = is_sure.lower()
        if self.getString(is_sure, 0, 50) or console.getString(is_sure, 1, 50):
            if self.getString(is_sure, 0, 50):
                return True
        return False

    def getLang(self):
        console.writeN(self.color("yellow")+"Hello choose a language\n1) Russia \n2) English")
        data = input("")
        if console.getString(data, 2, 50):
            return json.load(open("translate.json", encoding="utf-8"))["ru"]
        elif console.getString(data, 3, 50):
            return json.load(open("translate.json", encoding="utf-8"))["en"]
        else:
            self.getLang()


console = Console()
_lang = console.getLang()

def return_lang():
    global _lang
    return _lang


class Filter:
    def __init__(self, text):
        self.text = text

    def aplay_pixel(self, pixel: tuple) -> int:
        raise NotImplementedError()

    def aplay(self, img: Image) -> Image:
        for i in range(img.width):
            for j in range(img.height):
                # получаем цвет
                pixel = img.getpixel((i, j))

                # как-либо меняем цвет
                new_pixel = self.aplay_pixel(pixel)

                # сохраняем пиксель обратно
                img.putpixel((i, j), new_pixel)
        return img

    def description(self):
        return self.text


class Text(Filter):

    def aplay(self, img: Image):
        image = img
        font = [
            "./font/Arial.ttf",
            "./font/Attractive-Heavy.ttf",
            "./font/Impact.ttf"
        ]
        console.writeN(_lang["text_write"])
        text = input()
        draw = ImageDraw.Draw(image)
        ttf = ImageFont.truetype(font[random.randint(0, 2)], 32)
        draw.text((img.width / 2, 200), text=text, fill="red", font=ttf)
        return image


class DeadInside(Filter):

    def aplay(self, img: Image):
        return img.convert("L")


class Barbi(Filter):

    def aplay_pixel(self, pixel: tuple) -> tuple:
        return 200, pixel[1], pixel[2]


class Shlakl(Filter):

    def aplay(self, img: Image) -> Image:
        resized_img = img.resize((img.width // 4, img.height // 4))
        return resized_img.resize((img.width * 4, img.height * 4))


class Blur(Filter):

    def aplay(self, img: Image) -> Image:
        try:
            sila = int(input(_lang["blur_stroung"]))
        except Exception:
            console.writeN(console.color("red")+_lang["error"])
            self.aplay(img)
        return img.filter(ImageFilter.GaussianBlur(sila))


class Inversion(Filter):

    def aplay(self, img: Image) -> Image:
        return ImageOps.invert(img)


class Kletki(Filter):

    def aplay(self, img: Image) -> Image:
        w, h = img.size
        for x in range(0, w, 2):
            for y in range(0, h, 2):
                l = img.getpixel((x, y))
                img.putpixel((x, y), (255 - l[0], 255 - l[1], 255 - l[2]))
        return img