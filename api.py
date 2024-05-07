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
        self.messages.append({"role": role, "message": message})

    def get_messages(self) -> [{}]:
        return self.messages


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

        url = f"https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        headers = {
            'Authorization': f'Bearer {self.iam_token}',
            'Content-Type': 'application/json'
        }
        data = {
            "modelUri": f"gpt://{self.folder_id}/{self.gpt}/latest",
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": 100
            },
            "messages": messages.get_messages()
        }

        response = requests.request("POST", url, data=data, headers=headers)

        if response.status_code == 200:
            result = response.json()['result']['alternatives'][0]['message']['text']
            token = response.json()['result']['usage']['totalTokens']
            return True, [result, token]
        elif response.status_code == 401:
            self.iam_token = get_token()
            return self.gpt_ask(messages)
        else:
            return False, "При запросе в YandexGpt возникла ошибка"

# made by hoprik
