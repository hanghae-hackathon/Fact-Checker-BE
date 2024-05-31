```markdown
# YouTube URL Processor

이 프로젝트는 Flask를 사용하여 YouTube URL을 처리하고, 비디오 길이를 확인하며, 뉴스 문서와 유튜브 문서를 로드하여 헤드라인을 생성하고 검색 결과를 조회하는 기능을 제공합니다.

## 파일 구조

- `app/app.py`: Flask 애플리케이션의 메인 파일입니다.
- `app/storage/document_processors.py`: 문서 처리를 위한 클래스가 정의된 파일입니다.
- `app/storage/api_keys.py`: 환경 변수에서 API 키를 로드하는 클래스가 정의된 파일입니다.

## 설치 및 실행

### 1. 환경 설정

프로젝트를 클론한 후, 필요한 패키지를 설치합니다.

```bash
git clone <repository-url>
cd <repository-directory>
pip install -r requirements.txt
```

### 2. 환경 변수 설정

프로젝트 루트 디렉토리에 `.env` 파일을 생성하고, 필요한 API 키를 설정합니다.

```
DEVELOPER_KEY=your_youtube_api_key
OPENAI_API_KEY=your_openai_api_key
SERPAPI_API_KEY=your_serpapi_api_key
```

### 3. 애플리케이션 실행

Flask 애플리케이션을 실행합니다.

```bash
python app/app.py
```

## 주요 기능

### 1. YouTube 비디오 길이 확인

`get_video_duration(video_id)` 함수는 주어진 YouTube 비디오 ID에 해당하는 비디오의 길이를 초 단위로 반환합니다.

### 2. YouTube URL에서 비디오 ID 추출

`extract_youtube_id(url)` 함수는 주어진 URL에서 YouTube 비디오 ID를 추출합니다.

### 3. URL 유효성 검사 및 비디오 길이 확인

`check_url(url)` 함수는 주어진 URL이 유효한 YouTube 비디오 URL인지 확인하고, 비디오 길이를 체크합니다.

### 4. 문서 처리

`DocumentProcessor` 클래스는 뉴스와 유튜브 문서를 로드하고, 헤드라인을 생성하며, 검색 결과를 조회하는 기능을 제공합니다.

- `generate_headlines(document)`: 주어진 문서를 사용하여 헤드라인을 생성합니다.
- `search_results(text)`: 주어진 텍스트를 사용하여 Google 검색 결과를 조회합니다.
- `load_news_documents(urls)`: 주어진 URL 목록에서 뉴스 문서를 로드합니다.
- `load_youtube_documents(urls)`: 주어진 URL 목록에서 유튜브 문서를 로드합니다.
- `fact_check_api(headline, snippets)`: 주어진 헤드라인과 검색 결과를 사용하여 사실 여부를 판단합니다.

## API 엔드포인트

### `/get-result` (POST)

주어진 URL을 처리하여 결과를 반환하는 엔드포인트입니다.

- 요청 본문:
  ```json
  {
    "url": "https://www.youtube.com/watch?v=example"
  }
  ```

- 응답:
  ```json
  {
    "result": {
      "code": "success",
      "result": {
        "subject": "헤드라인",
        "percentage": 95,
        "summary": "이유",
        "news": [
          {
            "title": "뉴스 제목",
            "link": "https://news.link"
          }
        ]
      }
    }
  }
  ```

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.
```