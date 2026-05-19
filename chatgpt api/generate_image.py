from openai import OpenAI
import base64
from pathlib import Path
import os

client = OpenAI()

prompt = "メタリックな球体"

response = client.images.generate(
    model="gpt-image-2",
    prompt=prompt,
    size="1024x1024",
)

image_base64 = response.data[0].b64_json

output_path = Path("output2.png")
with open(output_path, "wb") as f:
    f.write(base64.b64decode(image_base64))

print("保存しました:", output_path.resolve())

os.startfile(output_path.resolve())