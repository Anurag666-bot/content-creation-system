# main.py - Complete with Female Avatar System
import os
import time
import hashlib
from scraper import get_reddit_posts
from script_maker import generate_script
from tts import text_to_speech
from free_avatar_engine import generate_talking_avatar
from config import OUTPUT_DIR

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs("assets/avatars", exist_ok=True)

USED_POSTS_FILE = "used_posts.txt"

def is_duplicate(post):
    post_hash = hashlib.md5(post.encode()).hexdigest()
    if not os.path.exists(USED_POSTS_FILE):
        return False
    with open(USED_POSTS_FILE, "r") as f:
        return post_hash in f.read()

def save_post(post):
    post_hash = hashlib.md5(post.encode()).hexdigest()
    with open(USED_POSTS_FILE, "a") as f:
        f.write(post_hash + "\n")

def main():
    print("🎭 Starting AI Female Avatar Content System...")
    print("=" * 50)
    
    # Get stories
    posts = get_reddit_posts()
    
    if not posts:
        print("❌ No posts found")
        return
    
    print(f"✅ Found {len(posts)} stories\n")
    
    for idx, post in enumerate(posts[:3]):  # Start with 3 videos
        print(f"\n{'='*50}")
        print(f"[{idx+1}/3] Creating video with NEW female avatar...")
        print(f"{'='*50}")
        
        try:
            # Skip duplicates
            if is_duplicate(post):
                print("⚠️ Duplicate skipped")
                continue
            
            # Generate script
            script = generate_script(post)
            print(f"📝 Story: {script[:100]}...")
            
            # Generate voice
            audio_file = f"{OUTPUT_DIR}/audio_{idx}.mp3"
            print(f"🎤 Generating female voice...")
            text_to_speech(script, audio_file)
            
            if not os.path.exists(audio_file):
                print("❌ Voice generation failed")
                continue
            
            # Generate avatar video (different lady each time)
            video_file = f"{OUTPUT_DIR}/video_{idx}.mp4"
            print(f"🎭 Creating talking avatar video...")
            
            success = generate_talking_avatar(audio_file, video_file)
            
            if success:
                print(f"✅ Video {idx+1} complete! New avatar used!")
                save_post(post)
            else:
                print(f"❌ Avatar generation failed")
            
            # Rate limiting
            time.sleep(3)
            
        except KeyboardInterrupt:
            print("\n⚠️ User interrupted")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            continue
    
    print(f"\n{'='*50}")
    print("✅ Complete! Check outputs/ folder")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()