# ==============================================================================
# LIVE GLOBAL social media DASHBOARD  (improved version)
# Run in Google Colab / Jupyter. Reads live RSS feeds, scores each article's
# sentiment, and shows a 6-panel dashboard + top headlines.
# ==============================================================================
!pip install -q feedparser vaderSentiment seaborn matplotlib pandas nltk

import html
import re
import textwrap
from collections import Counter
from datetime import datetime

import feedparser
import matplotlib.pyplot as plt
import nltk
import pandas as pd
import seaborn as sns
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

nltk.download("stopwords", quiet=True)
from nltk.corpus import stopwords

# ------------------------------------------------------------------------------
# SETTINGS  (change things here, not deep in the code)
# ------------------------------------------------------------------------------
RSS_SOURCES = {
    "The New York Times": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "BBC News": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "The Guardian": "https://www.theguardian.com/world/rss",
}

SENTIMENT_ORDER = ["Negative", "Neutral", "Positive"]        # same order everywhere
SENTIMENT_COLORS = {"Negative": "#E74C3C", "Neutral": "#B0B7BD", "Positive": "#2ECC71"}
POS_THRESHOLD, NEG_THRESHOLD = 0.05, -0.05                   # VADER's standard cut-offs
TOP_N_WORDS = 12
SAVE_PNG = True

# Words that appear in almost every news feed and say nothing useful
EXTRA_STOPWORDS = {"said", "says", "say", "new", "us", "also", "one", "two", "would",
                   "could", "year", "years", "after", "continue", "reading", "amp"}
STOP_WORDS = set(stopwords.words("english")) | EXTRA_STOPWORDS


# ------------------------------------------------------------------------------
# 1. FETCH DATA
# ------------------------------------------------------------------------------
def strip_html(text: str) -> str:
    """Remove HTML tags/entities and 'Continue reading...' leftovers."""
    text = re.sub(r"<[^>]+>", " ", str(text))
    text = html.unescape(text)
    text = re.sub(r"Continue reading\.*", "", text, flags=re.I)
    return re.sub(r"\s+", " ", text).strip()


def fetch_articles(sources: dict) -> pd.DataFrame:
    rows = []
    for name, url in sources.items():
        try:
            feed = feedparser.parse(url)
            if not feed.entries:
                print(f"⚠️  No articles returned for {name}")
                continue
            # LIMIT APPLIED HERE: Only take the first 10 entries per source
            for e in feed.entries[:10]:
                rows.append({
                    "newspaper": name,
                    "title": strip_html(e.get("title", "")),
                    "summary": strip_html(e.get("summary", e.get("description", ""))),
                })
        except Exception as err:                     # one bad feed shouldn't stop the rest
            print(f"⚠️  Could not read {name}: {err}")
    df = pd.DataFrame(rows)
    if df.empty:
        raise SystemExit("No articles fetched - check your internet connection.")
    return df.drop_duplicates(subset=["newspaper", "title"]).reset_index(drop=True)


now = datetime.now()
print(f"⏳ Fetching LIVE news at {now:%Y-%m-%d %H:%M:%S}...\n")
df = fetch_articles(RSS_SOURCES)
df["raw_text"] = df["title"] + ". " + df["summary"]


# ------------------------------------------------------------------------------
# 2. SENTIMENT
# Note: VADER is scored on the ORIGINAL text. The old code scored the "cleaned"
# text, which removed words like "not"/"no" and punctuation that VADER uses to
# understand meaning ("not good" would have looked positive!).
# ------------------------------------------------------------------------------
analyzer = SentimentIntensityAnalyzer()


def to_label(score: float) -> str:
    if score >= POS_THRESHOLD:
        return "Positive"
    if score <= NEG_THRESHOLD:
        return "Negative"
    return "Neutral"


df["sentiment_score"] = df["raw_text"].apply(lambda t: analyzer.polarity_scores(t)["compound"])
df["sentiment_label"] = pd.Categorical(
    df["sentiment_score"].apply(to_label), categories=SENTIMENT_ORDER, ordered=True
)


