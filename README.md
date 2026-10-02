
# LIVE SOCIAL MEDIA DATA ANALYSIS

**Team Details**

* **Time Table:** 2
* **Team:** 14
* **Team Leader:** S. Penchala Chaitanya (Roll Number: 25B11CS902)

**Team Members:**

1. S. Penchala Chaitanya (25B11CS902)
2. Konappagari Pandu (25B11CS457)
3. S. Radha Sai Lakshmi (25B11CS854)
4. M. Divya (25B11CS520)

---

## 1. Project Overview

This project focuses on analyzing live social media, tech forums, and news-related online information using data analysis and visualization techniques. The system collects current posts and articles through RSS feeds and public APIs, preprocesses the collected text, performs sentiment analysis and keyword analysis, and presents the results through a six-panel analytical dashboard.

The project demonstrates how continuously changing online information can be collected and transformed into meaningful insights using Python, Pandas, VADER Sentiment Analysis, Matplotlib, Requests, and Feedparser.

---

## 2. Problem Statement

A large amount of information is generated continuously through online news and social media platforms. Manually examining this information is time-consuming and makes it difficult to identify overall sentiment, major topics, and differences between various digital information sources.

This project addresses this problem by automatically collecting live data from social networks (Mastodon), tech forums (Hacker News), and global news outlets (RSS feeds). It applies data cleaning, sentiment analysis, keyword analysis, and statistical visualization to produce automated, meaningful insights.

---

## 3. Objectives

The main objectives of this project are:

* To collect live online data from multiple diverse sources using APIs and RSS feeds.
* To preprocess and clean the collected data (removing HTML, URLs, and junk characters).
* To remove duplicate content.
* To perform natural language sentiment analysis on the content.
* To classify text as Positive, Neutral, or Negative using VADER thresholds.
* To identify frequently occurring meaningful keywords across all platforms.
* To compare sentiment and volume (word counts) across different sources.
* To perform statistical analysis using Pandas.
* To visualize the results using a 6-panel Matplotlib dashboard.
* To generate exportable CSV reports containing the findings.

---

## 4. Scope of the Project

The project focuses on the real-time text analysis of live online information collected from 10 distinct sources across three categories:

**Social Source (Mastodon RSS):**

