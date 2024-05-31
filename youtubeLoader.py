from langchain_community.document_loaders import YoutubeLoader

def load_youtube_documents(urls):
    loader = YoutubeLoader(urls, language=["ko"], add_video_info=True)
    document = loader.load()
    return document

if __name__ == "__main__":
    urls = "ztlAnZK4LB0"
    try:
        document = load_youtube_documents(urls)
        print(document)
        with open("document4.txt", "w") as f:
            f.write(document[0].page_content)
    except ValueError as e:
        print(e)