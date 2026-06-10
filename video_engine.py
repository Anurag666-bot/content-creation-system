# video_engine.py - COMPLETE WORKING VERSION
import random
import numpy as np
import os
import uuid
import requests
import subprocess
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import (
    CompositeVideoClip,
    AudioFileClip,
    ImageClip,
    ColorClip
)
from caption_engine import split_words, chunk_words
from config import VIDEO_WIDTH, VIDEO_HEIGHT, FPS

# =========================
# SETUP
# =========================
os.makedirs("assets", exist_ok=True)
os.makedirs("outputs", exist_ok=True)


# =========================
# MOOD COLORS FOR CONTENT TYPES
# =========================
def get_mood_color(content_type):
    """Get mood-based colors for text"""
    colors = {
        "horror": "red",
        "funny": "gold",
        "emotional": "lightblue",
        "normal": "white"
    }
    return colors.get(content_type, "white")


# =========================
# RELIABLE BACKGROUND GENERATOR
# =========================
def generate_background_image():
    """Generate a reliable background image"""
    
    filename = f"assets/{uuid.uuid4()}.jpg"
    
    urls = [
        f"https://picsum.photos/{VIDEO_WIDTH}/{VIDEO_HEIGHT}?random={random.randint(1,999999)}",
    ]
    
    for url in urls:
        try:
            response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            if "image" in response.headers.get("Content-Type", ""):
                with open(filename, "wb") as f:
                    f.write(response.content)
                return filename
        except:
            continue
    
    # Fallback: black image
    img = Image.new("RGB", (VIDEO_WIDTH, VIDEO_HEIGHT), color=(20, 20, 40))
    img.save(filename)
    return filename


def get_background(duration):
    """Create background clip with zoom effect"""
    
    img_path = generate_background_image()
    
    try:
        with Image.open(img_path) as img:
            img = img.convert("RGB")
            img = img.resize((VIDEO_WIDTH, VIDEO_HEIGHT), Image.Resampling.LANCZOS)
            img_array = np.array(img)
        
        clip = ImageClip(img_array).set_duration(duration)
        # Add zoom effect for dynamic feel
        clip = clip.resize(lambda t: 1 + 0.02 * t)
        return clip
    except:
        # Fallback to solid color
        return ColorClip(size=(VIDEO_WIDTH, VIDEO_HEIGHT), color=(20, 20, 40), duration=duration)


