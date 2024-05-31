from flask import Flask, request, jsonify
from apiclient.discovery import build
from apiclient.errors import HttpError
from dotenv import dotenv_values
import isodate
import importlib.util
import os
import re

app = Flask(__name__)
env = dotenv_values()
DEVELOPER_KEY = env['DEVELOPER_KEY']
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
SCRIPTS_FOLDER = '../langchain'
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

def get_video_duration(video_id):
    request = youtube.videos().list(
        part="contentDetails",
        id=video_id
    )
    response = request.execute()

    if not response["items"]:
        return None

    duration = response["items"][0]["contentDetails"]["duration"]
    duration_seconds = isodate.parse_duration(duration).total_seconds()
    return duration_seconds

def extract_youtube_id(url):
    youtube_regex = re.compile(
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')
    
    match = youtube_regex.match(url)
    
    if match:
        return match.group(6)
    else:
        return None

def check_url(url:str):
    youtube_id = extract_youtube_id(url)
    if youtube_id:
        duration_seconds = get_video_duration(youtube_id)
        if duration_seconds is not None:
            if duration_seconds >= 600:
                return {"error":"video is too long"}
            else:
                return youtube_id
        else:
            return {"error":"Invalid URL"}
    else:
        return None 
    
@app.route('/get-result', methods=['POST'])
def execute_script():
    data = request.get_json()
    requested_url = data.get('url')
    if not requested_url:
        return jsonify({"error": "script_name and function_name are required"}), 400
    else:
        is_youtube = check_url(requested_url)
        if is_youtube is not None:
            if type(is_youtube) == str:
                result = 'success'
                 ## youtubue func
            else:
                return jsonify(is_youtube), 400
        else:
            result = 'success'
            ## article func
        
    try:
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
