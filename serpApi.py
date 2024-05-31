from langchain_community.utilities import SerpAPIWrapper
from documentToGPT import generate_headlines
from dotenv import load_dotenv
import os

def load_api_key():
    load_dotenv()
    return os.getenv("SERPAPI_API_KEY")

def search_results(video_id):
    text = generate_headlines(video_id)
    serp_api = SerpAPIWrapper(serpapi_api_key=load_api_key(), params={"engine": "google", "google_domain": "google.co.kr", "gl": "kr", "hl": "ko"})
    try:
        result = serp_api.results(query=text)
        if result and 'organic_results' in result:
            for organic in result['organic_results']:
                print(f"Title: {organic.get('title')}, snippet: {organic.get('snippet')}, link: {organic.get('link')}")
        else:
            print("No detailed organic results found.")
    except ValueError as e:
        print(f"Search failed: {e}")
    return result

# Example usage
result = search_results("3L7KnChvbFk")
