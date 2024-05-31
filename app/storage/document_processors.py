from .api_keys import APIKeys
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain_community.utilities import SerpAPIWrapper
from langchain_community.document_loaders import NewsURLLoader, YoutubeLoader
from langchain_core.output_parsers import JsonOutputParser

class DocumentProcessor:
    """
    문서 처리를 위한 클래스로, OpenAI와 SerpAPI를 사용하여 문서의 헤드라인을 생성하고 검색 결과를 조회합니다.
    또한, 뉴스와 유튜브 문서를 로드하는 기능을 제공합니다.
    """
    def __init__(self):
        """
        API 키를 로드하여 클래스 변수에 저장합니다.
        """
        self.openai_api_key = APIKeys.load_key("OPENAI_API_KEY")
        self.serpapi_api_key = APIKeys.load_key("SERPAPI_API_KEY")

    def create_prompt_template(self):
        """
        OpenAI 모델을 사용할 때 전달할 프롬프트 템플릿을 생성합니다.
        """
        template = """
        아래 본문 내용을 기준으로 기사 헤드라인 검색어 1가지로 추출해주세요.
        반드시 한글로 답변하세요.
        본문 내용 ###{text}###
        """
        return PromptTemplate.from_template(template)

    def generate_headlines(self, document):
        """
        주어진 문서를 사용하여 헤드라인을 생성합니다.
        """
        prompt = self.create_prompt_template()
        llm = ChatOpenAI(api_key=self.openai_api_key, model='gpt-3.5-turbo-16k',temperature=0.0)
        chain = prompt | llm
        return chain.invoke({"text": document[0].page_content})

    def search_results(self, text):
        """
        주어진 텍스트를 사용하여 Google 검색 결과를 조회합니다.
        """
        serp_api = SerpAPIWrapper(serpapi_api_key=self.serpapi_api_key, params={"engine": "google", "google_domain": "google.co.kr", "gl": "kr", "hl": "ko"})
        try:
            result = serp_api.results(query=text)
            if result and 'organic_results' in result:
                return result
            else:
                print("No detailed organic results found.")
                return None
        except ValueError as e:
            print(f"Search failed: {e}")
            return None

    def load_news_documents(self, urls):
        """
        주어진 URL 목록에서 뉴스 문서를 로드합니다.
        """
        loader = NewsURLLoader(urls)
        return loader.load()

    def load_youtube_documents(self, urls):
        """
        주어진 URL 목록에서 유튜브 문서를 로드합니다.
        """
        loader = YoutubeLoader(urls, language=["ko"], add_video_info=True)
        return loader.load()
    
    def fact_check_api(self, headline, snippets):
        llm = ChatOpenAI(api_key=self.openai_api_key, temperature=0.0, model="gpt-4o")
        prompt = PromptTemplate.from_template("""
                                            헤드라인 = {headline}
                                            검색결과 = {snippets}
                                            헤드라인이 사실인지 검색결과를 통해 판단해줘
                                            헤드라인의 신뢰도를 0부터 100 정수형으로 반환해줘.
                                            그리고 그러한 이유를 설명해줘.
                                            결과를 다음 JSON 형식으로 반환해줘:
                                            {{
                                                "headline": "{headline}",
                                                "confidence": 신뢰도,
                                                "reason": "이유"
                                            }}
                                            """)

        chain = prompt | llm | JsonOutputParser()
        return chain.invoke({"headline": headline, "snippets": snippets})