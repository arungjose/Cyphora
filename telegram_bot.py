import asyncio  # For asynchronous sleep
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import subprocess

TOKEN: Final = '8119967966:AAGXLsLHHj6_LQXavEPGfFbnl89cvu33Mkw'
BOT_USERNAME: Final = '@cyphorabot'

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Please provide the link to mirror:')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I can help. Just send a link!")

# Save link
def save_link_to_file(link: str):
    with open("user_links.txt", "w") as file:
        file.write(link)

async def mirror_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open("mirror.txt", "r") as file:
            mlink = file.read().strip()
            return mlink
    except FileNotFoundError:
        return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text.strip()

    print(f'User({update.message.chat.id}) in {message_type}: "{text}"')

    if text.startswith("http://") or text.startswith("https://"):
        save_link_to_file(text)

        # Run Tor and Scraper (asynchronously)
        await run_scraper(update, context)

        await update.message.reply_text("The mirror link is being hosted...")

        # Wait for mirror link
        mirror_result = await wait_for_mirror_link(update, context)
        if mirror_result:
            response = f"✅ Mirror link available:\n{mirror_result}"
            await update.message.reply_text(response)
        else:
            response = "Sorry! We are unable to host a mirror link for the given address."
            await update.message.reply_text(response)

        #Introduce a delay here before sending response.
        await asyncio.sleep(5)  # Delay for 5 seconds.

    else:
        if message_type == 'group' and BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response = handle_response(new_text)
        else:
            response = handle_response(text)

        print('Bot:', response)
        await update.message.reply_text(response)

async def run_scraper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        subprocess.Popen(["./tor.exe"])
        subprocess.Popen(["python", "scraper.py"])
        await update.message.reply_text("Scraping and Tor process started.")
    except FileNotFoundError:
        await update.message.reply_text("The mirror link is being hosted...")
    except Exception as e:
        await update.message.reply_text(f"Please wait. Hosting couldd take 2-3 minutes")

async def wait_for_mirror_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for _ in range(60):
        mirror_result = await mirror_link(update, context)
        if mirror_result:
            return mirror_result
        await asyncio.sleep(2)
    return None

# Responses
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hi there!'
    if 'hi' in processed:
        return 'Hello!'

    return "I don't understand..."

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)