# combine.py - RELIABLE AUDIO+VIDEO COMBINER
import subprocess
import os

def combine_audio_video(video_file, audio_file, output_file):
    """Combine video and audio using FFmpeg directly"""
    
    try:
        # Use ffmpeg to combine video and audio
        cmd = [
            'ffmpeg',
            '-i', video_file,      # input video (no audio)
            '-i', audio_file,      # input audio
            '-c:v', 'copy',        # copy video stream (no re-encode)
            '-c:a', 'aac',         # encode audio to AAC
            '-map', '0:v:0',       # take video from first input
            '-map', '1:a:0',       # take audio from second input
            '-shortest',           # match shortest duration
            '-y',                  # overwrite output
            output_file
        ]
        
        print(f"[COMBINE] Running ffmpeg...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"[COMBINE] ✅ Success: {output_file}")
            return True
        else:
            print(f"[COMBINE] ❌ Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"[COMBINE] ❌ Exception: {e}")
        return False

# Test function
if __name__ == "__main__":
    combine_audio_video("outputs/video_0.mp4", "outputs/audio_0.mp3", "outputs/final_0.mp4")