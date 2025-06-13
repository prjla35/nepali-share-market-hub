import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_article_content(url, headers):
    """
    Visits a single article URL and robustly extracts the main text content
    using the specific and reliable ID selector '#newsdetail-content'.
    """
    try:
        article_response = requests.get(url, headers=headers, timeout=10)
        article_response.raise_for_status()
        article_soup = BeautifulSoup(article_response.content, 'html.parser')
        
        # Using the more reliable ID selector from your target code
        # the '#' symbol selects by ID, which is less likely to change than a class
        content_div = article_soup.select_one('#newsdetail-content')
        
        if content_div:
            # .get_text() is more effective as it extracts all text from within the div,
            # and separator='\n' preserves line breaks for better readability
            return content_div.get_text(separator='\n', strip=True)
        else:
            return "FAILURE: Could not find the '#newsdetail-content' block on the article page."
            
    except requests.exceptions.RequestException as e:
        return f"FAILURE: Failed to load the article page. Error: {e}"

def scrape_upcoming_ipos():
    """
    Scrapes upcoming IPOs from ShareSansar, visits each article link,
    and extracts the full text content for detailed analysis.
    """
    list_url = "https://www.sharesansar.com/category/ipo-fpo-news"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        list_response = requests.get(list_url, headers=headers, timeout=10)
        list_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Error fetching IPO list URL: {e}"

    soup = BeautifulSoup(list_response.content, 'html.parser')
    articles_list = soup.find_all('div', class_='featured-news-list')

    if not articles_list:
        return "Could not find any articles on the main list page. The website layout may have changed."

    ipo_data = []
    
    # --- Limiting to the first 5 articles to keep scraping fast and efficient ---
    for article_div in articles_list[:5]:
        title_tag = article_div.find('h4', class_='featured-news-title')
        link_tag = article_div.find('a')
        date_tag = article_div.find('span', class_='text-org')

        if title_tag and link_tag and date_tag:
            title = title_tag.get_text(strip=True)
            link = link_tag['href']
            date = date_tag.get_text(strip=True)
            
            print(f"Deep scraping content for: {title}")
            # Use the robust helper function to get the full article content
            article_text = get_article_content(link, headers)
            
            # Append the complete record in a single pass
            ipo_data.append({
                "title": title, 
                "date": date, 
                "link": link, 
                "content": article_text
            })

    if not ipo_data:
        return "Found article containers, but could not extract any article details."

    return pd.DataFrame(ipo_data)
