
import feedparser
import requests
from bs4 import BeautifulSoup

# Example RSS feed URLs
rss_urls = [
    'https://www.cnbc.com/id/10001147/device/rss/rss.html',  # CNBC
    # 'http://feeds.bbci.co.uk/news/business/rss.xml',  # BBC Business
    # 'https://feeds.a.dj.com/rss/RSSMarketsMain.xml',  # Wall Street Journal (requires subscription)
    # 'https://finance.yahoo.com/news/rssindex'  # Yahoo Finance
]


def get_rss_articles(rss_url):
    feed = feedparser.parse(rss_url)
    articles = []

    for entry in feed.entries:
        articles.append({
            'title': entry.get('title', 'No title available'),
            'link': entry.get('link', 'No link available'),
            'published': entry.get('published', 'No published date available'),
            'summary': entry.get('summary', 'No summary available')  # Get the summary from the RSS feed
        })

    return articles


# Function to scrape the full article from the link
def scrape_full_article(link):
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Example for CNBC, adjust as necessary based on the site's structure
        article_body = soup.find('div', class_='ArticleBodyWrapper')  # Adjust this for each site

        if article_body:
            paragraphs = article_body.find_all('p')
            full_text = ' '.join([p.get_text() for p in paragraphs])
            return full_text
        else:
            return "Could not find full article content."
    except Exception as e:
        return f"Error scraping article: {e}"


# Fetch full articles for all RSS feed URLs
def get_all_articles_with_full_content(rss_urls):
    all_articles = []
    for url in rss_urls:
        articles = get_rss_articles(url)
        for article in articles:
            # Scrape full article content
            full_content = scrape_full_article(article['link'])
            article['full_content'] = full_content
            all_articles.append(article)
    return all_articles


# Example usage
all_articles = get_all_articles_with_full_content(rss_urls)

# Print full articles along with summaries
for article in all_articles:
    print(f"Title: {article['title']}")
    print(f"Link: {article['link']}")
    print(f"Published: {article['published']}")
    print(f"Summary: {article['summary']}")
    print(f"Full Content: {article['full_content'][:500]}...")  # Print first 500 characters of full article
    print("\n" + "=" * 100 + "\n")