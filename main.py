import engine, json
from PIL import ImageFilter, Image
from fuzzywuzzy import fuzz

# переменные

_mode = -1
_mode_list = {
    "1": [1, "meme_mode"],
    "2": [2, "photo_mode"],
    "3": [3, "all_mode"],
    "4": [4, "exit"],
    "5": [-1, 0]
}

filters = {
    "meme_mode": [
        engine.Text("test"),
        engine.DeadInside("test")
    ]
}

console = engine.Console()


def getFilters(mode):
    if mode == 1:
        return [
            engine.Text(_lang["desc_text"]),
            engine.DeadInside(_lang["desc_ded_inside"]),
            engine.Barbi(_lang["desc_barbi"]),
            engine.Shlakl(_lang["desc_shukal"]),
            engine.Kletki("exit")
        ]
    if mode == 2:
        return [
            engine.Blur(_lang["desc_blur"]),
            engine.Inversion(_lang["desc_inversion"]),
            engine.Kletki(_lang["desc_kletki"]),
            engine.Kletki("exit")
        ]
    if mode == 3:
        return [
            engine.Text(_lang["desc_text"]),
            engine.DeadInside(_lang["desc_ded_inside"]),
            engine.Barbi(_lang["desc_barbi"]),
            engine.Shlakl(_lang["desc_shukal"]),
            engine.Blur(_lang["desc_blur"]),
            engine.Inversion(_lang["desc_inversion"]),
            engine.Kletki(_lang["desc_kletki"]),
            engine.Kletki("exit")
        ]


def getPath():
    global _sure_list, _lang
    console.writeN(console.color("red")+_lang["choice_photo"])
    data = console.openFileDialog()
    if data != "":
        console.writeN(console.color("green")+_lang["choice_photo_give"].replace("%s", data))
        if console.sure(_lang):
            return data
    getPath()


def modef():
    global _mode_list, _mode, _lang
    if _mode == -1:
        console.writeN(console.color("purple")+_lang["mode_choice"])
        mode_int = input()
        try:
            return _mode_list[mode_int][0]
        except Exception:
            modef()


def menu(mode):
    if _mode_list[str(mode)][1] == "exit":
        exit()
    console.writeN(console.color("purple")+_lang[_mode_list[str(mode)][1]])
    count = _lang[_mode_list[str(mode)][1]].split(")")
    console.writeN(console.color("purple")+_lang["exit_mode"].replace("%s", str(len(count))))
    activate(_mode)


def img_menu(img: Image.Image):
    choice = int(input())
    try:
        if choice == 1:
            img.show(title="image")
        if choice == 2:
            save = console.saveFileDialog()
            img.save(save)
        if choice == 3:
            return
    except:
        console.writeN("Ошибка")
    img_menu(img)


def activate(mode):
    global _mode
    choice = int(input())
    try:
        if getFilters(mode)[choice - 1].description() == "exit":
            _mode = -1
            model = modef()
            menu(model)
            return
        console.writeN(console.color("red")+_lang["description_filter"] + getFilters(mode)[choice - 1].description())
    except Exception:
        console.writeN(console.color("red")+_lang["error"])
        activate(mode)
    if not console.sure(_lang):
        return menu(mode)
    data = getPath()
    img = getFilters(mode)[choice - 1].aplay(Image.open(data))
    console.writeN(console.color("purple")+_lang["menu_img"])
    img_menu(img)
    menu(mode)


_lang = engine.return_lang()

console.writeN(console.color("YELLOW") + f"""
{_lang["create_program"]}
     __ __   ___   ____  ____   ____  __  _
    |  |  | /   \ |    \|    \ |    ||  |/ ]
    |  |  ||     ||  o  )  D  ) |  | |  ' /
    |  _  ||  O  ||   _/|    /  |  | |    \\
    |  |  ||     ||  |  |    \  |  | |     |
    |  |  ||     ||  |  |  .  \ |  | |  .  |
    |__|__| \___/ |__|  |__|\_||____||__|\_|
          {_lang["intro"]}
""")

console.writeN(console.color("green")+_lang["welcome"])

_mode = modef()
menu(_mode)
