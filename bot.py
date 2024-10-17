import asyncio
import os
from aiogram import Bot, Dispatcher, html, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Filter, Command
from aiogram.types import Message

import apiStory

# Load the bot token from a file
with open("token.txt") as file:
    TOKEN = file.readline().strip().split("|")[1]

# Define the folder where the videos will be saved
STORIES_FOLDER = 'stories'

# Create the folder if it doesn't exist
if not os.path.exists(STORIES_FOLDER):
    os.makedirs(STORIES_FOLDER)


def get_file_id():
    return len(os.listdir("stories"))


def get_name_files():
    text = ""
    for i in os.listdir("stories"):
        if i != "story.txt":
            file = i.split(".")[0].split("-")
            file_id = file[0]
            author = file[1]
            text += f"file: {file_id} author: {author}\n"
    return text


# Custom filter for video messages
class Video(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.content_type == types.ContentType.VIDEO


class BotApp:
    def __init__(self, token: str):
        self.bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        self.dp = Dispatcher()

        # Command handler for the /start command
        self.dp.message(CommandStart())(self.command_start_handler)
        self.dp.message(Command("fileList"))(self.command_get_video_list)
        self.dp.message(Command("sendStory"))(self.command_send_story)
        # Video message handler
        self.dp.message(Video())(self.video_handler)

    # Command handler for the /start command
    async def command_start_handler(self, message: Message) -> None:
        await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")

    # Video message handler
    async def video_handler(self, message: Message) -> None:
        video = message.video
        file_id = video.file_id
        file = await self.bot.get_file(file_id)
        username = message.from_user.username
        if message.forward_from:
            username = message.forward_from.username
        file_id_in_system = get_file_id()
        await self.bot.download_file(file.file_path,
                                     os.path.join(STORIES_FOLDER, f"{file_id_in_system}-{username}.mp4"))
        await message.answer("Видео было успешной скачано")

    async def command_get_video_list(self, message: Message) -> None:
        await message.answer(get_name_files())

    async def command_send_story(self, message: Message) -> None:
        story_id = apiStory.update_story()
        story, author = apiStory.find_story(story_id)
        await apiStory.main(story, author)
        await message.answer("Видео было отправлено!")

    # Main function to start the bot
    async def main(self) -> None:
        self.dp.startup.register(lambda: None)  # Register startup actions if needed
        await self.dp.start_polling(self.bot)


# Entry point of the script
if __name__ == "__main__":
    app = BotApp(TOKEN)
    asyncio.run(app.main())
