> [n3d1117](https://github.com/n3d1117/chatgpt-telegram-bot) is back! Use this.
### Update
2023.3.2 Use official ChatGPT API
### A branch for bot to interact with chatgpt official api ( comes with [acheong08](https://github.com/acheong08/ChatGPT) )
### Configuration
Customize the configuration by create a file named `.env`, then editing the settings as desired:
```bash
OPENAI_API_KEY="<YOUR_OPENAI_API_KEY>"
TELEGRAM_BOT_TOKEN="<YOUR_TELEGRAM_BOT_TOKEN>"
```
* `OPENAI_API_KEY`: Your OpenAI api key. Steps to follow
1. Create account on [OpenAI](https://platform.openai.com/)
2. Go to https://platform.openai.com/account/api-keys
3. Copy API key
* `TELEGRAM_BOT_TOKEN`: Your Telegram bot's token, obtained using [BotFather](http://t.me/botfather) (see [tutorial](https://core.telegram.org/bots/tutorial#obtain-your-bot-token))

Additional optional configuration values:
```bash
OPENAI_MODEL="<ANY_MODEL_AVAILABLE_FROM_OPENAI>" # Defaults to "gpt-3.5-turbo"
```
### Usage
Create a file named `docker-compose.yml`(same directory as `.env`)
```bash
services:
  chatgpt:
    image: sheepgreen/chatgpt
    container_name: chatgpt
    volumes:
      - ./.env:/home/appuser/.env
    restart: always
```
Then run `docker-compose up -d`,that's all!
