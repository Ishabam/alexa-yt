import json
import requests

# Replace with your actual YouTube Data API key
YOUTUBE_API_KEY = "AIzaSyBoN9ppCx-6ePpd0h55Jzs4Sw-ex7stNPs"
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

def search_youtube(song_name):
    """Search YouTube for a song and return the video URL of the first result."""
    params = {
        "part": "snippet",
        "q": song_name,
        "key": YOUTUBE_API_KEY,
        "type": "video",
        "maxResults": 1
    }
    
    response = requests.get(YOUTUBE_SEARCH_URL, params=params)
    response_json = response.json()
    
    # Check if any items are returned
    if "items" in response_json and len(response_json["items"]) > 0:
        video_id = response_json["items"][0]["id"]["videoId"]
        video_title = response_json["items"][0]["snippet"]["title"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        return video_title, video_url
    else:
        return None, None

def lambda_handler(event, context):
    # Extract song name from Alexa's request
    try:
        song_name = event['request']['intent']['slots']['song']['value']
    except KeyError:
        return {
            'statusCode': 200,
            'body': json.dumps("I couldn't understand the song name. Please try again.")
        }
    
    # Search for the song on YouTube
    video_title, video_url = search_youtube(song_name)
    
    if video_url:
        # Respond to Alexa with the song title and URL
        return {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": f"I found {video_title} on YouTube. You can watch it here: {video_url}"
                },
                "shouldEndSession": True
            }
        }
    else:
        # Respond to Alexa if no video is found
        return {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "I couldn't find that song on YouTube. Please try another title."
                },
                "shouldEndSession": True
            }
        }
