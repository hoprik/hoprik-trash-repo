from math import trunc
from telethon import TelegramClient, functions, types
from telethon.sessions import StringSession
from videoprops import get_video_properties
import asyncio


def get_data_video(file: str):
    props = get_video_properties(file)
    return props["width"], props["height"], trunc(float(props["duration"]))


async def send_story(client: TelegramClient, filename: str, author: str):
    uploaded_file = await client.upload_file(filename)
    width, height, duration = get_data_video(filename)
    await client(functions.stories.SendStoryRequest(
        peer=types.InputPeerSelf(),
        media=types.InputMediaUploadedDocument(
            file=uploaded_file,
            mime_type='video/mp4',
            attributes=[
                types.DocumentAttributeVideo(duration=duration, w=width, h=height)
            ]
        ),
        privacy_rules=[types.InputPrivacyValueAllowAll()],
        caption=f'Видео от {author}',
    ))

    await client.send_message('me', 'Отправил историю!')


async def main(filename: str, author: str):
    with open("token.txt") as file:
        token = file.readline().split("|")[0]

    client = TelegramClient(StringSession(token), 28216737, "d3e76ec9f802203c2d7d98ae0e06030d")
    async with client:
        await send_story(client, filename, author)
