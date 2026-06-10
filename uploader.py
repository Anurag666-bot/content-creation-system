import os
import pickle
import random

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def get_authenticated_service():
    creds = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secret.json", SCOPES
        )
        creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("youtube", "v3", credentials=creds)


# 🔥 VIRAL TITLES
TITLES = [
    "This Reddit Story Is INSANE 😱",
    "You Won’t Believe This 😳",
    "This Actually Happened… 😨",
    "Reddit Never Fails 😂",
    "This Story Is Crazy 🤯"
]


def upload_video(file_path, script):

    youtube = get_authenticated_service()

    title = random.choice(TITLES)

    description = script[:200] + "\n\n#shorts #reddit #story #viral"

    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["reddit", "story", "shorts", "viral"],
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": "public"
        }
    }

    media = MediaFileUpload(file_path, resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )

    response = request.execute()

    print(f"[UPLOAD SUCCESS] Video ID: {response['id']}")