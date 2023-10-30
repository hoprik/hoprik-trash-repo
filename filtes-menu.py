import os, time

# цвета & движок текста как у chat gpt (да я его фанат)
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


# брал анси цвета с сайта https://dvmn.org/encyclopedia/python_strings/ansi-codes/

def sleep_typing(text: str, time_sleep: int):
    now = ""
    _time = 0
    for word in text:
        if _time != len(text) - 1:
            print(word, end="")
        else:
            print(word, end="\n" + colors["CLEAR"])
        _time += 1
        now += word
        time.sleep(time_sleep / 1000)


# https://stackoverflow.com/questions/55406457/copying-to-os-clipboard-without-importing-i-e-clipboard-pyperclip-in-python взял от сюда

def copy(text):
    command = 'echo ' + text.strip() + '| clip'
    os.system(command)


# функции фильтров, а еще мне лень было придумывать поэтому взял все филтры с практикума
def upper(text: str):
    return text.upper()


def lower(text: str):
    return text.lower()


# взял из яндекс практикума
def camel(text: str):
    result = ""
    is_next_upper = False
    for i in range(len(text)):
        if text[i] == " ":
            is_next_upper = True
        elif is_next_upper:
            result += text[i].upper()
            is_next_upper = False
        else:
            result += text[i]
    return result


def crazy(text: str):
    now = ""
    is_upper = False
    for i in text:
        if is_upper:
            is_upper = False
            now += i.upper()
            continue
        is_upper = True
        now += i.lower()
    return now


def snake(text: str):
    return text.replace(" ", "_")


def smile_face(text: str):
    return text.replace(" ", "🙂")


# debug
# print(smile_face("привет малький мальчик!"))

filters = {
    "0": {
        "name": "БОЛЬШИЕ БУКВЫ",
        "description": "Делает буквы БОЛЬШИМИ",
        "func": upper
    },
    "1": {
        "name": "маленькие буквы",
        "description": "Делает буквы маленькими",
        "func": lower
    },
    "2": {
        "name": "верблюжийСтиль",
        "description": "Удаляет пробелы и следущие слово пишет с большой буквы",
        "func": camel
    },
    "3": {
        "name": "ЧеРеДовКа БуКв",
        "description": "Делает чередование заглавных и строчных букв",
        "func": crazy
    },
    "4": {
        "name": "Змеиный_стиль",
        "description": "Заменяет пробелы на нижную черту",
        "func": snake
    },
    "5": {
        "name": "Эмодзи стиль",
        "description": "Заменяет пробелы на улыбаешься смайлик",
        "func": smile_face
    },
    "6": {
        "name": "выход",
        "description": "Выход из программы"
    }
}

last = ""

sleep_typing(colors["YELLOW"] + """
создал программу:
             __ __   ___   ____  ____   ____  __  _ 
            |  |  | /   \ |    \|    \ |    ||  |/ ]
            |  |  ||     ||  o  )  D  ) |  | |  ' / 
            |  _  ||  O  ||   _/|    /  |  | |    \ 
            |  |  ||     ||  |  |    \  |  | |     |
            |  |  ||     ||  |  |  .  \ |  | |  .  |
            |__|__| \___/ |__|  |__|\_||____||__|\_|
                     и ООО "Пельманая хоприка"                               
""", 1)

sleep_typing(colors["LIGHT_BLUE"] + "Добро пожаловать в настройщик фильторов!", 5)

# главный цикл
while True:
    try:
        sleep_typing(colors["LIGHT_BLUE"] + "Выберете цифру фильтра", 1)
        count = 0
        for _filter, item in filters.items():
            # сорян просто к такому стилю уже привык
            sleep_typing(str(count) + ") " + colors["PURPLE"] + item["name"], 1)
            count += 1

        id_filter = int(input())
        answer = filters.get(str(id_filter), "error 888")

        # проверка на ошибки и выход
        if answer == "error 888":
            sleep_typing(colors["RED"] + "Ошибка! Не правильный id" + colors["CLEAR"], 1)
            continue
        if answer["name"] == "выход":
            sleep_typing(colors["LIGHT_BLUE"] + "Досвидания!", 1)
            exit()

        # описание
        sleep_typing("Описание: " + colors["LIGHT_BLUE"] + answer["description"], 1)

        # уточнение
        sure = input(colors["LIGHT_BLUE"] + "Вы уверены? да/нет\n")
        if sure.lower() == "да":
            text = ""
            # проверка есть ли в памяти программы уже переделанное предложение
            if last != "":
                sleep_typing(colors["LIGHT_BLUE"] + "Выберете действие:" + colors["CLEAR"], 1)
                sleep_typing("0) " + colors["PURPLE"] + "Bспользовать фильтр на старом тексте", 1)
                sleep_typing("1) " + colors["PURPLE"] + "Bспользовать фильтр на новом тексте", 1)

                choice = int(input())
                if choice == 0:
                    text = last
                else:
                    text = input(colors["LIGHT_BLUE"] + "Введите текст к которому применится фильтр: " + colors["CLEAR"])
            else:
                text = input(colors["LIGHT_BLUE"] + "Введите текст к которому применится фильтр: " + colors["CLEAR"])

            # рендер текста с фильтром
            sleep_typing(colors["LIGHT_BLUE"] + "Текст с примененым фильтром: " + colors["CLEAR"] + answer["func"](text) +
                         "\n" + colors["LIGHT_BLUE"] + "текст был скопирован в буффер обмена", 1)
            # замена прошлого рендара, новым
            last = answer["func"](text)
            # копирование рендара
            copy(last)

        else:
            continue
    except Exception as e:
        sleep_typing(colors["RED"]+"НЕИЗВЕСТНАЯ ОШИБКА ВОЗРАЩЕНИЕ В НАЧАЛО ЦИКЛА")