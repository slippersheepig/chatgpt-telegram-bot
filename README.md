A branch for bot to interact with chatgpt official api ( comes with [n3d1117](https://github.com/n3d1117/chatgpt-telegram-bot) and [acheong08](https://github.com/acheong08/ChatGPT) ), with showing typing status support
### Configuration
Customize the configuration by create a file named `.env`, then editing the settings as desired:
```bash
OPENAI_EMAIL="<YOUR_OPENAI_EMAIL>"
OPENAI_PASSWORD="<YOUR_OPENAI_PASSWORD>"
TELEGRAM_BOT_TOKEN="<YOUR_TELEGRAM_BOT_TOKEN>"
```
* `OPENAI_EMAIL,OPENAI_PASSWORD`: Your OpenAI credentials (these are only sent to the OpenAI server to periodically refresh the access token and never shared). You can read more about it [here](https://github.com/acheong08/ChatGPT)
* `TELEGRAM_BOT_TOKEN`: Your Telegram bot's token, obtained using [BotFather](http://t.me/botfather) (see [tutorial](https://core.telegram.org/bots/tutorial#obtain-your-bot-token))

Additional optional (but recommended) configuration values:
```bash
ALLOWED_TELEGRAM_USER_IDS="<USER_ID_1>,<USER_ID_2>,..." # Defaults to "*"
```
* `ALLOWED_TELEGRAM_USER_IDS`: A comma-separated list of Telegram user IDs that are allowed to interact with the bot (use [getidsbot](https://t.me/getidsbot) to find your user ID). **Important**: by default, *everyone* is allowed (`*`)

### Usage
Create a file named `docker-compose.yml`(same directory as `.env`)
```bash
services:
  chatgpt:
    image: sheepgreen/chatgpt:proxy #for arm, use chatgpt:proxyarmarm
    container_name: chatgpt
#    environment:
#      - CHATGPT_BASE_URL=YOUR_PROXY_ENDPOINT(by default uses the author's, may have problems sometimes)
    volumes:
      - ./.env:/home/appuser/.env
    restart: always
```
Then run `docker-compose up -d`,that's all!
