import requests


def get_token() -> str:
    url = "http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token"
    headers = {"Metadata-Flavor": "Google"}
    response = requests.request("GET", url, headers=headers)
    return response.json()["access_token"]


class API_YANDEX:
    def __init__(self, iam_token: str, folder_id: str):
        self.iam_token = iam_token
        self.folder_id = folder_id

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

# made by hoprik
