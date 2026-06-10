# script_maker.py - Convert Reddit posts to engaging stories
import random

# Different hooks for different story types
HORROR_HOOKS = [
    "I still get chills thinking about this...",
    "What happened that night still haunts me...",
    "This is the most terrifying experience of my life...",
    "I never believed in ghosts until this happened...",
    "The police still can't explain what happened..."
]

FUNNY_HOOKS = [
    "You won't believe how badly I messed up...",
    "This is the most embarrassing thing that ever happened to me...",
    "I still cringe every time I think about this...",
    "My friends still make fun of me for this...",
    "This went completely wrong in the best way possible..."
]

CONFESSION_HOOKS = [
    "I've never told anyone this before...",
    "This secret has been eating me alive...",
    "I need to get this off my chest...",
    "What I did still keeps me up at night...",
    "Nobody knows the real story until now..."
]

def detect_story_type(text):
    """Detect if story is horror, funny, or confession"""
    
    text_lower = text.lower()
    
    horror_words = ['scared', 'terror', 'haunt', 'ghost', 'dark', 'shadow', 'blood', 'kill', 'death', 'creepy', 'nightmare', 'afraid']
    funny_words = ['laugh', 'funny', 'hilarious', 'joke', 'embarrassing', 'cringe', 'stupid', 'dumb', 'awkward']
    
    horror_score = sum(1 for word in horror_words if word in text_lower)
    funny_score = sum(1 for word in funny_words if word in text_lower)
    
    if horror_score > funny_score:
        return "horror"
    elif funny_score > horror_score:
        return "funny"
    return "confession"

def clean_story(text):
    """Clean and format story for narration"""
    
    # Remove Reddit formatting
    text = text.replace('**', '')
    text = text.replace('*', '')
    text = text.replace('[removed]', '')
    text = text.replace('[deleted]', '')
    
    # Fix line breaks
    text = text.replace('\n\n', '. ')
    text = text.replace('\n', ' ')
    
    # Remove extra spaces
    import re
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def generate_script(post_text):
    """Generate engaging narration script from story"""
    
    # Clean the story
    story = clean_story(post_text)
    
    # Detect story type
    story_type = detect_story_type(story)
    
    # Select appropriate hook
    if story_type == "horror":
        hook = random.choice(HORROR_HOOKS)
    elif story_type == "funny":
        hook = random.choice(FUNNY_HOOKS)
    else:
        hook = random.choice(CONFESSION_HOOKS)
    
    # Get the main story (first 400 words for 50-60 sec)
    words = story.split()
    if len(words) > 350:
        story = ' '.join(words[:350]) + "..."
    
    # Build final script
    script = f"{hook} {story}"
    
    # Add conclusion
    conclusions = [
        " And that's the story. What would you have done?",
        " I'll never forget this for as long as I live.",
        " Sometimes life is stranger than fiction.",
        " Let me know what you think in the comments."
    ]
    script += random.choice(conclusions)
    
    print(f"[SCRIPT] Type: {story_type.upper()}")
    print(f"[SCRIPT] Length: {len(script)} chars, ~{len(script.split())} words")
    
    return script