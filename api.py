import json

import requests


def get_token() -> str:
    url = "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token"
    headers = {"Metadata-Flavor": "Google"}
    response = requests.request("GET", url, headers=headers)
    return response.json()["access_token"]


class Messanger:
    def __init__(self):
        self.messages = []

    def add_message(self, role: str, message: str):
        self.messages.append({"role": role, "text": message})

    def get_messages(self) -> [{}]:
        return self.messages

    def get_messages_str(self) -> str:
        wrapper = {
            "messages": self.messages
        }
        return json.dumps(wrapper)

    def add_messages_by_json(self, messages: {"": [{}]}):
        for message in messages["messages"]:
            self.messages.append(message)

    def add_messages_by_string(self, messages: str):
        wrapper = json.loads(messages)
        self.add_messages_by_json(wrapper)


class API_YANDEX:
    def __init__(self, iam_token: str, folder_id: str, gpt: str):
        self.iam_token = iam_token
        self.folder_id = folder_id
        self.gpt = gpt

    def speech_to_text(self, data: bytes) -> (bool, str):
        """
        Функция для расшифравки (STT)
        :param data: байты файла
        :return: Ответ готовый, текст
        """
        params = {
            "lang": "ru-RU",
            "folderId": self.folder_id
        }

        headers = {
            "Content-Type": "audio/ogg",
            "Authorization": "Bearer " + self.iam_token
        }

        response = requests.post("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize", data=data, headers=headers,
                                 params=params)

        if response.status_code == 200:
            return True, response.json()["result"]
        elif response.status_code == 401:
            self.iam_token = get_token()
            return self.speech_to_text(data)
        else:
            return False, "Ошибка, текст не распознан!"

    def text_to_speech(self, text, voice='marina') -> (bool, bytes):
        """
        Функция для синтеза речи (TTS)
        :param text: текст синтеза
        :param voice: голос помощника
        :return: Ответ готовый, байты файла
        """

        headers = {
            "Authorization": "Bearer " + self.iam_token}
        data = {
            'text': text,
            'lang': 'ru-RU',
            'voice': voice,
            'folderId': self.folder_id
        }
        url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'

        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return True, response.content
        elif response.status_code == 401:
            self.iam_token = get_token()
            return self.text_to_speech(text, voice)
        else:
            return False, "При запросе в SpeechKit возникла ошибка"

    def gpt_ask(self, messages: Messanger) -> [bool, any]:
        """
        Функция для генерации ответа от ии
        :param messages: Сообщения от yandexgpt
        :return: Ответ готовый, значение
        """

        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.iam_token}",
        }
        payload = {
            "modelUri": "gpt://b1g18jbemvgi6dkjue7h/yandexgpt-lite",
            "completionOptions": {
                "stream": False,
                "temperature": 0.1,
                "maxTokens": "150"
            },
            "messages": messages.get_messages()
        }
        print(messages.get_messages())

        response = requests.request("POST", url, json=payload, headers=headers)

        print(response.text)

        if response.status_code == 200:
            result = response.json()['result']['alternatives'][0]['message']['text']
            token = response.json()['result']['usage']['totalTokens']
            return True, (result, token)
        elif response.status_code == 401:
            self.iam_token = get_token()
            return self.gpt_ask(messages)
        else:
            print(response.text)
            return False, "При запросе в YandexGpt возникла ошибка"

    def count_tokens(self, text: str) -> int:
        token = self.iam_token
        folder_id = self.folder_id
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        return len(
            requests.post(
                "https://llm.api.cloud.yandex.net/foundationModels/v1/tokenize",
                json={"modelUri": f"gpt://{folder_id}/yandexgpt/latest", "text": text},
                headers=headers
            ).json()['tokens'])
# made by hoprik
