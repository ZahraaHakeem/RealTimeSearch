import requests
from urllib.parse import urlparse

def process_search_results(data, trusted_domains):
    results = []
    if 'items' in data:
        for item in data['items']:  
            url = item['link']
            if url.startswith(('https://', 'www.')):  
                parsed_url = urlparse(url)
                domain = parsed_url.netloc.lower() 
                
                if any(domain.endswith(trusted_domain) for trusted_domain in trusted_domains):
                    results.append({
                        'title': item['title'],
                        'url': url,
                        'snippet': item.get('snippet', 'No snippet available')
                    })
    return results

def search_google(query, api_key, cx, trusted_domains):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cx}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return process_search_results(data, trusted_domains)  
    else:
        return []

def combine_search_results(query, api_key, cx, trusted_domains):
    google_results = search_google(query, api_key, cx, trusted_domains)
    return google_results

