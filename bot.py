import asyncio
import os
from aiogram import Bot, Dispatcher, html, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Filter
from aiogram.types import Message

import main

# Load the bot token from a file
with open("token.txt") as file:
    TOKEN = file.readline().strip().split("|")[1]

# Define the folder where the videos will be saved
STORIES_FOLDER = 'stories'

# Create the folder if it doesn't exist
if not os.path.exists(STORIES_FOLDER):
    os.makedirs(STORIES_FOLDER)


def get_file_id():
    only_files = next(os.walk(STORIES_FOLDER))[2]
    return len(only_files)


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
        await self.bot.download_file(file.file_path, os.path.join(STORIES_FOLDER, f"{get_file_id()+1}-{username}.mp4"))
        await message.answer("Video downloaded successfully!")

    # Main function to start the bot
    async def main(self) -> None:
        self.dp.startup.register(lambda: None)  # Register startup actions if needed
        await self.dp.start_polling(self.bot)


# Entry point of the script
if __name__ == "__main__":
    asyncio.run(main.start())
    app = BotApp(TOKEN)
    asyncio.run(app.main())
