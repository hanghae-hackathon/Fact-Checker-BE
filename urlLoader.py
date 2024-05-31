# from langchain_community.document_loaders import PlaywrightURLLoader
from langchain_community.document_loaders import NewsURLLoader
import json

def load_news_documents(urls):
    loader = NewsURLLoader(urls)
    document = loader.load()
    return document

# def load_documents_from_urls(urls):
#     if not isinstance(urls, list):
#         raise ValueError("urls must be a list of strings.")
    
#     loader = PlaywrightURLLoader(urls)
#     document = loader.load()
#     return document

if __name__ == "__main__":
    urls = ["https://n.news.naver.com/article/005/0001700234?type=editn&cds=news_edit"]
    try:
        loader = NewsURLLoader(urls)
        documents = loader.load()  # 문서 로드
        print(documents)
        with open("document3.txt", "w") as f:
            # JSON 형식으로 파일에 쓰기
            f.write(documents[0].page_content)  # 첫 번째 문서의 내용을 파일에 쓰기
    except ValueError as e:
        print(e)