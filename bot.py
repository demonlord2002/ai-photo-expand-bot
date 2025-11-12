import os
import requests
from io import BytesIO
from PIL import Image
import base64
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Hugging Face free public outpainting API
HF_API_URL = "https://hf.space/embed/ppxxl/stable-diffusion-xl-outpainting/+/api/predict/"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! Send me a photo (portrait or square), and I’ll expand it to a cinematic 1280×720 YouTube thumbnail using AI 🧠✨"
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    file_path = file.file_path

    await update.message.reply_text("🧠 Expanding your image... please wait 20–40 seconds ⏳")

    try:
        # Download the Telegram image
        img_data = requests.get(file_path).content
        # Convert to Base64
        img_base64 = base64.b64encode(img_data).decode("utf-8")

        # Send image as base64 to Hugging Face API
        response = requests.post(HF_API_URL, json={
            "data": [f"data:image/png;base64,{img_base64}", "expand background naturally to cinematic 1280x720 youtube thumbnail"]
        })

        # Check response
        result = response.json()
        output_url = result["data"][0]

        # Download expanded image
        expanded_data = requests.get(output_url).content
        img = Image.open(BytesIO(expanded_data))
        img = img.resize((1280, 720))  # Ensure exact thumbnail size

        bio = BytesIO()
        bio.name = "expanded.jpg"
        img.save(bio, "JPEG")
        bio.seek(0)

        await update.message.reply_photo(photo=bio, caption="✅ AI Expanded YouTube Thumbnail Ready!")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error expanding image: {e}")

# Initialize the bot
app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

print("🤖 AI Photo Expand Bot is running...")
app.run_polling()
