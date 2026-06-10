# config.py - Optimized for stories
import os

# -------------------------
# REDDIT API
# -------------------------
REDDIT_CLIENT_ID = "vi7Sl14qtJMB2IK3LOqFhQ"
REDDIT_CLIENT_SECRET = "yiQ6--LQT6120yfnZgzrcMLAchXoKg"
REDDIT_USER_AGENT = "Content_video_bot"

# -------------------------
# SUBREDDITS (Story-focused)
# -------------------------
SUBREDDITS = [
    "tifu",           # Funny stories
    "nosleep",        # Horror stories  
    "confessions",    # Real confessions
    "LetsNotMeet",    # Creepy encounters
]

POST_LIMIT = 5

# -------------------------
# FILTERS (For stories)
# -------------------------
MIN_SCORE = 100       # Only popular stories
MIN_COMMENTS = 10     # Engaged stories
MAX_POST_LENGTH = 2000

# -------------------------
# VIDEO SETTINGS
# -------------------------
VIDEO_WIDTH = 720
VIDEO_HEIGHT = 1280
FPS = 24

TTS_LANG = "en"
MUSIC_FILE = "assets/music.mp3"

OUTPUT_DIR = "outputs/"