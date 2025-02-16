import os
import requests
from dotenv import load_dotenv
from duckduckgo_search import DDGS
from moecolor import print
from moecolor import FormatText as ft
import json


load_dotenv()
news_api_key = os.getenv("NEWS_API_KEY")
serper_api_key = os.getenv("SERPER_KEY")

# Function to search using DuckDuckGo
def search_duckduckgo(query, limit=10):
    results = DDGS().text(query)
    return [{"Title": item["title"], "URL": item["href"], "Snippet": item["body"]} for item in results[:limit]] or \
           [{"Title": "No results found.", "URL": "", "Snippet": ""}]



# Function to fetch news using NewsAPI
def fetch_news(api_key, query, page_size=10):
    url = "https://newsapi.org/v2/everything"
    params = {"apiKey": api_key, "q": query, "pageSize": page_size, "sortBy": "relevancy"}
    news_results = requests.get(url, params=params).json().get("articles", [])
    return [{"Title": article.get("title", "No title available"), "URL": article.get("url", ""), 
             "Snippet": article.get("description", "No description available")} for article in news_results] or \
           [{"Title": "No relevant news articles found.", "URL": "", "Snippet": ""}]



# Function to fetch Google search results using Serper API
def search_serper(api_key, query, limit=20):
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query , "num": limit})
    headers = {'X-API-KEY': api_key, 'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.json()
    results = []
    if "organic" in data:
        results = [{"Title": item["title"], "URL": item["link"], "Snippet": item.get("snippet", "No description available")}
                   for item in data["organic"][:limit]]
    knowledge_graph = fetch_knowledge_graph_with_serper(data)
    return results or [{"Title": "No search results found.", "URL": "", "Snippet": ""}], knowledge_graph


# Function to fetch Knowledge Graph Google search results using Serper API
def fetch_knowledge_graph_with_serper(data):
    if "knowledgeGraph" in data and data["knowledgeGraph"]:
        return data["knowledgeGraph"]
    return None 


query = input(ft("Enter your search query: ", color='yellow').text)
google_results, knowledge_graph = search_serper(serper_api_key, query)


for source, results in [
    ("🔍 DuckDuckGo", search_duckduckgo(query)),
    ("📰 NewsAPI", fetch_news(news_api_key, query)),
    ("🌐 Google (Serper)", google_results)
    ]:
    
    print(ft(f"\n{source} Results for: {query}", color="blue"))
    for i, result in enumerate(results, 1):
        print(f"{ft(str(i), color='green')}. {ft('Title:', color='cyan')} {ft(result['Title'], color='yellow')}\n"
              f"   {ft('URL:', color='cyan')} {result['URL']}\n"
              f"   {ft('Snippet:', color='cyan')} {result['Snippet']}\n")


if knowledge_graph:
    print(ft("\n🎯 Knowledge Graph Information 🎯", color="magenta"))
    for key, value in knowledge_graph.items():
        if key == "attributes":
            print(ft("\n📌 Additional Details:", color="cyan"))
            for attr_key, attr_value in value.items():
                print(f"  - {ft(attr_key, color='yellow')}: {attr_value}")
        else:
            print(f"{ft(key.capitalize(), color='green')}: {value}")
