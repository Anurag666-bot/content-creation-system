# tts.py - Female Voice Generator (Working)
import asyncio
import edge_tts
import random
import time

# Best FREE female voices
FEMALE_VOICES = [
    "en-US-JennyNeural",      # American - Very natural
    "en-GB-SoniaNeural",      # British - Elegant  
    "en-AU-NatashaNeural",    # Australian - Friendly
    "en-CA-ClaraNeural",      # Canadian - Warm
]

def detect_content_type(text):
    """Detect if content is horror or funny for voice style"""
    horror_words = ['scared', 'terror', 'haunt', 'ghost', 'dark', 'shadow', 'blood', 'kill', 'death', 'creepy', 'nightmare']
    funny_words = ['laugh', 'funny', 'hilarious', 'joke', 'crack', 'lol', 'lmfao', 'embarrassing', 'cringe']
    
    text_lower = text.lower()
    if any(word in text_lower for word in horror_words):
        return "horror"
    elif any(word in text_lower for word in funny_words):
        return "funny"
    return "normal"

def get_rate(content_type):
    """Get appropriate rate based on content type"""
    rates = {
        "horror": "-15%",   # Slower for horror
        "funny": "+10%",    # Faster for comedy
        "normal": "+0%"     # Normal speed
    }
    return rates.get(content_type, "+0%")

async def generate_female_voice(text, filename):
    """Generate realistic female voice with emotion"""
    
    # Detect content type
    content_type = detect_content_type(text)
    
    # Select random female voice
    voice = random.choice(FEMALE_VOICES)
    
    # Get rate based on content
    rate = get_rate(content_type)
    
    # Clean text (remove special characters that might break TTS)
    text = text.replace('*', '')
    text = text.replace('_', '')
    text = text.replace('...', '. ')
    
    # Add natural pauses
    text = text.replace('. ', '. ')
    text = text.replace('! ', '! ')
    
    # Generate speech
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(filename)
    
    print(f"[TTS] ✅ Female voice ({voice}, {content_type}, rate:{rate})")
    return filename

def text_to_speech(text, filename, retries=2):
    """Synchronous wrapper for TTS"""
    
    for attempt in range(retries):
        try:
            # Run async function
            asyncio.run(generate_female_voice(text, filename))
            return True
        except Exception as e:
            print(f"[TTS] Attempt {attempt+1} failed: {e}")
            time.sleep(2)
    
    print("[TTS] ❌ All attempts failed")
    return False

# Test function
if __name__ == "__main__":
    test_text = "This is a test of the female voice system. It should work perfectly now."
    success = text_to_speech(test_text, "test_female.mp3")
    if success:
        print("✅ Test completed! Check test_female.mp3")
    else:
        print("❌ Test failed")