* Mastodon (Tags: #news, #technology, #science, #music, #art, #sports)

**Tech Source (Public JSON API):**

* Hacker News (Top Stories)

**News Sources (RSS Feeds):**

1. BBC News
2. The Guardian
3. Al Jazeera
4. NPR
5. NYT World
6. Times of India
7. The Hindu
8. NDTV

The system collects up to **40 articles** per news feed, **15 posts** per Mastodon tag, and **50 top stories** from Hacker News during each execution.

---

## 5. Significance of the Project

The project demonstrates the practical use of data analysis techniques on a diverse range of continuously changing digital sources. Instead of looking at just one newspaper, it provides a simple way to understand and contrast the tone of traditional news media versus social networks and tech communities.

It provides a foundation for larger real-time digital analytics systems used in brand monitoring, public relations, and trend forecasting.

---

## 6. Dataset

**Dataset Source:**
The data is collected dynamically on execution from public RSS feeds and the Hacker News Firebase JSON API.

**Dataset Description:**
Each collected item provides information that is processed and stored in a Pandas DataFrame. The primary attributes in the generated dataset are:

| Attribute | Description |
| --- | --- |
| `source` | Name of the platform or news outlet |
| `category` | Classification (Social, Tech, News) |
| `title` | Article headline or post title |
| `text` | Cleaned post text or article summary |
| `word_count` | Total number of words in the text |
| `sentiment_score` | VADER compound score (-1.0 to +1.0) |
| `sentiment_label` | Positive, Neutral, or Negative classification |

**Number of Records:**
The maximum number of collected records before duplicate removal is over 450 items per execution. After cleaning and duplicate removal, the final dataset typically contains a robust, highly relevant set of current digital data.

---

## 7. Technologies Used

The project uses the following technologies and Python libraries:

* **Python:** Core programming language
* **Pandas:** Data manipulation, aggregation, and statistical analysis
* **Feedparser:** Parsing XML RSS feeds
* **Requests:** Handling HTTP requests for JSON APIs
* **VADER Sentiment:** Rule-based sentiment analysis
* **Matplotlib:** Data visualization and dashboard generation
* **Regular Expressions (`re`):** Text cleaning

---

## 8. Project Workflow

**Live Data Collection (APIs & RSS)**
↓
**Data Cleaning (HTML & URL Removal)**
↓
**Duplicate & Junk Removal**
↓
**Word Counting & Keyword Extraction**
↓
**Sentiment Analysis (VADER)**
↓
**Source-wise Statistical Grouping**
↓
**Dashboard Visualization**
↓
**Export Findings to CSV**

---

## 9. Data Loading and Inspection

The program uses `feedparser` for RSS feeds and the `requests` library for Hacker News. The collected records are appended to a list of dictionaries and converted into a Pandas DataFrame. The console logs the exact number of successful items retrieved from each of the 10 sources in real time.

---

## 10. Missing-Value and Error Handling

The extraction uses safe access and `try-except` blocks. If an API times out or a feed is down, the program prints a failure message for that specific source and continues executing the rest of the pipeline safely. Text fields that are empty fall back to using the title text to ensure no empty data breaks the sentiment analyzer.

---

## 11. Duplicate Removal

Duplicate articles are removed using the combination of source and article title to prevent the same trending story from being counted multiple times. Furthermore, rows containing less than 10 characters of text are dropped to ensure high data quality. The duplicate removal is performed using Pandas `drop_duplicates(subset=["title"])`.

---

## 12. Data Cleaning and Filtering

The project utilizes a custom `clean_text()` function. The cleaning process:

* Removes HTML tags using regular expressions (`<[^>]+>`).
* Converts HTML entities (e.g., `&amp;` -> `&`).
* Removes web URLs (http/https).
* Normalizes whitespace to a single space.
* During keyword analysis, it extracts only alphabetic words (3+ characters), converts them to lowercase, and filters out an extensive list of custom `STOP_WORDS` (including "said", "new", "https", etc.).

---

## 13. Sentiment Analysis

The project uses **VADER (Valence Aware Dictionary and sEntiment Reasoner)**. VADER generates a compound sentiment score between -1 and +1.

The project uses the following thresholds:

* **Score >= 0.05:** Positive
* **Score <= -0.05:** Negative
* **Between -0.05 and 0.05:** Neutral

Sentiment analysis is performed on the fully cleaned text, maintaining punctuation that VADER relies on for contextual understanding (like exclamation marks).

---

## 14. Keyword Analysis

Keyword analysis is used to identify the most frequently occurring meaningful words across all platforms. The script uses Python's `Counter` module to tally all valid words after stopwords are removed. The system captures and plots the Top 12 trending keywords.

---

## 15. Pandas Operations and Data Manipulation

Pandas is used extensively. Important operations include:

* `df.drop_duplicates()`: Removing repeated news cycles.
* `df.groupby("source")`: Aggregating stats per platform.
* `pd.crosstab()`: Calculating the exact percentage makeup of Positive/Neutral/Negative items per source.
* `df.nlargest()` / `df.nsmallest()`: Fetching the most extreme sentiment headlines for the final console report.

---

## 16. Statistical Analysis

The project performs several source-level statistical analyses:

* Total items collected per source.
* Total volume of words analyzed per source.
* Average words per post/article (identifying short-form vs. long-form platforms).
* Average sentiment score (mood) by source.
* Percentage distribution of sentiment labels.

---

## 17. Data Visualizations

The project uses Matplotlib to generate a high-resolution, six-panel dashboard:

1. **Items per Source (Bar Chart):** Shows data volume contributed by each source.
2. **Total Words (Bar Chart):** Shows total text volume processed per source.
3. **Average Words per Item (Bar Chart):** Compares the text density of social posts versus news articles.
4. **Sentiment Mix (100% Stacked Bar Chart):** Compares the percentage makeup of Positive (Green), Neutral (Gray), and Negative (Red) items for each source.
5. **Average Sentiment Score (Bar Chart):** Plots the overall mood of each platform. Positive averages plot upwards in green, negative averages plot downwards in red.
6. **Top 12 Words (Horizontal Bar Chart):** Displays the most frequently mentioned keywords across the entire live dataset.

---

## 18. Interpretation of Visualizations

* The **Items and Words** charts show which platforms dominate the data pool.
* The **Average Words** chart highlights the structural difference between social media (short text) and traditional news (long text).
* The **Stacked Sentiment** and **Average Sentiment** charts reveal platform bias—showing if certain news outlets or social tags skew heavily negative or positive at the current moment.
* The **Keyword** chart acts as a snapshot of what the world is talking about right now.

---

## 19. Findings and Results

Because the data is live, findings change on every execution. However, the system permanently logs the findings by exporting three files:

1. **`capstone_dashboard.png`**: The 6-chart visual dashboard.
2. **`capstone_data.csv`**: The complete, cleaned dataset containing all text and sentiment scores.
3. **`capstone_summary.csv`**: The aggregated source-level statistics.

The console also prints a live summary identifying the most positive and negative platforms overall, and highlights the 3 most positive and negative specific headlines.

---

## 20. Conclusion

This project successfully demonstrates a complete, automated ETL (Extract, Transform, Load) data-analysis workflow using Python.

By scaling beyond a few basic RSS feeds to include API-based tech forums and tag-based social media networks, the project provides a much richer and more accurate representation of current digital sentiment. The automated dashboard instantly converts chaotic online text into digestible, structured business intelligence.

---

## 21. Limitations

* The dataset is highly time-sensitive; results rely entirely on the exact moment the script is executed.
* Hacker News restricts API limits to the top 50 stories.
* VADER may not correctly understand deep sarcasm, irony, or highly domain-specific technical jargon on Hacker News.
* Keyword frequency alone does not perfectly measure the true contextual importance of a trending topic.

---

## 22. How to Run the Project

**Step 1: Install Dependencies**
Install the required Python libraries using pip:

```bash
pip install pandas matplotlib feedparser requests vaderSentiment

```

**Step 2: Run the Python Program**
Execute the script from your terminal:

```bash
python capstone_project.py

```

**Step 3: View the Results**
After execution, the program will print the real-time extraction logs and text summary to the terminal. The visualization dashboard will display on screen, and the following files will be saved in your directory:

* `capstone_dashboard.png`
* `capstone_data.csv`
* `capstone_summary.csv`
