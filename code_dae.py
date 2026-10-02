# ==============================================================================
# LIVE SOCIAL MEDIA DATA ANALYSIS
# Real-Time Sentiment Analysis of Social Media & Online News Content
# ==============================================================================
#
# Team Details
#
# Time Table: 2
# Team Number: 14
#
# Team Leader
#     S. Penchala Chaitanya       Roll Number: 25B11CS902
#
# Team Members
#     1    S. Penchala Chaitanya     25B11CS902
#     2    Konappagari Pandu         25B11CS457
#     3    S. Radha Sai Lakshmi      25B11CS854
#     4    M. Divya                  25B11CS520
#
# ==============================================================================


# ==============================================================================
# 1. Project Overview
# ------------------------------------------------------------------------------
# This project focuses on analysing live social-media and news-related online
# information using data analysis and visualization techniques. The system
# collects current posts and articles through RSS feeds and a public API,
# preprocesses the collected text, performs sentiment analysis and keyword
# analysis, and presents the results through a six-panel analytical dashboard.
#
# The project demonstrates how continuously changing online information can
# be collected and transformed into meaningful insights using Python,
# Pandas, VADER Sentiment Analysis, Matplotlib, Feedparser, and Requests.
# ==============================================================================


# ==============================================================================
# 2. Libraries Used
# ------------------------------------------------------------------------------
# The project uses the following Python libraries:
#     - re          : Regular expressions for text cleaning
#     - html        : HTML entity handling (&amp; -> &)
#     - requests    : HTTP requests to public APIs
#     - feedparser  : RSS feed parsing
#     - pandas      : Data manipulation and analysis
#     - matplotlib  : Data visualization
#     - datetime    : Date and time handling
#     - Counter     : Keyword frequency counting
#     - vaderSentiment : Sentiment analysis (VADER)
# ==============================================================================

import re
import html
import requests
import feedparser
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime
from collections import Counter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# ==============================================================================
# 3. Settings and Configuration
# ------------------------------------------------------------------------------
# All adjustable parameters are defined here so the project can be easily
# modified without changing the main logic.
# ==============================================================================

MAX_ITEMS = 40          # Maximum items per RSS feed
TOP_N_WORDS = 12        # Number of top keywords to display

# Sentiment category colors
COLORS = {
    "Negative": "#E74C3C",   # red
    "Neutral":  "#B0B7BD",   # gray
    "Positive": "#2ECC71",   # green
}
MOODS = ["Negative", "Neutral", "Positive"]

# Common stopwords removed during keyword analysis
STOP_WORDS = {
    "the","and","for","that","with","was","are","this","from","have","has",
    "had","not","but","his","her","its","they","their","them","will","would",
    "could","should","been","were","who","what","when","where","which","while",
    "about","after","before","into","over","than","then","there","these",
    "those","also","more","most","some","such","only","other","just","how",
    "why","you","your","can","all","out","our","she","him","one","two","new",
    "say","says","said","year","years","amp","because","against","between",
    "during","under","may","now","does","did","get","got","link","https",
    "http","com","www",
}

# Initialize the VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()


# ==============================================================================
# 4. Helper Functions
# ------------------------------------------------------------------------------
# Small reusable functions used throughout the data-analysis pipeline.
# ==============================================================================

def clean_text(text):
    """
    Remove HTML tags and web links from text.

    Example:
        Input  : "<p>Hello &amp; welcome</p> Visit https://x.com"
        Output : "Hello & welcome Visit"
    """
    text = re.sub(r"<[^>]+>", " ", str(text))     # remove HTML tags
    text = html.unescape(text)                    # &amp; -> &
    text = re.sub(r"https?://\S+", "", text)      # remove URLs
    return re.sub(r"\s+", " ", text).strip()      # normalize whitespace


def score_to_label(score):
    """
    Convert a VADER compound score into a sentiment label.

    Thresholds:
        score >=  0.05  -> "Positive"
        score <= -0.05  -> "Negative"
        otherwise       -> "Neutral"
    """
    if score >= 0.05:  return "Positive"
    if score <= -0.05: return "Negative"
    return "Neutral"


def get_keywords(text):
    """Extract meaningful words only (3+ letters, not stopwords)."""
    words = re.findall(r"[a-z]{3,}", text.lower())
    return [w for w in words if w not in STOP_WORDS]


