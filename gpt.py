import requests


def make_prompt(message: list) -> dict:
    json = {
        "messages": message,
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }
    return json


def make_message(role: str, content: str) -> dict:
    return {"role": role, "content": content}


def send_request(json: dict) -> requests.Response:
    url = "http://localhost:1234/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    response = requests.request("POST", url, json=json, headers=headers)
    return response


def get_request(answer: requests.Response) -> str:
    return answer.json()["choices"][0]["message"]["content"]
