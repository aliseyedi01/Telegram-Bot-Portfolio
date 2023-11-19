# telegram
import requests
import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
import logging

load_dotenv()

TOKEN = os.getenv("TOKEN")
BOT_USERNAME = '@BlockCodeBot'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Buttons
main_buttons = [[InlineKeyboardButton('👨‍💻 About Me ', callback_data='info'),
                 InlineKeyboardButton('⌨️  Skills ', callback_data='skills')],
                [InlineKeyboardButton('🧾  Resume ', callback_data='resume'),
                 InlineKeyboardButton('🌐 Projects', callback_data='project')],
                [InlineKeyboardButton('📞  Contact', callback_data='contact')]
                ]

contact_buttons = [
    [InlineKeyboardButton('🔮 GitHub', url='https://github.com/aliseyedi01'),
        InlineKeyboardButton('👨‍💻 LinkedIn', url='https://www.linkedin.com/in/aliseyedi01/')],
    [InlineKeyboardButton('✉ Email', url='https://mail.google.com/mail/u/0/?view=cm&fs=1&to=aliseyedi07@gmail.com1'),
        InlineKeyboardButton('🗯 Chat', url='https://t.me/aliseyedi01')],
    [InlineKeyboardButton('🔙 Back', callback_data='back_contact')]
]

back_buttons = [[InlineKeyboardButton('🔙 Back', callback_data='back_contact')]]

# text
skills_text = [
    "*Languages*",
    "   HTML",
    "   JavaScript",
    "   TypeScript",
    "*Libraries & Framework*",
    "   React\.js",
    "   Next\.js",
    "   Redux",
    "   Redux Toolkit",
    "   React Query",
    "*Styles*",
    "   Css",
    "   Sass",
    "   Tailwind Css",
    "   Bootstrap",
    "   Material\-UI",
    "   Ant\-Design",
    "   Shadcn\-UI",
    "*Tools*",
    "   Git",
    "   Git Hub",
    "   Post Man",
    "   Fire base",
    "   Supa base",
    "   Figma",
]

about_text = "This is where you can find \n information about me and my work."


class MyBot:
    def __init__(self, token):
        self.app = Application.builder().token(token).build()

    def run(self):
        self.add_handlers()
        self.app.run_polling(timeout=10)

    def add_handlers(self):
        self.app.add_handler(CallbackQueryHandler(self.handle_button_press))
        self.app.add_handler(CommandHandler('start', self.start_command))
        self.app.add_handler(MessageHandler(filters.TEXT, self.handle_message))
        self.app.add_error_handler(self.error)

    def create_inline_keyboard(self, buttons):
        return InlineKeyboardMarkup(buttons)

    async def send_back_contact(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.edit_message_text(text='Welcome to my bot!', reply_markup=self.create_inline_keyboard(main_buttons))

    async def send_information(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.edit_message_text(text=about_text, reply_markup=self.create_inline_keyboard(back_buttons))

    async def send_contact(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.edit_message_text(text='Select a contact option:', reply_markup=self.create_inline_keyboard(contact_buttons))

    async def send_projects(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.edit_message_text('Here you can find a list of my projects', reply_markup=self.create_inline_keyboard(back_buttons))

    async def send_resume(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.edit_message_text('Here you can find *my resume*', reply_markup=self.create_inline_keyboard(back_buttons), parse_mode="MarkdownV2")

    async def send_skills(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        skill_text = "\n".join(skills_text)
        logger.info(skill_text)
        await update.callback_query.edit_message_text(text=skill_text, reply_markup=self.create_inline_keyboard(back_buttons), parse_mode="MarkdownV2")

    async def handle_button_press(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        data = query.data

        if data == "info":
            await self.send_information(update, context)
        elif data == "skills":
            await self.send_skills(update, context)
        elif data == "resume":
            await self.send_resume(update, context)
        elif data == "project":
            await self.send_projects(update, context)
        elif data == "contact":
            await self.send_contact(update, context)
        elif data == "back_contact":
            await self.send_back_contact(update, context)

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text('Welcome to My Bot!', reply_markup=self.create_inline_keyboard(main_buttons))

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message:
            message_type = update.message.chat.type
            text = update.message.text

            if message_type == "group" and BOT_USERNAME in text:
                new_text = text.replace(BOT_USERNAME, '').strip()
                response = self.handle_response(new_text)
            elif message_type != "group":
                response = self.handle_response(text)
            else:
                return

            await update.message.reply_text(response)

    def handle_response(self, text):
        processed = text.lower()

        if "hello" in processed:
            return 'hey there!'

        return "I do not understand what you wrote ..."

    async def error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.error(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    logger.info('Starting bot...')
    my_bot = MyBot(TOKEN)
    my_bot.run()
