from PIL import Image

def resize_to_thumbnail(img_path, output_path, width=1280, height=720):
    with Image.open(img_path) as img:
        img = img.convert("RGB")
        img.thumbnail((width, height))
        img.save(output_path, format="PNG")
      
