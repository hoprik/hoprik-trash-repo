import os
from math import trunc
from telethon import TelegramClient, functions, types
from telethon.sessions import StringSession
from videoprops import get_video_properties

async def send_story(client: TelegramClient, filename: str, author: str):
    uploaded_file = await client.upload_file(filename)
    await client(functions.stories.SendStoryRequest(
        peer=types.InputPeerSelf(),
        media=types.InputMediaUploadedDocument(
            file=uploaded_file,
            mime_type='video/mp4',
            attributes=[]
        ),
        privacy_rules=[types.InputPrivacyValueAllowAll()],
        caption=f'Видео от @{author}\n❗️Видео отправлено через hoprik story autouploader. Подробности в тгк❗️',
    ))

    await client.send_message('me', 'Отправил историю!')


async def main(filename: str, author: str):
    with open("token.txt") as file:
        token = file.readline().split("|")[0]

    client = TelegramClient(StringSession(token), 28216737, "d3e76ec9f802203c2d7d98ae0e06030d")
    async with client:
        await send_story(client, "stories/"+filename, author)


def update_story():
    with open("stories/story.txt", "r+") as f:
        story = f.read()
    with open("stories/story.txt", "w") as f:
        try:
            f.write(str(int(story)+1))
        except:
            f.write("1")
        f.close()
        return story


def find_story(story):
    files = os.listdir("stories")
    for i in files:
        file_id = i.split("-")[0]
        if story == file_id:
            return i, i.split("-")[1].split(".")[0]
    return ""