# ==============================================================================
# 5. Data Collection
# ------------------------------------------------------------------------------
# The system collects live online information from the following sources:
#
#     Social source (1 RSS endpoint, 6 hashtags)
#         - Mastodon (#news, #technology, #science, #music, #art, #sports)
#
#     Tech source (1 public API)
#         - Hacker News
#
#     News sources (8 RSS feeds)
#         - BBC News
#         - The Guardian
#         - Al Jazeera
#         - NPR
#         - The New York Times (World)
#         - Times of India
#         - The Hindu
#         - NDTV
#
# Each collector returns a list of dictionaries with the same schema:
#     {"source": ..., "category": ..., "title": ..., "text": ...}
# ==============================================================================

def collect_mastodon():
    """Download social media posts from Mastodon (free RSS)."""
    tags = ["news", "technology", "science", "music", "art", "sports"]
    rows = []
    for tag in tags:
        try:
            feed = feedparser.parse(
                f"https://mastodon.social/tags/{tag}.rss",
                agent="Mozilla/5.0")
            for e in feed.entries[:15]:
                rows.append({
                    "source":   f"Mastodon #{tag}",
                    "category": "Social",
                    "title":    clean_text(e.get("title", "")),
                    "text":     clean_text(e.get("summary", "")),
                })
        except Exception:
            pass
    print(f"   Mastodon          : {len(rows):3d} posts")
    return rows


def collect_hackernews():
    """Download top tech stories from Hacker News (free public API)."""
    rows = []
    try:
        ids = requests.get(
            "https://hacker-news.firebaseio.com/v0/topstories.json",
            timeout=15).json()[:50]

        for sid in ids:
            try:
                item = requests.get(
                    f"https://hacker-news.firebaseio.com/v0/item/{sid}.json",
                    timeout=10).json()
                if item and item.get("title"):
                    rows.append({
                        "source":   "Hacker News",
                        "category": "Tech",
                        "title":    clean_text(item["title"]),
                        "text":     clean_text(item.get("text", "") or item["title"]),
                    })
            except Exception:
                pass
        print(f"   Hacker News       : {len(rows):3d} stories")
    except Exception:
        print(f"   Hacker News failed")
    return rows


def collect_news():
    """Download news from 8 RSS feeds (free, no login required)."""
    feeds = {
        "BBC News":       "http://feeds.bbci.co.uk/news/world/rss.xml",
        "The Guardian":   "https://www.theguardian.com/world/rss",
        "Al Jazeera":     "https://www.aljazeera.com/xml/rss/all.xml",
        "NPR":            "https://feeds.npr.org/1004/rss.xml",
        "NYT World":      "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
        "Times of India": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
        "The Hindu":      "https://www.thehindu.com/news/national/feeder/default.rss",
        "NDTV":           "https://feeds.feedburner.com/ndtvnews-top-stories",
    }
    rows = []
    for name, url in feeds.items():
        try:
            feed = feedparser.parse(url, agent="Mozilla/5.0")
            for e in feed.entries[:MAX_ITEMS]:
                rows.append({
                    "source":   name,
                    "category": "News",
                    "title":    clean_text(e.get("title", "")),
                    "text":     clean_text(e.get("summary", "") or e.get("title", "")),
                })
            print(f"   {name:18s}: {len(feed.entries[:MAX_ITEMS]):3d} articles")
        except Exception:
            print(f"   {name} failed")
    return rows


# ==============================================================================
# 6. Running the Data Collectors
# ------------------------------------------------------------------------------
# Executing all collectors to build the working dataset.
# ==============================================================================

print("=" * 70)
print(f"STEP 1: Collecting live data  |  {datetime.now():%d %b %Y, %H:%M}")
print("=" * 70)

print("\nSocial sources:")
all_rows = collect_mastodon()

print("\nTech sources:")
all_rows += collect_hackernews()

print("\nNews sources:")
all_rows += collect_news()

# Combine all collected records into a Pandas DataFrame
df = pd.DataFrame(all_rows, columns=["source", "category", "title", "text"])
print(f"\nCollected {len(df)} items from {df['source'].nunique()} sources")


# ==============================================================================
# 7. Data Cleaning and Duplicate Removal
# ------------------------------------------------------------------------------
# Real-world data contains blanks, duplicates, and short junk rows.
# These are removed so that subsequent analysis remains accurate.
#
# Operations performed:
#     - Drop rows whose text length is less than 10 characters
#     - Drop rows with empty titles
#     - Drop duplicate items by title
#     - Re-index the DataFrame
# ==============================================================================

print("\n" + "=" * 70)
print("STEP 2: Cleaning data")
print("=" * 70)

