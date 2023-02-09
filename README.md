## Update
2023.2.10
* Change to browser based ChatGPT by [acheong08](https://github.com/acheong08/ChatGPT), due to ChatGPT often gets overloaded, the responses may very slow
### Configuration
> `.env`, `config.json` and `docker-compose.yml` must be in the same directory

Customize the configuration by create a file named `.env`, then editing the settings as desired:
```bash
BOT_TOKEN="<YOUR_TELEGRAM_BOT_TOKEN>"
```
* `BOT_TOKEN`: Your Telegram bot's token, obtained using [BotFather](http://t.me/botfather) (see [tutorial](https://core.telegram.org/bots/tutorial#obtain-your-bot-token))

Customize the configuration by create a file named `config.json`, then editing the settings as desired:
```js
{
    "email": "<your openai email>",
    "password": "<your openai password>"
}
```

### Usage
Create a file named `docker-compose.yml`
```bash
version: '3'
services:
  chatgpt:
    image: sheepgreen/chatgpt
    container_name: chatgpt
    volumes:
      - ./config.json:/chatgpt/config.json
      - ./.env:/chatgpt/.env
    restart: always
```
Then run `docker-compose up -d`,that's all!
