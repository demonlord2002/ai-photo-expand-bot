from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests
from io import BytesIO

HEROKU_API_URL = "https://your-app-name.herokuapp.com/expand"  # Change this
BOT_TOKEN = "YOUR_BOT_TOKEN"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a portrait photo, I will expand it to YouTube thumbnail size!")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.photo[-1].get_file()
    bio = BytesIO()
    await file.download_to_memory(out=bio)
    bio.seek(0)

    await update.message.reply_text("🧠 Expanding your image... please wait 20–40 seconds ⏳")
    files = {"image": bio}
    try:
        r = requests.post(HEROKU_API_URL, files=files)
        r.raise_for_status()
        expanded = BytesIO(r.content)
        expanded.seek(0)
        await update.message.reply_photo(photo=expanded)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error expanding image: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling()
    
