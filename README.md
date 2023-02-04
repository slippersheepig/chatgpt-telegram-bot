A branch for bot to interact with chatgpt official api ( comes with [n3d1117](https://github.com/n3d1117/chatgpt-telegram-bot) and [acheong08](https://github.com/acheong08/ChatGPT) ), with showing typing status support
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

### Usage
Create a file named `docker-compose.yml`(same directory as `.env`)
```bash
version: '3'
services:
  chatgpt:
    image: sheepgreen/chatgpt:api #for arm, use chatgpt:apiarm
    container_name: chatgpt
    volumes:
      - ./.env:/home/appuser/.env
    restart: always
```
Then run `docker-compose up -d`,that's all!
