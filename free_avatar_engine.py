# free_avatar_engine.py - Simple Avatar Video Generator
import os
import random
from moviepy.editor import AudioFileClip, ImageClip, CompositeVideoClip
from config import VIDEO_WIDTH, VIDEO_HEIGHT

def get_random_avatar():
    """Get a random female avatar for each video"""
    avatar_dir = "assets/avatars"
    
    # Check if avatars exist
    if not os.path.exists(avatar_dir):
        os.makedirs(avatar_dir, exist_ok=True)
        print(f"[AVATAR] Created {avatar_dir} folder")
        return None
    
    avatars = [f for f in os.listdir(avatar_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    if not avatars:
        print(f"[AVATAR] No avatars found in {avatar_dir}")
        return None
    
    avatar = random.choice(avatars)
    avatar_path = os.path.join(avatar_dir, avatar)
    print(f"[AVATAR] 🎭 Using avatar: {avatar}")
    return avatar_path

def generate_talking_avatar(audio_file, output_file):
    """Generate video with female avatar (simple version)"""
    
    print(f"[AVATAR] Creating talking avatar video...")
    
    # Get random avatar
    avatar_path = get_random_avatar()
    if not avatar_path:
        print(f"[AVATAR] ❌ No avatar found!")
        return False
    
    # Check audio file
    if not os.path.exists(audio_file):
        print(f"[AVATAR] ❌ Audio not found: {audio_file}")
        return False
    
    try:
        # Load audio
        audio = AudioFileClip(audio_file)
        duration = audio.duration
        print(f"[AVATAR] Audio duration: {duration:.1f}s")
        
        # Load and resize avatar image
        avatar = ImageClip(avatar_path)
        avatar = avatar.resize(height=VIDEO_HEIGHT)
        avatar = avatar.set_duration(duration)
        
        # Add subtle zoom effect
        avatar = avatar.resize(lambda t: 1 + 0.005 * t)
        
        # Combine audio and video
        final = avatar.set_audio(audio)
        
        # Save video
        print(f"[AVATAR] Rendering video...")
        final.write_videofile(
            output_file,
            fps=24,
            codec='libx264',
            audio_codec='aac',
            verbose=False,
            logger=None
        )
        
        # Cleanup
        audio.close()
        final.close()
        
        print(f"[AVATAR] ✅ Video saved: {output_file}")
        return True
        
    except Exception as e:
        print(f"[AVATAR] ❌ Error: {e}")
        return False

# Test
if __name__ == "__main__":
    print("Testing avatar engine...")
    test_audio = "outputs/audio_0.mp3"
    if os.path.exists(test_audio):
        generate_talking_avatar(test_audio, "test_avatar.mp4")
    else:
        print("No test audio found. Run main.py first.")
