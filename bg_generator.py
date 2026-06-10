import requests
import uuid
import os

def generate_background():
    url = "https://picsum.photos/720/1280"  # ✅ stable random image API

    filename = f"assets/{uuid.uuid4()}.jpg"

    try:
        response = requests.get(url, timeout=10)

        # ✅ Validate response
        if response.status_code != 200 or "image" not in response.headers.get("Content-Type", ""):
            raise Exception("Invalid image response")

        with open(filename, "wb") as f:
            f.write(response.content)

        return filename

    except Exception as e:
        print(f"[BG ERROR] {e}")

        # ✅ fallback image (VERY IMPORTANT)
        return "assets/fallback.jpg"