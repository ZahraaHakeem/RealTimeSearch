import os
import requests
import serpapi
from dotenv import load_dotenv
from duckduckgo_search import DDGS
from moecolor import print
from moecolor import FormatText as ft

# Load API key from .env
load_dotenv()
serp_api_key = os.getenv("SERP_API_KEY")
news_api_key = os.getenv("NEWS_API_KEY")

def search_duckduckgo(query, limit=10):
    results = DDGS().text(query)
    return [{"Title": item["title"], "URL": item["href"], "Snippet": item["body"]} for item in results[:limit]] or \
           [{"Title": "No results found.", "URL": "", "Snippet": ""}]


def fetch_news(api_key, query, page_size=10):
    url = "https://newsapi.org/v2/everything"
    params = {"apiKey": api_key, "q": query, "pageSize": page_size, "sortBy": "relevancy"}
    news_results = requests.get(url, params=params).json().get("articles", [])
    return [{"Title": article.get("title", "No title available"), "URL": article.get("url", ""), 
             "Snippet": article.get("description", "No description available")} for article in news_results] or \
           [{"Title": "No relevant news articles found.", "URL": "", "Snippet": ""}]



query = input(ft("Enter your search query: ", color='yellow').text)

for source, results in [
    ("🔍 DuckDuckGo", search_duckduckgo(query)),
    ("📰 NewsAPI", fetch_news(news_api_key, query))]:
    
    print(ft(f"\n{source} Results for: {query}", color="blue"))
    for i, result in enumerate(results, 1):
        print(f"{ft(str(i), color='green')}. {ft('Title:', color='cyan')} {ft(result['Title'], color='yellow')}\n"
              f"   {ft('URL:', color='cyan')} {result['URL']}\n"
              f"   {ft('Snippet:', color='cyan')} {result['Snippet']}\n")







# def search_bing_serpapi(query, limit=10):
#     if not serp_api_key:
#         return [{"Title": "Missing SerpAPI Key.", "URL": "", "Snippet": "Set SERP_API_KEY in .env"}]
    
#     try:
#         client = serpapi.Client(api_key=serp_api_key)
#         results = client.search({'engine': 'bing', 'q': query}).get("organic_results", [])
#         return [{"Title": res.get("title", "No title"), "URL": res.get("link", ""), 
#                  "Snippet": res.get("snippet", "No snippet")} for res in results[:limit]] or \
#                [{"Title": "No results found.", "URL": "", "Snippet": ""}]
#     except Exception as e:
#         return [{"Title": "SerpAPI Error", "URL": "", "Snippet": str(e)}]