from flask import Flask, request, send_file
from PIL import Image
import io
from diffusers import StableDiffusionPipeline
import torch
from utils.image_utils import resize_to_thumbnail

app = Flask(__name__)

# Load lightweight SD model (CPU-friendly)
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float32
)
pipe.to("cpu")  # Heroku free dyno, CPU only

@app.route("/expand", methods=["POST"])
def expand_image():
    if "image" not in request.files:
        return {"error": "No image uploaded"}, 400

    input_file = request.files["image"]
    img = Image.open(input_file).convert("RGB")

    # Generate expanded image (simple prompt)
    prompt = "A beautiful expanded version of the photo, realistic"
    result = pipe(prompt=prompt, image=img, num_inference_steps=20).images[0]

    # Resize to 1280x720
    output_bytes = io.BytesIO()
    resize_to_thumbnail(result, output_bytes)
    output_bytes.seek(0)
    return send_file(output_bytes, mimetype="image/png")

@app.route("/")
def index():
    return "🧠 AI Photo Expand API Ready ✅"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
