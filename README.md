> **Warning**
> Current deprecated due to Cloudflare protections
### Configuration
Customize the configuration by create a file named `.env`, then editing the settings as desired:
```bash
SESSION_TOKEN="<YOUR_OPENAI_SESSION_TOKEN>"
BOT_TOKEN="<YOUR_TELEGRAM_BOT_TOKEN>"
```
* `SESSION_TOKEN`: Your OpenAI session token. For instructions see [here](https://github.com/acheong08/ChatGPT/wiki/Setup#authentication)
* `BOT_TOKEN`: Your Telegram bot's token, obtained using [BotFather](http://t.me/botfather) (see [tutorial](https://core.telegram.org/bots/tutorial#obtain-your-bot-token))

### Usage
Create a file named `docker-compose.yml`(same directory as `.env`)
```bash
version: '3'
services:
  chatgpt:
    image: sheepgreen/chatgpt
    container_name: chatgpt
    volumes:
      - ./.env:/chatgpt/.env
    restart: always
```
Then run `docker-compose up -d`,that's all!