# ------------------------------------------------------------------------------
# 3. KEYWORDS  (cleaning is only needed here, for word counting)
# ------------------------------------------------------------------------------
def tokenize(text: str) -> list:
    text = re.sub(r"http\S+|www\S+", "", text.lower())
    words = re.findall(r"[a-z]{3,}", text)           # letters only, 3+ chars
    return [w for w in words if w not in STOP_WORDS]


word_counts = Counter(w for t in df["raw_text"] for w in tokenize(t))
top_words = pd.Series(dict(word_counts.most_common(TOP_N_WORDS)))


# ------------------------------------------------------------------------------
# 4. DASHBOARD
# ------------------------------------------------------------------------------
sns.set_theme(style="whitegrid", font_scale=1.05)
fig = plt.figure(figsize=(19, 17), layout="constrained")
gs = fig.add_gridspec(3, 2)
ax_vol, ax_donut = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1])
ax_stack, ax_avg = fig.add_subplot(gs[1, 0]), fig.add_subplot(gs[1, 1])
ax_box, ax_words = fig.add_subplot(gs[2, 0]), fig.add_subplot(gs[2, 1])

fig.suptitle(f"Live Global News Dashboard  |  {now:%d %b %Y, %H:%M}",
             fontsize=22, fontweight="bold")


def style(ax, title, subtitle):
    """Bold title + a small plain-English line explaining how to read the chart."""
    ax.set_title(f"{title}\n", fontsize=15, fontweight="bold", loc="left")
    ax.text(0, 1.02, subtitle, transform=ax.transAxes, fontsize=10.5,
            color="#555", style="italic", va="bottom")


papers = df["newspaper"].unique().tolist()
paper_palette = dict(zip(papers, sns.color_palette("crest", len(papers))))

# --- 1. Volume ----------------------------------------------------------------
counts = df["newspaper"].value_counts()
sns.barplot(x=counts.index, y=counts.values, hue=counts.index,
            palette=paper_palette, legend=False, ax=ax_vol)
ax_vol.bar_label(ax_vol.containers[0], fontsize=12, fontweight="bold", padding=3)
style(ax_vol, "1. Articles Collected", "How many articles each newspaper contributed")
ax_vol.set(xlabel="", ylabel="Number of articles")

# --- 2. Donut -----------------------------------------------------------------
sent_counts = df["sentiment_label"].value_counts().reindex(SENTIMENT_ORDER).fillna(0)
ax_donut.pie(
    sent_counts.values,
    labels=[f"{l}\n({int(n)})" for l, n in sent_counts.items()],
    colors=[SENTIMENT_COLORS[l] for l in sent_counts.index],
    autopct=lambda p: f"{p:.0f}%" if p > 0 else "",
    startangle=90, counterclock=False, pctdistance=0.78,
    textprops=dict(fontsize=12),
    wedgeprops=dict(width=0.42, edgecolor="white", linewidth=2.5),
)
for t in ax_donut.texts:                                # make the % labels white + bold
    if t.get_text().endswith("%"):
        t.set(color="white", fontweight="bold", fontsize=12)
ax_donut.text(0, 0, f"{len(df)}\narticles", ha="center", va="center",
              fontsize=18, fontweight="bold")
style(ax_donut, "2. Overall Sentiment Mix", "Share of all articles that are negative / neutral / positive")

# --- 3. 100% stacked bar per newspaper ---------------------------------------------
pct = (pd.crosstab(df["newspaper"], df["sentiment_label"], normalize="index")
       .reindex(columns=SENTIMENT_ORDER, fill_value=0) * 100)
pct.plot(kind="barh", stacked=True, ax=ax_stack, width=0.65,
         color=[SENTIMENT_COLORS[c] for c in pct.columns], edgecolor="white")
for cont in ax_stack.containers:                        # % label inside each segment
    ax_stack.bar_label(cont, labels=[f"{v:.0f}%" if v >= 6 else "" for v in cont.datavalues],
                       label_type="center", color="white", fontweight="bold")
