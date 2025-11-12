import os
import requests
from io import BytesIO
from PIL import Image
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")        # Optional
HEROKU_API_URL = os.getenv("HEROKU_API_URL")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Send me a portrait photo, and I’ll expand it to a 1280×720 YouTube thumbnail using AI 🧠✨"
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    image_url = file.file_path

    await update.message.reply_text("🧠 Expanding your image... please wait 20–40 seconds ⏳")

    try:
        # Optional: store original in your channel
        if CHANNEL_ID:
            await update.message.bot.send_photo(chat_id=CHANNEL_ID, photo=image_url)

        # Send to your API
        response = requests.post(HEROKU_API_URL, json={
            "image_url": image_url,
            "prompt": "expand background naturally to cinematic 1280x720 YouTube thumbnail"
        })

        if response.status_code == 200:
            expanded_data = response.content
            img = Image.open(BytesIO(expanded_data))
            bio = BytesIO()
            bio.name = "expanded.jpg"
            img.save(bio, "JPEG")
            bio.seek(0)
            await update.message.reply_photo(photo=bio, caption="✅ AI Expanded YouTube Thumbnail Ready!")
        else:
            await update.message.reply_text("⚠️ Error expanding image. Please try again.")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Something went wrong: {e}")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

print("🤖 AI Photo Expand Bot is running...")
app.run_polling()
