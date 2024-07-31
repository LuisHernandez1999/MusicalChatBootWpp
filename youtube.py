from googleapiclient.discovery import build
import random
from config import YOUTUBE_API_KEY, YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, ARTISTAS_TRISTES, ARTISTAS_FELIZES

def search_videos(artist):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        part="snippet",
        maxResults=5,
        q=artist,
        type="video"
    )
    response = request.execute()
    
    videos = []
    for item in response['items']:
        video_id = item['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        videos.append(video_url)
        
    return videos

def get_youtube_playlist(vibe):
    playlists = []
    if vibe in ["triste", "reflexiva"]:
        for artist in ARTISTAS_TRISTES:
            videos = search_videos(artist)
            if videos:
                playlists.extend(videos)
    elif vibe in ["feliz", "normal", "boa", "animada"]:
        for artist in ARTISTAS_FELIZES:
            videos = search_videos(artist)
            if videos:
                playlists.extend(videos)
    random.shuffle(playlists)
    return playlists[:3]