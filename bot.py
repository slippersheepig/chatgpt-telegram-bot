import os
import asyncio
import json
from pathlib import Path
from dotenv import dotenv_values
from telebot.async_telebot import AsyncTeleBot
from revChatGPT.Unofficial import Chatbot

# get config
parent_dir = Path(__file__).resolve().parent
config = dotenv_values(f"{parent_dir}/.env")

# init telegram bot
BOT_TOKEN = config["BOT_TOKEN"]
bot = AsyncTeleBot(BOT_TOKEN, parse_mode="MARKDOWN")

# init chatbot
with open("config.json", "r") as f: config = json.load(f)
chatbot = Chatbot(config)
print("初始化机器人，请稍后")

# define a message handler to send a message when the command /start is issued
@bot.message_handler(commands=["start", "hello"])
async def send_welcome(message):
    await bot.reply_to(message, "This bot uses the browser based ChatGPT, responses may very slow")

@bot.message_handler(func=lambda m: True)
async def send_gpt(message):
    print("获取AI回复")
#   await bot.send_chat_action(message.chat.id, 'typing')
#   await bot.send_message(message.chat.id, "思考中，请稍后")
    response = chatbot.ask(message.text)
    await bot.reply_to(message, response["message"])


# run the bot
asyncio.run(bot.polling())
