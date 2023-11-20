# telegram
import os
import requests
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
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


resume_buttons = [[InlineKeyboardButton('📰 PDF ', callback_data='pdf'),
                   InlineKeyboardButton('🖥  Website ', url='https://portfolio-aliseyedi01.vercel.app/en')],
                  [InlineKeyboardButton('🔙  Back', callback_data='back_contact')]
                  ]
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

about_text = """
I'm *Ali Seyedi*, a passionate Front\-End developer with one year of experience \. I continuously enhance my coding skills through online resources, articles, and hands\-on projects \. My journey includes exploring _web and mobile development_, with a focus on *JavaScript* and *TypeScript* \.
I've worked with popular libraries like __React\.js__ and the __Next\.js__ framework \.Check out my skills section for a complete list of technologies I've mastered \. Currently seeking new opportunities to expand my expertise and tackle fresh challenges
Feel free to share educational resources or projects that align with my goals \.
👉 ||Let's connect and grow together \!||
"""


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
        await update.callback_query.edit_message_text(text=about_text, reply_markup=self.create_inline_keyboard(back_buttons), parse_mode="MarkdownV2")

    async def send_contact(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.edit_message_text(text='Select a contact option:', reply_markup=self.create_inline_keyboard(contact_buttons))

    async def send_pdf(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        pdf_file_path = 'English.pdf'

        # Open the PDF file
        with open(pdf_file_path, 'rb') as pdf_file:
            # Send the PDF file
            await context.bot.send_document(chat_id=update.callback_query.message.chat_id, document=InputFile(pdf_file, filename='English.pdf'))

    async def send_github_projects(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        github_username = 'aliseyedi01'
        github_api_url = f'https://api.github.com/users/{github_username}/repos'

        try:
            response = requests.get(github_api_url)
            response.raise_for_status()
            repositories = response.json()
        except requests.RequestException as e:
            logger.error(f'Error fetching GitHub repositories: {e}')
            await update.callback_query.edit_message_text('Error fetching GitHub repositories.')
            return

        buttons = []
        row = []
        for repo in repositories:
            project_name = repo['name']
            button = InlineKeyboardButton(project_name, callback_data=f'repo_{repo["id"]}')
            row.append(button)
            if len(row) == 2:
                buttons.append(row)
                row = []

        # Add the remaining buttons if any
        if row:
            buttons.append(row)

        # Add a back button
        buttons.append([InlineKeyboardButton('🔙 Back', callback_data='back_contact')])

        keyboard = InlineKeyboardMarkup(buttons)

        await update.callback_query.edit_message_text('Select a repository:', reply_markup=keyboard)

    async def send_repo_details(self, update: Update, context: ContextTypes.DEFAULT_TYPE, repo_id: str):
        github_username = 'aliseyedi01'
        github_api_url = f'https://api.github.com/repositories/{repo_id}'

        try:
            response = requests.get(github_api_url)
            response.raise_for_status()
            repo_details = response.json()
        except requests.RequestException as e:
            logger.error(f'Error fetching GitHub repository details: {e}')
            await update.callback_query.edit_message_text('Error fetching GitHub repository details.')
            return

        # Get information
        repo_name = repo_details.get('name', 'Unnamed Repository')
        repo_description = repo_details.get('description', 'No description available')
        repo_html_url = repo_details.get('html_url')
        repo_language = repo_details.get('language', 'without language')
        repo_technologies = repo_details.get('topics', [])

        # Format text
        name_text = f"<b>🔅 {repo_name} 🔅</b>"
        description_text = f"<strong>💠 Description</strong>: {repo_description}"
        technologies_text = "\n".join([f"       {technology}" for technology in repo_technologies])
        technologies_text = f"<strong>✨ Technologies</strong>:\n{technologies_text}" if technologies_text else ""
        languages_text = f"<strong>💡 Language</strong>: {repo_language}" if repo_language else ""
        url_text = f"<a href='{repo_html_url}'>🌐 Online</a>"

        # Final format
        details_text = f"{name_text}\n\n{description_text}\n\n" \
            f"{languages_text}\n\n{technologies_text}\n\n" \
            f"{url_text}"

        details_keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton('🔙 Back', callback_data='project')]])

        await update.callback_query.edit_message_text(text=details_text, reply_markup=details_keyboard, parse_mode="HTML")

    async def send_resume(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.edit_message_text('Here you can find *My Resume*', reply_markup=self.create_inline_keyboard(resume_buttons), parse_mode="MarkdownV2")

    async def send_skills(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        skill_text = "\n".join(skills_text)
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
            await self.send_github_projects(update, context)
        elif data == "contact":
            await self.send_contact(update, context)
        elif data == "pdf":
            await self.send_pdf(update, context)
        elif data == "back_contact":
            await self.send_back_contact(update, context)
        elif data.startswith("repo_"):
            # Extract the repository ID from the callback data
            repo_id = data.split('_')[1]
            await self.send_repo_details(update, context, repo_id)
        elif data == "back_contact":
            await self.send_back_contact(update, context)

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_name = update.message.from_user.first_name
        logger.info(f'Start command received from user: {user_name}')
        await update.message.reply_text(f'Welcome to My Bot, {user_name}!', reply_markup=self.create_inline_keyboard(main_buttons))

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message:
            message_type = update.message.chat.type
            user_name = update.message.from_user.first_name
            text = update.message.text

            logger.info(f'Message received from user {user_name}: {text}')

            if message_type == "group" and BOT_USERNAME in text:
                new_text = text.replace(BOT_USERNAME, '').strip()
                response = self.handle_response(new_text, user_name)
            elif message_type != "group":
                response = self.handle_response(text, user_name)
            else:
                return

            await update.message.reply_text(response)

    def handle_response(self, text, user_name):
        processed = text.lower()

        if "hello" in processed:
            return f'Hey there, {user_name}!'
        return f"I do not understand what you wrote, {user_name} ..."

    async def error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.error(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    logger.info('Starting bot...')
    my_bot = MyBot(TOKEN)
    my_bot.run()
