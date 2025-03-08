from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = '7952680876:AAGgj9HQeW-3tLFsjDdAXjuXm8fLzv2bMpw'
BOT_USERNAME: Final = '@testingsbcbot'

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I can help. Just send a link!!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I can help. Just send a link!")

# Save link
def save_link_to_file(link: str):
    with open("links.txt", "a") as file:
        file.write(link + "")
    
    with open("return.txt", "w") as file:  # Overwrites return.txt with the latest link
        file.write(link + "")

async def show_last_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open("return.txt", "r") as file:
            links = file.readlines()
        
        if links:
            last_link = links[-1].strip()  # Get the last link and remove any extra spaces/newlines
            response = f"Here is the last saved link:\n{last_link}"
        else:
            response = "No links found."

    except FileNotFoundError:
        response = "No links have been saved yet."

    await update.message.reply_text(response)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text.strip()

    print(f'User({update.message.chat.id}) in {message_type}: "{text}"')
    
    if text.startswith("http://") or text.startswith("https://"):
        save_link_to_file(text)
        
        # Read and return the latest saved link
        try:
            with open("return.txt", "r") as file:
                last_link = file.readlines()[-1].strip()  # Get the last saved link
                response = f"✅ Link saved! Here it is:\n{last_link}"
        except FileNotFoundError:
            response = "✅ Link saved, but no link found in return.txt!"

    else:
        if message_type == 'group' and BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response = handle_response(new_text)
        else:
            response = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)


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
    app.add_handler(CommandHandler('lastlink', show_last_link))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)
