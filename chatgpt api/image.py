import base64
from pathlib import Path
from typing import Any
from openai import OpenAI

client = OpenAI()

def image2content(image_path: Path) -> dict[str,Any]:
    # base64エンコード
    with image_path.open("rb") as f:
        image_base64 = base64.b64encode(f.read()).decode("utf-8")

        #　contentの作成
        content = {
            "type": "image_url",
            "image_url": {"url": f"data:image/{image_path.stem};base64,{image_base64}", "detail": "low"},
        }
        return content
    
prompt = "この画像は何ですか？"
image_path = Path("./sample_image1.png")
contents = [{"type": "text", "text": prompt}, image2content(image_path)]

response = client.chat.completions.create(
    model="gpt-4o",
    temperature=0.0,
    messages=[{"role": "user", "content": contents}],
)

print(response.choices[0].message.content)

# 複数画像の入力
image_path2 = Path("./sample_image2.png")

prompt = "２枚の画像の違いを教えてください。"
contents = [
    {"type": "text", "text": prompt},
    image2content(image_path),
    image2content(image_path2),
]
response = client.chat.completions.create(
    model="gpt-4o-mini",
    temperature=0.0,
    messages=[{"role": "user", "content": contents}],
)

print(response.choices[0].message.content)