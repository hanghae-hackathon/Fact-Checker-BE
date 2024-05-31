from flask import Flask, request, jsonify
from apiclient.discovery import build
from apiclient.errors import HttpError
from dotenv import dotenv_values
import isodate
import importlib.util
import os
import re
from storage.document_processors import DocumentProcessor

app = Flask(__name__)
env = dotenv_values()
DP = DocumentProcessor()
DEVELOPER_KEY = env['DEVELOPER_KEY']
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
SCRIPTS_FOLDER = '../langchain'
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

def get_video_duration(video_id):
    """
    주어진 유튜브 비디오 ID에 해당하는 비디오의 길이를 초 단위로 반환합니다.
    
    Args:
        video_id (str): 유튜브 비디오 ID.
    
    Returns:
        float: 비디오 길이(초).
    """
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
    """
    주어진 URL에서 유튜브 비디오 ID를 추출합니다.
    
    Args:
        url (str): 유튜브 비디오 URL.
    
    Returns:
        str: 추출된 유튜브 비디오 ID.
    """
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
    """
    주어진 URL이 유효한 유튜브 비디오 URL인지 확인하고, 비디오 길이를 체크합니다.
    
    Args:
        url (str): 유튜브 비디오 URL.
    
    Returns:
        dict or str: 유효하지 않은 경우 에러 메시지, 유효한 경우 유튜브 비디오 ID.
    """
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
    """
    주어진 URL을 처리하여 결과를 반환하는 엔드포인트.
    
    Returns:
        Response: JSON 형식의 결과.
    """
    data = request.get_json()
    requested_url = data.get('url')
    if not requested_url:
        return jsonify({"error": "script_name and function_name are required"}), 400
    else:
        is_youtube = check_url(requested_url)
        if is_youtube is not None:
            if type(is_youtube) == str:
                script = DP.load_youtube_documents(is_youtube)
            else:
                return jsonify(is_youtube), 400
        else:
            script = DP.load_news_documents(requested_url)            
        headline = DP.generate_headlines(script)
        search_query = headline.content + "site:kbs.co.kr OR site:yna.co.kr OR site:chosun.com OR site:imbc.com OR site:sbs.co.kr OR site:jtbc.co.kr OR site:ytn.co.kr"
        serp_result = DP.search_results(search_query)
        if serp_result:
            snippets = ""
            for organic in serp_result['organic_results']:
                snippets += organic.get('snippet')
            result = DP.fact_check_api(headline.content , snippets)
            result_json =  {
                "code":'success',
                "result":{
                    "subject":result.get('headline'),
                    "percentage":result.get('confidence'),
                    "summary":result.get('reason'),
                    "news":[
                        {"title":organic.get('title'), "link":organic.get('link')} for organic in serp_result['organic_results'] 
                    ]
                }
            }
            
        else:
            result_json = {
                "code":"success",
                "result":{
                    "subject":headline.content,
                    "percentage":0,
                    "summary":"신뢰도가 높은 언론사의 헤드라인 검색결과가 없습니다.",
                    "news":[
                        {"title": "KBS 검색 결과 없음", "link": "https://kbs.co.kr"},
                        {"title": "연합뉴스 검색 결과 없음", "link": "https://yna.co.kr"},
                        {"title": "조선일보 검색 결과 없음", "link": "https://chosun.com"},
                        {"title": "MBC 검색 결과 없음", "link": "https://imbc.com"},
                        {"title": "SBS 검색 결과 없음", "link": "https://sbs.co.kr"},
                        {"title": "JTBC 검색 결과 없음", "link": "https://jtbc.co.kr"},
                        {"title": "YTN 검색 결과 없음", "link": "https://ytn.co.kr"}
                    ]
                }
            }        
    try:
        return jsonify({"result": result_json}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)