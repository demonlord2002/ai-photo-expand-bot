import os
import requests
from io import BytesIO
from PIL import Image
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Free Hugging Face API (no token, unlimited use)
HF_API_URL = "https://hf.space/embed/ppxxl/stable-diffusion-xl-outpainting/+/api/predict/"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! Send me a photo (portrait or square), and I’ll expand it to 1280×720 YouTube thumbnail size using AI 🧠✨"
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    image_url = file.file_path

    await update.message.reply_text("🧠 Expanding your image... please wait 15–30 seconds ⏳")

    try:
        response = requests.post(HF_API_URL, json={
            "data": [image_url, "expand background naturally to cinematic 1280x720 youtube thumbnail"]
        })
        result = response.json()
        output_url = result["data"][0]

        # Download the expanded image
        img_data = requests.get(output_url).content
        img = Image.open(BytesIO(img_data))
        img = img.resize((1280, 720))  # Ensure exact thumbnail size

        bio = BytesIO()
        bio.name = "expanded.jpg"
        img.save(bio, "JPEG")
        bio.seek(0)

        await update.message.reply_photo(photo=bio, caption="✅ AI Expanded YouTube Thumbnail Ready!")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error expanding image: {e}")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

print("🤖 Bot started successfully!")
app.run_polling()
