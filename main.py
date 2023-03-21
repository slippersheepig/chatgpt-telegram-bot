import os
import asyncio
from pathlib import Path
from dotenv import dotenv_values
from telebot.async_telebot import AsyncTeleBot
from revChatGPT.V3 import Chatbot

# get config
parent_dir = Path(__file__).resolve().parent

dotenv_values = dotenv_values(f"{parent_dir}/.env")
default_envs = {"OPENAI_MODEL": "gpt-3.5-turbo"}
config = {
    **default_envs,
    **dotenv_values
}

# init telegram bot
BOT_TOKEN = config["TELEGRAM_BOT_TOKEN"]
bot = AsyncTeleBot(BOT_TOKEN, parse_mode="MARKDOWN")

# init chatbot
chatbot = Chatbot(api_key=config["OPENAI_API_KEY"], engine=config["OPENAI_MODEL"])
print("initial bot...")

# define a message handler to send a message when the command /start is issued
@bot.message_handler(commands=["start", "hello"])
async def send_welcome(message):
    await bot.reply_to(message, "This bot uses the official ChatGPT API")

@bot.message_handler(func=lambda m: True)
async def send_gpt(message):
    print("get response...")
#   await bot.send_chat_action(message.chat.id, 'typing')
#   await bot.send_message(message.chat.id, "思考中，请稍后")
    response = chatbot.ask(message.text)
    await bot.reply_to(message, response)


# run the bot
asyncio.run(bot.polling())
