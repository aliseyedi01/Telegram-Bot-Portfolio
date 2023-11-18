from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
from typing import Final
# env
import os
from dotenv import load_dotenv
load_dotenv()

# TOKEN: Final = os.getenv("TOKEN")
TOKEN: Final = "6001097101:AAE06zWpGqRy7mpjMk3heQqTPqr0L7DcFVA"
BOT_USERNAME: Final = '@BlockCodeBot'


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello ! Thank for Chatting with me , i am ali seyedi ')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('i am ali seyedi ! Please Type  something i can respond !')


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('this is a custom command !')


# Response

def handle_response(text: str) -> str:
    processed: str = text.lower()

    if "hello" in processed:
        return 'hey there!'

    return "I do not understand what you wrote ..."


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}" ')

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:', response)

    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print('starting bot ...')
    app = Application.builder().token(TOKEN).build()

    # commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # errors
    app.add_error_handler(error)

    print('polling ...')
    app.run_polling(poll_interval=3)
