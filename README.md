# Portfolio Telegram Bot

A Telegram bot built with Python using the `python-telegram-bot` library. The bot provides information about the owner, skills, resume, projects, and contact details.

## Features

- **About Me:** Get to know more about the bot owner.
- **Skills:** View a list of programming languages, libraries, frameworks, and tools the owner is familiar with.
- **Resume:** Access the owner's resume in PDF format or view it on their website.
- **Projects:** Explore the owner's GitHub repositories and get details about each project.
- **Contact:** Connect with the owner through GitHub, LinkedIn, email, or Telegram.

## Technology Used

- **Python:** Programming language used for bot development.
- **python-telegram-bot:** Telegram Bot API wrapper for Python.
- **requests:** Library for making HTTP requests.
- **dotenv:** Library for loading environment variables from a .env file.

## Prerequisites

- Python 3.6 or later
- Telegram API token
- GitHub API token 

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/aliseyedi01/Portfolio-Telegram-Bot.git
    cd your_repository
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file and add your Telegram API token:

    ```plaintext
    TOKEN=your_telegram_api_token
    ```

4. Run the bot:

    ```bash
    python main.py
    ```

## Usage

1. Start the bot by sending the `/start` command in the Telegram app.
2. Use the inline keyboard to navigate through different sections and get information.
3. Explore projects by selecting the "Pro


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.