# =========================
# TEXT IMAGE CREATOR (NO IMAGEMAGICK!)
# =========================
def create_text_image(text, fontsize=60, color="white"):
    """Create text image using PIL (no ImageMagick)"""
    
    # Create transparent background
    img = Image.new("RGBA", (VIDEO_WIDTH, 400), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Try to load font
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "C:\\Windows\\Fonts\\Arial.ttf"
    ]
    
    font = None
    for path in font_paths:
        if os.path.exists(path):
            try:
                font = ImageFont.truetype(path, fontsize)
                break
            except:
                continue
    
    if font is None:
        font = ImageFont.load_default()

    # Auto line wrap
    max_width = VIDEO_WIDTH - 100
    words = text.split()
    lines = []
    current = ""

    for word in words:
        test = current + " " + word if current else word
        bbox = draw.textbbox((0, 0), test, font=font)
        width = bbox[2] - bbox[0]

        if width <= max_width:
            current = test
        else:
            lines.append(current)
            current = word

    if current:
        lines.append(current)

    # Draw text with background shadow for better visibility
    y_text = 50
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        
        # Draw shadow
        draw.text(
            ((VIDEO_WIDTH - text_width) // 2 + 2, y_text + 2),
            line,
            font=font,
            fill="black"
        )
        # Draw main text
        draw.text(
            ((VIDEO_WIDTH - text_width) // 2, y_text),
            line,
            font=font,
            fill=color
        )
        y_text += fontsize + 10

    return np.array(img)


def make_text_clip(text, fontsize=60, color="white", duration=2, position=("center", "center")):
    """Create text clip without ImageMagick"""
    
    img_array = create_text_image(text, fontsize, color)
    clip = ImageClip(img_array).set_duration(duration)
    return clip.set_position(position)


# =========================
# CAPTION FUNCTIONS
# =========================
def create_word_captions(script, duration, content_type="normal"):
    """Create word-by-word captions with mood colors"""
    
    words = split_words(script)
    if not words:
        return []
    
    word_time = duration / len(words)
    clips = []
    mood_color = get_mood_color(content_type)
    
    for i, word in enumerate(words):
        # Alternate colors for emphasis
        if i % 3 == 0:
            color = mood_color
        elif i % 3 == 1:
            color = "yellow"
        else:
            color = "white"
            
        clip = make_text_clip(
            word,
            fontsize=70,
            color=color,
            duration=word_time,
            position=("center", "center")
        ).set_start(i * word_time)
        clips.append(clip)
    
    return clips


def create_scene_captions(script, duration, content_type="normal"):
    """Create scene captions"""
    
    chunks = chunk_words(script.split(), 4)
    if not chunks:
        return []
    
    chunk_time = duration / len(chunks)
    clips = []
    mood_color = get_mood_color(content_type)
    
    for i, chunk in enumerate(chunks):
        clip = make_text_clip(
            chunk,
            fontsize=55,
            color=mood_color,
            duration=chunk_time,
            position=("center", "bottom")
        ).set_start(i * chunk_time)
        clips.append(clip)
    
    return clips


def create_hook(script, content_type="normal"):
    """Create hook text with mood color"""
    
    hook = script[:60]
    mood_color = get_mood_color(content_type)
    
    return make_text_clip(
        hook,
        fontsize=80,
        color=mood_color,
        duration=3,
        position=("center", "top")
    )


# =========================
# MAIN VIDEO FUNCTION
# =========================
def create_video(audio_file, script, output_file, content_type="normal"):
    """Create final video with audio and mood-based styling"""
    
    print("=" * 50)
    print("[VIDEO] Starting...")
    print("=" * 50)
    
    # Check if audio file exists
    if not os.path.exists(audio_file):
        print(f"[ERROR] Audio file not found: {audio_file}")
        return False
    
    # Load audio
    try:
        audio = AudioFileClip(audio_file)
        duration = audio.duration
        print(f"[1/5] Audio loaded: {duration:.1f}s")
        print(f"[1/5] Content type: {content_type.upper()}")
    except Exception as e:
        print(f"[ERROR] Failed to load audio: {e}")
        return False
    
    # Create background
    print("[2/5] Creating background...")
    try:
        bg = get_background(duration)
    except Exception as e:
        print(f"[ERROR] Background failed: {e}")
        bg = ColorClip(size=(VIDEO_WIDTH, VIDEO_HEIGHT), color=(0, 0, 0), duration=duration)
    
    # Create captions
    print("[3/5] Creating captions...")
    try:
        hook = create_hook(script, content_type)
        word_caps = create_word_captions(script, duration, content_type)
        scene_caps = create_scene_captions(script, duration, content_type)
        print(f"      ✓ Created {len(word_caps)} word captions")
        print(f"      ✓ Created {len(scene_caps)} scene captions")
    except Exception as e:
        print(f"[ERROR] Captions failed: {e}")
        word_caps = []
        scene_caps = []
        hook = None
    
    # Combine all layers
    print("[4/5] Assembling video...")
    try:
        layers = [bg]
        if hook:
            layers.append(hook)
        layers.extend(word_caps)
        layers.extend(scene_caps)
        
        final = CompositeVideoClip(layers)
        
        # Add audio
        final = final.set_audio(audio)
    except Exception as e:
        print(f"[ERROR] Assembly failed: {e}")
        return False
    
    # Render final video
    print("[5/5] Rendering video...")
    try:
        final.write_videofile(
            output_file,
            fps=FPS,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            verbose=False,
            logger=None
        )
    except Exception as e:
        print(f"[ERROR] Rendering failed: {e}")
        return False
    
    # Cleanup
    final.close()
    bg.close()
    audio.close()
    
    # Verify
    if os.path.exists(output_file):
        size = os.path.getsize(output_file) / (1024 * 1024)
        print(f"[✓] FINAL VIDEO: {output_file} ({size:.1f} MB)")
        
        # Quick audio verification
        try:
            verify = AudioFileClip(output_file)
            if verify.duration > 0:
                print(f"[✓] Audio verified! Duration: {verify.duration:.1f}s")
            verify.close()
        except:
            print("[⚠] Could not verify audio (but file was created)")
        
        return True
    
    print("[✗] Failed to create video")
    return False


# =========================
# TEST FUNCTION
# =========================
if __name__ == "__main__":
    print("✅ video_engine.py loaded (No ImageMagick)")
    print(f"   Video size: {VIDEO_WIDTH}x{VIDEO_HEIGHT}")
    print(f"   FPS: {FPS}")
    
    # Test mood colors
    for mood in ["horror", "funny", "normal"]:
        print(f"   {mood} color: {get_mood_color(mood)}")