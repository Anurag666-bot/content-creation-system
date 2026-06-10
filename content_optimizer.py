# content_optimizer.py - Fixed version
import random
import re

# Viral hooks for different content types
VIRAL_HOOKS = {
    "horror": [
        "WARNING: This story will haunt you...",
        "I couldn't sleep after reading this...",
        "What happened next will terrify you...",
        "This Reddit story is DISTURBING...",
    ],
    "funny": [
        "You won't believe what this person did...",
        "I'm literally crying laughing at this...",
        "This person had ONE JOB...",
        "The plot twist is absolutely insane...",
    ],
    "normal": [
        "This Reddit story went VIRAL...",
        "You need to hear this story...",
        "This will make you think differently...",
    ]
}

# Engagement triggers
ENGAGEMENT = [
    "What would YOU do in this situation?",
    "Comment your thoughts below",
    "Like if you agree with this",
    "Follow for more amazing stories",
]

def detect_content_type(text):
    """Auto-detect if story is horror, funny, or normal"""
    
    text_lower = text.lower()
    
    horror_keywords = ['scared', 'terror', 'haunt', 'ghost', 'dark', 'shadow', 'blood', 'kill', 'death', 'horror', 'creepy', 'nightmare']
    funny_keywords = ['laugh', 'funny', 'hilarious', 'joke', 'crack', 'lol', 'lmfao', 'stupid', 'dumb', 'crazy', 'embarrassing']
    
    horror_score = sum(1 for word in horror_keywords if word in text_lower)
    funny_score = sum(1 for word in funny_keywords if word in text_lower)
    
    if horror_score > funny_score:
        return "horror"
    elif funny_score > horror_score:
        return "funny"
    return "normal"

def optimize_script(script):
    """Add hooks and optimize for viral reach"""
    
    # Detect content type
    content_type = detect_content_type(script)
    
    # Add viral hook at beginning
    hook = random.choice(VIRAL_HOOKS.get(content_type, VIRAL_HOOKS["normal"]))
    enhanced = f"{hook}. {script}"
    
    # Add engagement trigger at end
    enhanced += f" {random.choice(ENGAGEMENT)}"
    
    # Clean up text for TTS
    enhanced = enhanced.replace('\n', ' ')
    enhanced = enhanced.replace('  ', ' ')
    
    # Remove special characters
    enhanced = re.sub(r'[^\w\s\.\!\?\,]', '', enhanced)
    
    # Limit length for Shorts (50-60 seconds = ~450-500 words)
    words = enhanced.split()
    if len(words) > 450:
        enhanced = ' '.join(words[:450]) + "..."
    
    print(f"[OPTIMIZER] Content type: {content_type.upper()}")
    print(f"[OPTIMIZER] Script length: {len(enhanced)} chars, {len(words)} words")
    
    return enhanced, content_type

# Test
if __name__ == "__main__":
    test = "I saw a ghost in my room last night and I'm terrified"
    optimized, ctype = optimize_script(test)
    print(f"Type: {ctype}")
    print(f"Optimized: {optimized[:100]}...")