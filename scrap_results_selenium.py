from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_yahoo_selenium(query, num_results=10):
    # Setup WebDriver with optimized options
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--window-size=1200,900")
    options.page_load_strategy = 'eager'  # Load page faster
    
    # Block unnecessary resources but keep CSS 
    options.add_experimental_option(
        "prefs", {
            "profile.managed_default_content_settings.images": 2,
            "profile.managed_default_content_settings.plugins": 2,
            "profile.managed_default_content_settings.popups": 2,
            "profile.managed_default_content_settings.geolocation": 2,
            "profile.managed_default_content_settings.notifications": 2,
        }
    )
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    
    # Set page load timeout
    driver.set_page_load_timeout(10)
    
    try:
        # Open Yahoo search
        url = f"https://search.yahoo.com/search?p={query.replace(' ', '+')}"
        start_time = time.time()
        driver.get(url)
        
        # Extract search results
        search_results = []
        
        # Get all the result containers
        result_containers = driver.find_elements(By.CSS_SELECTOR, "div.algo.algo-sr")
        
        # Process each result container (limited to num_results)
        for container in result_containers[:num_results]:
            try:
                # Extract title and link
                title_element = container.find_element(By.CSS_SELECTOR, "h3.title")
                link_element = title_element.find_element(By.TAG_NAME, "a")
                title = title_element.text.strip()
                link = link_element.get_attribute("href")
                
                # Extract snippet (located in a paragraph after the title)
                try:
                    snippet_element = container.find_element(By.CSS_SELECTOR, "div.compText p")
                    snippet = snippet_element.text.strip()
                except:
                    snippet = "No snippet available"
                
                search_results.append({
                    "title": title,
                    "url": link,
                    "snippet": snippet
                })
            except Exception as e:
                print(f"Error processing result: {e}")
                continue
        
        end_time = time.time()
        print(f"Scraping completed in {end_time - start_time:.2f} seconds \n")
        
    except Exception as e:
        print(f"Error: {e}")
        search_results = []
    finally:
        driver.quit()
    
    return search_results

if __name__ == "__main__":
    query = input("Enter your search query: ")
    results = scrape_yahoo_selenium(query)
    
    # Print results in the requested format
    for result in results:
        print(f"Title: {result['title']}")
        print(f"URL: {result['url']}")
        print(f"Snippet: {result['snippet']}\n ______________ \n")
