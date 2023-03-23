> I found a great [project](https://github.com/wenLiangcan/chatgpt-telegram-bot) which also based on [n3d1117](https://github.com/n3d1117/chatgpt-telegram-bot) and [acheong08](https://github.com/acheong08/ChatGPT), thanks to his awesome job. You should use this instead of mine.

A branch for bot to interact with chatgpt official api ( comes with [n3d1117](https://github.com/n3d1117/chatgpt-telegram-bot) and [acheong08](https://github.com/acheong08/ChatGPT) ), with showing typing status and streaming responses support
### Configuration
Customize the configuration by create a file named `.env`, then editing the settings as desired (choose only one method ):
```bash
//method 1
OPENAI_EMAIL="<YOUR_OPENAI_EMAIL>"
OPENAI_PASSWORD="<YOUR_OPENAI_PASSWORD>"
//method 2
OPENAI_SESSION_TOKEN="<YOUR_OPENAI_SESSION_TOKEN>"
//method 3
OPENAI_ACCESS_TOKEN="<YOUR_OPENAI_ACCESS_TOKEN>"
//below is a must
TELEGRAM_BOT_TOKEN="<YOUR_TELEGRAM_BOT_TOKEN>"
```
* `OPENAI_EMAIL,OPENAI_PASSWORD`: Your OpenAI credentials (these are only sent to the OpenAI server to periodically refresh the access token and never shared). You can read more about it [here](https://github.com/acheong08/ChatGPT)
* `OPENAI_SESSION_TOKEN`: Follow steps below
1. Go to https://chat.openai.com/chat and open the developer tools by `F12`.
2. Find the `__Secure-next-auth.session-token` cookie in `Application` > `Storage` > `Cookies` > `https://chat.openai.com`.
3. Copy the value in the `Cookie Value` field.
* `OPENAI_ACCESS_TOKEN`: https://chat.openai.com/api/auth/session
* `TELEGRAM_BOT_TOKEN`: Your Telegram bot's token, obtained using [BotFather](http://t.me/botfather) (see [tutorial](https://core.telegram.org/bots/tutorial#obtain-your-bot-token))

Additional optional (but recommended) configuration values:
```bash
ALLOWED_TELEGRAM_USER_IDS="<USER_ID_1>,<USER_ID_2>,..." # Defaults to "*"
PROXY="<HTTP/HTTPS_PROXY>" # E.g. "http://localhost:8080", defaults to none
USE_STREAM=false # Defaults to true
```
* `ALLOWED_TELEGRAM_USER_IDS`: A comma-separated list of Telegram user IDs that are allowed to interact with the bot (use [getidsbot](https://t.me/getidsbot) to find your user ID). **Important**: by default, *everyone* is allowed (`*`)
* `PROXY`: Proxy to be used when authenticating with OpenAI
* `USE_STREAM`: Streams the response as the bot types. Set to `false` to only answer once the response is fully generated

### Usage
Create a file named `docker-compose.yml`(same directory as `.env`)
```bash
services:
  chatgpt:
    image: sheepgreen/chatgpt:proxy
    container_name: chatgpt
#    environment:
#      - CHATGPT_BASE_URL=YOUR_PROXY_ENDPOINT(by default uses the author's, may have problems sometimes)
    volumes:
      - ./.env:/home/appuser/.env
    restart: always
```
Then run `docker-compose up -d`,that's all!
