import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from youtubeLoader import load_youtube_documents

def setup_openai_api():
    load_dotenv()
    return os.getenv("OPENAI_API_KEY")

def create_prompt_template():
    template = """
    아래 본문 내용을 기준으로 기사 헤드라인 검색어 1가지로 추출해주세요.
    반드시 한글로 답변하세요.
    본문 내용 ###{text}###
    """
    return PromptTemplate.from_template(template)

def get_documents(video_id):
    return load_youtube_documents(video_id)

def generate_headlines(video_id):
    OPENAI_API_KEY = setup_openai_api()
    documents = get_documents(video_id)
    if not documents:
        return "No documents found for the given video ID."
    prompt = create_prompt_template()
    llm = OpenAI(api_key=OPENAI_API_KEY, temperature=0.0)
    chain = prompt | llm
    print("doc : ", documents[0].page_content)
    return chain.invoke({"text": documents[0].page_content})