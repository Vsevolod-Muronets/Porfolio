import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from transformers import AutoProcessor, BlipForConditionalGeneration

processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

url = "https://en.wikipedia.org/wiki/IBM"

headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
print("Status:", response.status_code, "HTML size:", len(response.text))

soup = BeautifulSoup(response.text, "html.parser")
img_elements = soup.find_all("img")
print(f"Found {len(img_elements)} <img> tags")

with open("captions.txt", "w", encoding="utf-8") as caption_file:
    for idx, img_element in enumerate(img_elements, start=1):
        img_url = img_element.get("src") or img_element.get("data-src")
        if not img_url and img_element.has_attr("srcset"):
            img_url = img_element["srcset"].split()[0]
        if not img_url:
            continue

        if img_url.endswith(".svg") or ".svg" in img_url:
            continue

        if img_url.startswith("//"):
            img_url = "https:" + img_url
        elif img_url.startswith("/"):
            img_url = "https://en.wikipedia.org" + img_url
        elif not img_url.startswith("http"):
            continue

        try:
            r = requests.get(img_url, timeout=10, headers=headers)
            raw_image = Image.open(BytesIO(r.content))

            if raw_image.size[0] * raw_image.size[1] < 200:
                continue

            raw_image = raw_image.convert("RGB")

            text = "the image of"
            inputs = processor(images=raw_image, text=text, return_tensors="pt")
            out = model.generate(**inputs, max_new_tokens=50)
            caption = processor.decode(out[0], skip_special_tokens=True)

            caption_file.write(f"{img_url}: {caption}\n")
            print(f"[{idx}] Caption saved")

        except OSError:
            continue
        except Exception as e:
            print(f"[{idx}] Error: {e}")
            continue

