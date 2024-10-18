import feedparser

# Example RSS feed URL from Yahoo Finance (and others)
rss_urls = [
    # 'https://www.cnbc.com/id/10001147/device/rss/rss.html',  # CNBC
    # 'http://feeds.bbci.co.uk/news/business/rss.xml',  # BBC Business
    'https://feeds.a.dj.com/rss/RSSMarketsMain.xml',  # Wall Street Journal (requires subscription)
    # 'https://finance.yahoo.com/news/rssindex'  # Yahoo Finance (may lack 'summary')
]

def get_rss_articles(rss_url):
    feed = feedparser.parse(rss_url)
    articles = []

    for entry in feed.entries:
        articles.append({
            'link': entry.get('link', 'No link available'),
            'published': entry.get('published', 'No published date available'),
            'title': entry.get('title', 'No title available'),
            'summary': entry.get('summary', 'No summary available')  # Get the summary from the RSS feed
        })

    return articles

# Get articles from all feeds
def get_all_articles(rss_urls):
    all_articles = []
    for url in rss_urls:
        articles = get_rss_articles(url)
        all_articles.extend(articles)
    return all_articles

# Fetch and print all articles
all_articles = get_all_articles(rss_urls)

for article in all_articles:
    print(f"Link: {article['link']}")
    print(f"Published: {article['published']}")
    print(f"Title: {article['title']}")
    print(f"Summary: {article['summary']}")


