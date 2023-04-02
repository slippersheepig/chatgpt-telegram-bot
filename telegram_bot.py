import asyncio
import collections
import logging

import telegram.constants as constants
from revChatGPT.V1 import AsyncChatbot as ChatGPT3Bot
from telegram import Update, Message
from telegram.error import RetryAfter
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters


class ChatGPT3TelegramBot:
    """
    Class representing a Chat-GPT3 Telegram Bot.
    """

    def __init__(self, config: dict, gpt3_bot: ChatGPT3Bot):
        """
        Initializes the bot with the given configuration and GPT-3 bot object.
        :param config: A dictionary containing the bot configuration
        :param gpt3_bot: The GPT-3 bot object
        """
        self.config = config
        self.gpt3_bot = gpt3_bot
        self.disallowed_message = "Sorry, you are not allowed to use this bot. You can check out the source code at " \
                                  "https://github.com/n3d1117/chatgpt-telegram-bot"

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Shows the help menu.
        """
        await update.message.reply_text("/start - Start the bot\n"
                                        "/reset - Reset conversation\n"
                                        "/help - Help menu\n\n"
                                        "Open source at https://github.com/n3d1117/chatgpt-telegram-bot",
                                        disable_web_page_preview=True)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handles the /start command.
        """
        if not self.is_allowed(update):
            logging.info(f'User {update.message.from_user.name} is not allowed to start the bot')
            await self.send_disallowed_message(update, context)
            return

        logging.info('Bot started')
        await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a Chat-GPT3 Bot, please talk to me!")

    async def reset(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Resets the conversation.
        """
        if not self.is_allowed(update):
            logging.info(f'User {update.message.from_user.name} is not allowed to reset the bot')
            await self.send_disallowed_message(update, context)
            return

        logging.info('Resetting the conversation...')
        self.gpt3_bot.reset_chat()
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Done!")

    async def send_typing_periodically(self, update: Update, context: ContextTypes.DEFAULT_TYPE, every_seconds: float):
        """
        Sends the typing action periodically to the chat
        """
        while True:
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.TYPING)
            await asyncio.sleep(every_seconds)

    async def prompt(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        React to incoming messages and respond accordingly.
        """
        if not self.is_allowed(update):
            logging.info(f'User {update.message.from_user.name} is not allowed to use the bot')
            await self.send_disallowed_message(update, context)
            return

        logging.info(f'New message received from user {update.message.from_user.name}')

        # Send "Typing..." action periodically every 4 seconds until the response is received
        typing_task = context.application.create_task(
            self.send_typing_periodically(update, context, every_seconds=4)
        )

        if self.config['use_stream']:
            queue = asyncio.Queue()
            _END = object()

            async def fast_forward():
                size = queue.qsize()
                dq2 = collections.deque([None] * 2, 2)
                if size > 0:
                    c = 0
                    while c < size:
                        dq2.appendleft(await queue.get())
                        c += 1
                else:
                    dq2.appendleft(await queue.get())
                return dq2

            async def stream_message(per_messages, sleep_seconds):
                sent_message: Message or None = None
                chunk_text = ''
                ended = False
                sent = True  # make sure message would not be discarded after encountering `RetryAfter` error
                count = 0
                while True:
                    if count >= per_messages:
                        count = 0
                        await asyncio.sleep(sleep_seconds)
                    try:
                        if not ended:
                            (second, first) = await fast_forward()
                            ended = first is _END or second is _END
                            # avoid overriding the message waiting to retry or parsing as Markdown
                            if (not isinstance(first, str)) and (not isinstance(second, str)):
                                pass
                            else:
                                chunk_text = second if isinstance(second, str) else first
                                sent = False

                        if ended and sent:
                            if sent_message is not None:
                                # Final edit, including Markdown formatting
                                sent_message = await sent_message.edit_text(
                                    chunk_text, parse_mode=constants.ParseMode.MARKDOWN)
                            break

                        if sent_message is None:
                            if len(chunk_text.strip()) == 0:
                                continue
                            sent_message = await context.bot.send_message(
                                chat_id=update.effective_chat.id,
                                reply_to_message_id=update.message.message_id,
                                text=chunk_text
                            )
                        elif sent_message.text.strip() != chunk_text.strip():
                            # Edits the `sent_message` with the updated text from the latest chunk
                            sent_message = await sent_message.edit_text(chunk_text)

                        sent = True
                        count += 1
                    except RetryAfter as e:
                        logging.info(f'{str(e)}, retry after {e.retry_after} second(s)')
                        sent = False
                        await asyncio.sleep(e.retry_after)
                    except Exception as e:
                        sent = True
                        logging.info(f'Error while editing the message: {str(e)}')
                        if ended:
                            break

            # Start task to retrieve messages from queue and send to Telegram
            message_update_task = context.application.create_task(stream_message(per_messages=30, sleep_seconds=0.5))

            # Stream the response
            try:
                async for chunk in self.gpt3_bot.ask(update.message.text):
                    await queue.put(chunk['message'])
            except Exception as e:
                logging.info(f'Streaming error: {str(e)}')
            await queue.put(_END)

            await asyncio.gather(message_update_task)
            typing_task.cancel()

        else:
            response = await self.get_chatgpt_response(update.message.text)
            typing_task.cancel()

            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                reply_to_message_id=update.message.message_id,
                text=response,
                parse_mode=constants.ParseMode.MARKDOWN
            )

    async def get_chatgpt_response(self, message) -> dict:
        """
        Gets the response from the ChatGPT APIs.
        """
        try:
            response = {'message': ''}
            async for data in self.gpt3_bot.ask(message):
                response = data
            return response
        except Exception as e:
            error_text = f'Error while getting the response: {str(e)}'
            logging.info(error_text)
            return error_text

    async def send_disallowed_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Sends the disallowed message to the user.
        """
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=self.disallowed_message,
            disable_web_page_preview=True
        )

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Handles errors in the telegram-python-bot library.
        """
        logging.debug(f'Exception while handling an update: {context.error}')

    def is_allowed(self, update: Update) -> bool:
        """
        Checks if the user is allowed to use the bot.
        """
        if self.config['allowed_user_ids'] == '*':
            return True
        return str(update.message.from_user.id) in self.config['allowed_user_ids'].split(',')

    def run(self):
        """
        Runs the bot indefinitely until the user presses Ctrl+C
        """
        application = ApplicationBuilder().token(self.config['token']).build()

        application.add_handler(CommandHandler('start', self.start, block=False))
        application.add_handler(CommandHandler('reset', self.reset, block=False))
        application.add_handler(CommandHandler('help', self.help, block=False))
        application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.prompt, block=False))

        application.add_error_handler(self.error_handler)

        application.run_polling()
