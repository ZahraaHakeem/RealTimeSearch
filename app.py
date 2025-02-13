from duckduckgo_search import DDGS
from moecolor import print
from moecolor import FormatText as ft
from typing import List, Dict

def search_duckduckgo(query):
    seen_urls = set()
    search = DDGS()
    results = search.text(query)
    duckduckgo_results = []
    for item in results[:5]:  
        url = item['href']
        if url not in seen_urls:
            seen_urls.add(url)
            duckduckgo_results.append({
                'title': item['title'],
                'url': url,
                'snippet': item['body']
            })
    return duckduckgo_results

results: List[Dict] = search_duckduckgo(input(ft("Enter your search query: ", color='yellow').text))
for result in results:
    for k, v in result.items():
        print(f"{ft(k, color='green')}: {v}")
    print("*" * 75)