before = len(df)
df = df[df["text"].str.len() > 10]
df = df[df["title"].str.len() > 0]
df = df.drop_duplicates(subset=["title"])
df = df.reset_index(drop=True)

print(f"Before cleaning : {before} rows")
print(f"After cleaning  : {len(df)} rows")
print(f"Removed         : {before - len(df)} rows")


# ==============================================================================
# 8. Word Counting and Keyword Analysis
# ------------------------------------------------------------------------------
# Word count per item and frequency of meaningful keywords are computed.
# ==============================================================================

print("\n" + "=" * 70)
print("STEP 3: Counting words")
print("=" * 70)

df["word_count"] = df["text"].str.split().str.len()

word_counter = Counter()
for text in df["text"]:
    word_counter.update(get_keywords(text))

top_words = pd.Series(dict(word_counter.most_common(TOP_N_WORDS)), dtype=float)

print(f"Total words : {df['word_count'].sum():,}")
print(f"Top 5 words : {list(top_words.index[:5])}")


# ==============================================================================
# 9. Sentiment Analysis
# ------------------------------------------------------------------------------
# VADER assigns each item a compound score between -1 (very negative) and
# +1 (very positive). Thresholds used to classify items:
#
#     score >=  0.05  -> Positive
#     score <= -0.05  -> Negative
#     between -0.05 and 0.05 -> Neutral
# ==============================================================================

print("\n" + "=" * 70)
print("STEP 4: Analysing sentiment")
print("=" * 70)

df["sentiment_score"] = df["text"].apply(
    lambda t: analyzer.polarity_scores(t)["compound"])

df["sentiment_label"] = df["sentiment_score"].apply(score_to_label)

pos = (df["sentiment_label"] == "Positive").sum()
neu = (df["sentiment_label"] == "Neutral").sum()
neg = (df["sentiment_label"] == "Negative").sum()

print(f"Positive: {pos:4d} ({pos/len(df)*100:.1f}%)")
print(f"Neutral : {neu:4d} ({neu/len(df)*100:.1f}%)")
print(f"Negative: {neg:4d} ({neg/len(df)*100:.1f}%)")


# ==============================================================================
# 10. Source-wise Comparison and Statistical Analysis
# ------------------------------------------------------------------------------
# Sentiment scores are grouped by source to compute average sentiment values.
# Cross-tabulation is used to calculate percentage distribution of sentiment
# categories per source.
# ==============================================================================

print("\n" + "=" * 70)
print("STEP 5: Comparing sources")
print("=" * 70)

summary = df.groupby("source").agg(
    items=("text", "count"),
    total_words=("word_count", "sum"),
    avg_words=("word_count", "mean"),
    avg_mood=("sentiment_score", "mean"),
).sort_values("items", ascending=False)

mood_pct = (pd.crosstab(df["source"], df["sentiment_label"], normalize="index")
            .reindex(columns=MOODS, fill_value=0) * 100)

print(summary.round(2).to_string())


# ==============================================================================
# 11. Data Visualization
# ------------------------------------------------------------------------------
# A six-panel dashboard is created:
#
#     1. Items per Source
#     2. Total Words per Source
#     3. Average Words per Item
#     4. Sentiment Mix (100% per Source)
#     5. Average Sentiment Score
#     6. Top Keywords
# ==============================================================================

print("\n" + "=" * 70)
print("STEP 6: Drawing dashboard")
print("=" * 70)

fig, ax = plt.subplots(3, 2, figsize=(18, 17), layout="constrained")
fig.suptitle(f"Live Social Media Data Dashboard  |  {datetime.now():%d %b %Y}",
             fontsize=20, fontweight="bold")


def tilt(a):
    """Rotate x-axis labels so long source names do not overlap."""
    plt.setp(a.get_xticklabels(), rotation=30, ha="right", fontsize=8)


# Chart 1: Items per Source
bars = ax[0, 0].bar(summary.index, summary["items"], color="#3498DB")
ax[0, 0].bar_label(bars, fontweight="bold", fontsize=8)
ax[0, 0].set_title("1. Items per Source", loc="left", fontsize=13, fontweight="bold")
ax[0, 0].set_ylabel("Count"); tilt(ax[0, 0])

# Chart 2: Total Words per Source
bars = ax[0, 1].bar(summary.index, summary["total_words"], color="#9B59B6")
ax[0, 1].bar_label(bars, fontweight="bold", fontsize=8)
ax[0, 1].set_title("2. Total Words", loc="left", fontsize=13, fontweight="bold")
ax[0, 1].set_ylabel("Words"); tilt(ax[0, 1])

