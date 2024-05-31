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
                result = {
                    "code":'success',
                    "result":{
                        "subject":"서울 도심 까마귀 출현",
                        "percentage":71,
                        "summary":"서울에서 까마귀가 민간인을 공격하는 사건은 사실입니다. 최근 서울 도심에서 까마귀가 사람을 공격하는 사례가 늘어나고 있으며, 이는 주로 까마귀의 새끼들이 둥지를 떠나는 시기인 5월에서 6월 사이에 발생하는 것으로 보고됩니다. 전문가들은 이 기간 동안 까마귀가 새끼를 보호하려는 본능 때문에 사람을 위협으로 느껴 공격성을 보일 수 있다고 설명합니다.주민들은 이러한 공격성 때문에 공포를 느끼고 있으며, 일부 지역에서는 까마귀 출몰 구역에 안전선을 설치해 주민 출입을 통제하기도 했습니다​.",
                        "news":[
                            {"title":"까마귀 습격' 잇단 제보...서울 한복판서 공격당해 [앵커리포트]","link":"https://www.ytn.co.kr/_ln/0103_202405291506066773"},
                            {"title":"[제보는Y] 강남 한복판에서 '까마귀 습격'…\"번식기 영향\"","link":"https://news.nate.com/view/20240529n01764"},
                            {"title":"까마귀","link":"https://namu.wiki/w/%EA%B9%8C%EB%A7%88%EA%B7%80"},
                            {"title":"[제보는Y] 강남 한복판에서 '까마귀 습격'...\"번식기 영향\"","link":"https://science.ytn.co.kr/program/view.php?mcd=0082&key=202405291115040451"},
                            {"title":"\"새가 사람 공격한다\"…도심 한복판서 까마귀 습격","link":"https://www.newsis.com/view/?id=NISX20240529_0002752574"},
                            {"title":"강남 한복판 걷다 '뒤통수' 쪼였다..'까마귀 습격'에 무대책","link":"https://www.fnnews.com/news/202405290956099131"},
                            {"title":"\"나도 길 가다 당했다\" 쏟아진 제보…'까마귀 공격' 급증 - SBS 뉴스","link":"http://news.sbs.co.kr/news/endPage.do?news_id=N1007666969"}
                        ]
                    }
                }
                ## youtubue func
            else:
                return jsonify(is_youtube), 400
        else:
            result = {
                "code":'success',
                "result":{
                    "subject":"서울 도심 까마귀 출현",
                    "percentage":71,
                    "summary":"서울에서 까마귀가 민간인을 공격하는 사건은 사실입니다. 최근 서울 도심에서 까마귀가 사람을 공격하는 사례가 늘어나고 있으며, 이는 주로 까마귀의 새끼들이 둥지를 떠나는 시기인 5월에서 6월 사이에 발생하는 것으로 보고됩니다. 전문가들은 이 기간 동안 까마귀가 새끼를 보호하려는 본능 때문에 사람을 위협으로 느껴 공격성을 보일 수 있다고 설명합니다.주민들은 이러한 공격성 때문에 공포를 느끼고 있으며, 일부 지역에서는 까마귀 출몰 구역에 안전선을 설치해 주민 출입을 통제하기도 했습니다​.",
                    "news":[
                        {"title":"까마귀 습격' 잇단 제보...서울 한복판서 공격당해 [앵커리포트]","link":"https://www.ytn.co.kr/_ln/0103_202405291506066773"},
                        {"title":"[제보는Y] 강남 한복판에서 '까마귀 습격'…\"번식기 영향\"","link":"https://news.nate.com/view/20240529n01764"},
                        {"title":"까마귀","link":"https://namu.wiki/w/%EA%B9%8C%EB%A7%88%EA%B7%80"},
                        {"title":"[제보는Y] 강남 한복판에서 '까마귀 습격'...\"번식기 영향\"","link":"https://science.ytn.co.kr/program/view.php?mcd=0082&key=202405291115040451"},
                        {"title":"\"새가 사람 공격한다\"…도심 한복판서 까마귀 습격","link":"https://www.newsis.com/view/?id=NISX20240529_0002752574"},
                        {"title":"강남 한복판 걷다 '뒤통수' 쪼였다..'까마귀 습격'에 무대책","link":"https://www.fnnews.com/news/202405290956099131"},
                        {"title":"\"나도 길 가다 당했다\" 쏟아진 제보…'까마귀 공격' 급증 - SBS 뉴스","link":"http://news.sbs.co.kr/news/endPage.do?news_id=N1007666969"}
                    ]
                }
            }
        
    try:
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
