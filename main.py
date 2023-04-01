import logging
import os
import json
from dotenv import load_dotenv
from EdgeGPT import Chatbot as ChatGPT4Bot

from telegram_bot import ChatGPT4TelegramBot

with open('./cookie.json', 'r') as f:
    cookies = json.load(f)
def main():
    # Read .env file
    load_dotenv()

    # Setup logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    # Check if the required environment variables are set
    required_values = ['TELEGRAM_BOT_TOKEN']
    missing_values = [value for value in required_values if os.environ.get(value) is None]
    if len(missing_values) > 0:
        logging.error(f'The following environment values are missing in your .env: {", ".join(missing_values)}')
        exit(1)

    # Setup configuration
    telegram_config = {
        'token': os.environ['TELEGRAM_BOT_TOKEN'],
        'allowed_user_ids': os.environ.get('ALLOWED_TELEGRAM_USER_IDS', '*')
    }

    # Setup and run ChatGPT and Telegram bot
    gpt4_bot = ChatGPT4Bot(cookies=cookies)

    telegram_bot = ChatGPT4TelegramBot(config=telegram_config, gpt4_bot=gpt4_bot)
    telegram_bot.run()


if __name__ == '__main__':
    main()
