import streamlit as st
import pandas as pd
import json
from search_system import combine_search_results  

def load_api_keys(config_file='config.json'):
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config

keys = load_api_keys()
api_key = keys.get('API_KEY')
cx = keys.get('CX')

st.title("Search Results Viewer")
query = st.text_input("Enter your search query:", key="search_query_input")

trusted_domains = ['.edu', '.gov', '.net', '.org', '.com']

if query and api_key and cx:
    results = combine_search_results(query, api_key, cx, trusted_domains)
    if results:
        # Display Google results first
        st.markdown("# Google Search Results")
        google_results = results[:5] 
        for idx, result in enumerate(google_results, 1):
            st.subheader(f"{result['title']}")
            st.write(f"[{result['url']}]({result['url']})")
            st.write(f"{result['snippet']}")
            st.markdown("---")
        
        # Display DuckDuckGo results
        st.markdown("# DuckDuckGo Search Results")
        duckduckgo_results = results[5:10]  
        for idx, result in enumerate(duckduckgo_results, 1):
            st.subheader(f"{result['title']}")
            st.write(f"[{result['url']}]({result['url']})")
            st.write(f"{result['snippet']}")
            st.markdown("---")

        df = pd.DataFrame(results, columns=['title', 'url', 'snippet'])
        st.markdown("### Results DataFrame")
        st.dataframe(df)

else:
    st.write("Please enter a search query.")