# Chart 3: Average Words per Item
bars = ax[1, 0].bar(summary.index, summary["avg_words"], color="#F39C12")
ax[1, 0].bar_label(bars, fmt="%.1f", fontweight="bold", fontsize=8)
ax[1, 0].set_title("3. Average Words per Item", loc="left", fontsize=13, fontweight="bold")
ax[1, 0].set_ylabel("Words"); tilt(ax[1, 0])

# Chart 4: Sentiment Mix (100% stacked)
mood_pct.plot(kind="barh", stacked=True, ax=ax[1, 1],
              color=[COLORS[c] for c in mood_pct.columns])
ax[1, 1].set_xlim(0, 100)
ax[1, 1].set_title("4. Sentiment Mix (100% per source)", loc="left",
                   fontsize=13, fontweight="bold")
ax[1, 1].set_xlabel("%")
ax[1, 1].legend(title="", loc="lower right", fontsize=8)

# Chart 5: Average Sentiment Score
colors = [COLORS["Positive"] if v >= 0 else COLORS["Negative"]
          for v in summary["avg_mood"]]
bars = ax[2, 0].bar(summary.index, summary["avg_mood"], color=colors)
ax[2, 0].bar_label(bars, fmt="%.3f", fontweight="bold", fontsize=8)
ax[2, 0].axhline(0, color="black", linestyle="--", linewidth=1)
ax[2, 0].set_title("5. Average Sentiment Score", loc="left", fontsize=13, fontweight="bold")
ax[2, 0].set_ylabel("Score (-1 to +1)"); tilt(ax[2, 0])

# Chart 6: Top Keywords
sw = top_words.sort_values()
bars = ax[2, 1].barh(sw.index, sw.values, color="#16A085")
ax[2, 1].bar_label(bars, fontweight="bold", fontsize=8)
ax[2, 1].set_title(f"6. Top {TOP_N_WORDS} Words", loc="left", fontsize=13, fontweight="bold")
ax[2, 1].set_xlabel("Times used")

plt.savefig("capstone_dashboard.png", dpi=150, bbox_inches="tight")
plt.show()
print("Saved: capstone_dashboard.png")


# ==============================================================================
# 12. Saving Results
# ------------------------------------------------------------------------------
# The full dataset and the source-level summary are saved as CSV files.
# ==============================================================================

df.to_csv("capstone_data.csv", index=False)
summary.to_csv("capstone_summary.csv")
print("Saved: capstone_data.csv")
print("Saved: capstone_summary.csv")


# ==============================================================================
# 13. Final Report
# ------------------------------------------------------------------------------
# A concise text-based summary is printed for the project submission.
# ==============================================================================

print("\n" + "=" * 70)
print("FINAL REPORT")
print("=" * 70)
print(f"Total items analysed    : {len(df):,}")
print(f"Total words analysed    : {df['word_count'].sum():,}")
print(f"Sources used            : {df['source'].nunique()}")
print(f"Most items from         : {summary['items'].idxmax()} "
      f"({summary['items'].max()})")
print(f"Most positive source    : {summary['avg_mood'].idxmax()} "
      f"({summary['avg_mood'].max():+.3f})")
print(f"Most negative source    : {summary['avg_mood'].idxmin()} "
      f"({summary['avg_mood'].min():+.3f})")

print("\nTop 3 most positive posts:")
for _, r in df.nlargest(3, "sentiment_score").iterrows():
    print(f"  [{r['sentiment_score']:+.2f}] {r['source']}: {r['title'][:60]}")

print("\nTop 3 most negative posts:")
for _, r in df.nsmallest(3, "sentiment_score").iterrows():
    print(f"  [{r['sentiment_score']:+.2f}] {r['source']}: {r['title'][:60]}")

print("\n" + "=" * 70)
print("PROJECT COMPLETE")
print("=" * 70)


# ==============================================================================
# 14. Project Outcome
# ------------------------------------------------------------------------------
# The project demonstrates a complete data-analysis workflow:
#
#     Data Collection -> Data Cleaning -> Data Transformation ->
#     Sentiment Analysis -> Keyword Analysis -> Statistical Analysis ->
#     Visualization -> Findings -> Conclusion
#
# Output files:
#     - capstone_dashboard.png   : 6-chart visual dashboard
#     - capstone_data.csv        : full dataset with sentiment scores
#     - capstone_summary.csv     : source-level aggregate statistics
# ==============================================================================
