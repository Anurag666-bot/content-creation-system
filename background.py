# background.py - COMPLETE FIX (no more image errors)
import requests
import uuid
import os
from PIL import Image
import io

def generate_background():
    """Generate reliable background image - guaranteed to work"""
    
    os.makedirs("assets", exist_ok=True)
    filename = f"assets/{uuid.uuid4()}.jpg"
    
    # Try multiple reliable sources
    urls = [
        f"https://picsum.photos/720/1280",
        "https://placekitten.com/720/1280",
        "https://picsum.photos/id/1/720/1280",
    ]
    
    for url in urls:
        try:
            print(f"[BG] Trying: {url}")
            response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            
            # Check if response is actually an image
            content_type = response.headers.get("Content-Type", "")
            
            if "image" in content_type:
                # Verify it's a valid image
                img = Image.open(io.BytesIO(response.content))
                img.verify()
                
                # Save the image
                with open(filename, "wb") as f:
                    f.write(response.content)
                
                print(f"[BG] ✅ Success: {filename}")
                return filename
            else:
                print(f"[BG] Not an image, trying next source...")
                
        except Exception as e:
            print(f"[BG] Failed: {e}")
            continue
    
    # Ultimate fallback - create a gradient image
    print("[BG] Creating fallback gradient background")
    from PIL import ImageDraw
    
    img = Image.new("RGB", (720, 1280), color=(20, 20, 40))
    draw = ImageDraw.Draw(img)
    
    # Add simple gradient effect
    for i in range(1280):
        color = int(20 + (i / 1280) * 50)
        draw.line([(0, i), (720, i)], fill=(color, color, color+10))
    
    img.save(filename)
    print(f"[BG] ✅ Fallback created: {filename}")
    return filename