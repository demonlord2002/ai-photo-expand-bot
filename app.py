from flask import Flask, request, send_file
from diffusers import StableDiffusionXLImg2ImgPipeline
import torch
from PIL import Image
import requests, io

app = Flask(__name__)

print("🔄 Loading Stable Diffusion XL model... this may take 2-3 minutes")
pipe = StableDiffusionXLImg2ImgPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)
pipe.to("cuda" if torch.cuda.is_available() else "cpu")

@app.route("/", methods=["GET"])
def home():
    return "🧠 AI Photo Expand API Ready"

@app.route("/expand", methods=["POST"])
def expand():
    data = request.json
    image_url = data.get("image_url")
    prompt = data.get("prompt", "expand background naturally to cinematic 1280x720 YouTube thumbnail")

    # Download image
    image = Image.open(requests.get(image_url, stream=True).raw).convert("RGB")

    # Run SDXL outpainting
    result = pipe(prompt=prompt, image=image, strength=0.75, guidance_scale=7.5)
    output = result.images[0]

    # Save to BytesIO
    img_bytes = io.BytesIO()
    output.save(img_bytes, format="JPEG")
    img_bytes.seek(0)
    return send_file(img_bytes, mimetype="image/jpeg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
