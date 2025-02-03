import requests
from urllib.parse import urlparse
from duckduckgo_search import DDGS

def process_search_results(data, trusted_domains, seen_urls):
    results = []
    if 'items' in data:
        for item in data['items']:  
            url = item['link']
            if url.startswith(('https://', 'www.')):  
                parsed_url = urlparse(url)
                domain = parsed_url.netloc.lower() 

                if any(domain.endswith(trusted_domain) for trusted_domain in trusted_domains) and url not in seen_urls:
                    seen_urls.add(url)
                    results.append({
                        'title': item['title'],
                        'url': url,
                        'snippet': item.get('snippet', 'No snippet available')
                    })
    return results

def search_google(query, api_key, cx, trusted_domains, seen_urls):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cx}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return process_search_results(data, trusted_domains, seen_urls)  
    else:
        return []

def search_duckduckgo(query, seen_urls):
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

def combine_search_results(query, api_key, cx, trusted_domains):
    seen_urls = set()  # don't allow duplicates URLs
    google_results = search_google(query, api_key, cx, trusted_domains, seen_urls)
    duckduckgo_results = search_duckduckgo(query, seen_urls)
    combined_results = google_results + duckduckgo_results
    return combined_results
