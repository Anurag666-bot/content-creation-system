# scraper.py - Get REAL stories (not questions)
import praw
import os
import random
from config import (
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_USER_AGENT,
    SUBREDDITS,
    POST_LIMIT
)

USED_FILE = "used_posts.txt"

def is_used(post_id):
    if not os.path.exists(USED_FILE):
        return False
    with open(USED_FILE, "r") as f:
        return post_id in f.read()

def save_used(post_id):
    with open(USED_FILE, "a") as f:
        f.write(post_id + "\n")

def is_real_story(post):
    """Check if post is a real story, not a question"""
    
    # Skip if title ends with question mark (questions)
    if post.title.strip().endswith('?'):
        return False
    
    # Skip question words in title
    question_words = ['what', 'why', 'how', 'does', 'do you', 'would you', 'should i', 'is it']
    title_lower = post.title.lower()
    for word in question_words:
        if title_lower.startswith(word):
            return False
    
    # Must have enough text content
    if not post.selftext or len(post.selftext) < 200:
        return False
    
    return True

def get_reddit_posts():
    """Get REAL storytelling posts"""
    
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )
    
    posts = []
    
    # Story-focused subreddits
    story_subreddits = [
        "tifu",           # Today I Fucked Up (funny stories)
        "nosleep",        # Horror stories
        "confessions",    # Real confessions
        "LetsNotMeet",    # Creepy encounters
        "TalesFromRetail", # Work stories
        "ProRevenge",     # Revenge stories
        "MaliciousCompliance",
        "IDontWorkHereLady",
        "Glitch_in_the_Matrix"
    ]
    
    for sub_name in story_subreddits:
        print(f"[SCRAPER] Getting stories from r/{sub_name}")
        
        try:
            subreddit = reddit.subreddit(sub_name)
            
            # Get top stories from this week
            for post in subreddit.top(time_filter="week", limit=15):
                try:
                    # Skip if already used
                    if is_used(post.id):
                        continue
                    
                    # Skip stickied posts
                    if post.stickied:
                        continue
                    
                    # Check if it's a real story
                    if not is_real_story(post):
                        continue
                    
                    # Format as a story
                    story = f"{post.title}\n\n"
                    story += post.selftext[:800]  # Get first 800 chars
                    
                    # Clean up the text
                    story = story.replace('\n\n\n', '\n\n')
                    story = story.replace('\r', '')
                    
                    posts.append(story)
                    save_used(post.id)
                    print(f"[✓] Story: {post.title[:50]}...")
                    
                    if len(posts) >= POST_LIMIT:
                        print(f"[SCRAPER] Collected {len(posts)} stories")
                        return posts
                        
                except Exception as e:
                    print(f"  Skip: {e}")
                    continue
                    
        except Exception as e:
            print(f"[ERROR] r/{sub_name}: {e}")
            continue
    
    # If no stories found, try horror subreddits
    if len(posts) == 0:
        print("[SCRAPER] Trying horror subreddits...")
        for sub_name in ["nosleep", "creepypasta", "LetsNotMeet"]:
            try:
                subreddit = reddit.subreddit(sub_name)
                for post in subreddit.top(time_filter="month", limit=10):
                    if not is_used(post.id) and post.selftext and len(post.selftext) > 300:
                        story = f"{post.title}\n\n{post.selftext[:800]}"
                        posts.append(story)
                        save_used(post.id)
                        print(f"[✓] Horror: {post.title[:50]}...")
                        if len(posts) >= POST_LIMIT:
                            return posts
            except:
                continue
    
    print(f"[SCRAPER] Found {len(posts)} stories")
    return posts