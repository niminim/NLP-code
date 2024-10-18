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


from transformers import pipeline
sentiment_analysis = pipeline('sentiment-analysis')


# Add sentiment analysis to the article title and summary
def analyze_sentiment(text):
    result = sentiment_analysis(text)[0]
    return {'label': result['label'], 'score': result['score']}


# Fetch articles and perform sentiment analysis
def get_all_articles_with_sentiment(rss_urls):
    all_articles = []
    for url in rss_urls:
        articles = get_rss_articles(url)
        for article in articles:
            # Perform sentiment analysis on the title
            title_sentiment = analyze_sentiment(article['title'])

            # Perform sentiment analysis on the summary
            summary_sentiment = analyze_sentiment(article['summary'])

            # Add sentiment analysis results to the article dictionary
            article['title_sentiment'] = title_sentiment
            article['summary_sentiment'] = summary_sentiment

            all_articles.append(article)
    return all_articles


# Example usage
all_articles = get_all_articles_with_sentiment(rss_urls)

# Print articles with sentiment analysis results
for article in all_articles:
    print(f"Title: {article['title']}")
    print(f"Title Sentiment: {article['title_sentiment']}")
    print(f"Summary: {article['summary']}")
    print(f"Summary Sentiment: {article['summary_sentiment']}")
    print(f"Link: {article['link']}")
    print("\n" + "="*100 + "\n")