ax_stack.set_xlim(0, 100)
ax_stack.legend(title="", ncol=3, loc="lower center", bbox_to_anchor=(0.5, -0.22), frameon=False)
style(ax_stack, "3. Sentiment Mix by Newspaper",
      "Each bar = 100% of that paper's articles (fair even if paper sizes differ)")
ax_stack.set(xlabel="% of articles", ylabel="")

# --- 4. Average score ----------------------------------------------------------
avg = df.groupby("newspaper")["sentiment_score"].mean().sort_values(ascending=False)
bar_colors = [SENTIMENT_COLORS["Positive"] if v > 0 else SENTIMENT_COLORS["Negative"] for v in avg.values]
ax_avg.bar(avg.index, avg.values, color=bar_colors, width=0.55)
ax_avg.bar_label(ax_avg.containers[0], fmt="%.3f", fontsize=12, fontweight="bold", padding=3)
ax_avg.axhline(0, color="black", linewidth=1.2, linestyle="--")
lim = max(0.1, avg.abs().max() * 1.4)
ax_avg.set_ylim(-lim, lim)
style(ax_avg, "4. Average Sentiment Score (High → Low)",
      "Above 0 = more positive tone, below 0 = more negative tone")
ax_avg.set(xlabel="", ylabel="Average score (-1 to +1)")

# --- 5. Score distribution -----------------------------------------------------
ax_box.axhspan(POS_THRESHOLD, 1, color=SENTIMENT_COLORS["Positive"], alpha=0.08)
ax_box.axhspan(-1, NEG_THRESHOLD, color=SENTIMENT_COLORS["Negative"], alpha=0.08)
sns.boxplot(data=df, x="newspaper", y="sentiment_score", hue="newspaper",
            palette=paper_palette, legend=False, width=0.5, fliersize=0, ax=ax_box)
sns.stripplot(data=df, x="newspaper", y="sentiment_score", color="#222", alpha=0.45,
              size=3.5, jitter=0.2, ax=ax_box)
ax_box.axhline(0, color="black", linewidth=1, linestyle="--")
ax_box.set_ylim(-1, 1)
style(ax_box, "5. Spread of Scores (every dot = 1 article)",
      "Box = middle 50% of articles, line = median. Green zone positive, red zone negative")
ax_box.set(xlabel="", ylabel="Sentiment score")

# --- 6. Top keywords -----------------------------------------------------------
top_sorted = top_words.sort_values()
ax_words.barh(top_sorted.index, top_sorted.values,
              color=sns.color_palette("flare", len(top_sorted)))
ax_words.bar_label(ax_words.containers[0], padding=3, fontweight="bold")
style(ax_words, f"6. Top {TOP_N_WORDS} Keywords", "Most frequent meaningful words in today's headlines & summaries")
ax_words.set(xlabel="Mentions", ylabel="")

if SAVE_PNG:
    fig.savefig("news_dashboard.png", dpi=150, bbox_inches="tight")
plt.show()


# ------------------------------------------------------------------------------
# 5. TEXT SUMMARY
# ------------------------------------------------------------------------------
def show_headlines(title, frame):
    print(f"\n{title}")
    for _, r in frame.iterrows():
        line = f"[{r.sentiment_score:+.2f}] {r.newspaper}: {r.title}"
        print(textwrap.fill(line, 100, initial_indent="  • ", subsequent_indent="      "))


print("\n" + "=" * 60)
print("📈 LIVE DATA SUMMARY")
print("=" * 60)
print(f"Total articles analyzed : {len(df)} from {df['newspaper'].nunique()} newspapers")
print(f"Most positive newspaper : {avg.index[0]} ({avg.iloc[0]:+.3f})")
print(f"Most negative newspaper : {avg.index[-1]} ({avg.iloc[-1]:+.3f})")
print(f"Overall average score   : {df['sentiment_score'].mean():+.3f}")
show_headlines("🟢 Most positive headlines:", df.nlargest(3, "sentiment_score"))
show_headlines("🔴 Most negative headlines:", df.nsmallest(3, "sentiment_score"))
print("=" * 60)
