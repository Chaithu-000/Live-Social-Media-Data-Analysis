# LIVE SOCIAL MEDIA DATA ANALYSIS

## 1. Project Overview

This project focuses on analyzing live social-media-related online information using data analysis and visualization techniques. The system collects current news articles through RSS feeds, preprocesses the collected text, performs sentiment analysis and keyword analysis, and presents the results through a six-panel analytical dashboard.

The project demonstrates how continuously changing online information can be collected and transformed into meaningful insights using Python, Pandas, VADER Sentiment Analysis, Matplotlib, Seaborn, NLTK, and Feedparser.

---

## 2. Problem Statement

A large amount of information is generated continuously through online news and social-media-related platforms. Manually examining this information is time-consuming and makes it difficult to identify overall sentiment, major topics, and differences between information sources.

This project addresses this problem by automatically collecting live RSS-based news data and applying data cleaning, sentiment analysis, keyword analysis, statistical analysis, and visualization to produce meaningful insights.

---

## 3. Objectives

The main objectives of this project are:

* To collect live online news data using RSS feeds.
* To preprocess and clean the collected data.
* To remove duplicate articles.
* To perform sentiment analysis on article content.
* To classify articles as Positive, Neutral, or Negative.
* To identify frequently occurring meaningful keywords.
* To compare sentiment across different news sources.
* To perform statistical analysis using Pandas.
* To visualize the results using different charts.
* To generate meaningful findings from the analyzed data.

---

## 4. Scope of the Project

The project focuses on the analysis of live online news information collected through RSS feeds.

The current implementation uses RSS feeds from:

* The New York Times
* BBC News
* The Guardian

The system collects up to 10 articles from each source during each execution and analyzes the available article titles and summaries.

The scope includes:

* Live data collection
* Text preprocessing
* Duplicate removal
* Sentiment analysis
* Keyword extraction
* Statistical analysis
* Data visualization
* Source-wise comparison
* Headline-level sentiment analysis

---

## 5. Significance of the Project

The project demonstrates the practical use of data analysis techniques on continuously changing online information.

It provides a simple way to understand:

* The amount of information collected from different sources.
* The overall sentiment distribution.
* Differences in sentiment between sources.
* The most frequently occurring keywords.
* The distribution of sentiment scores.
* The most positive and negative headlines.

The project can serve as a foundation for larger real-time information monitoring and analytics systems.

---

# 6. Dataset

## Dataset Source

The data is collected dynamically from RSS feeds provided by online news sources.

The current RSS sources are:

1. The New York Times
2. BBC News
3. The Guardian

The RSS feed URLs are defined in the Python program.

## Dataset Description

Each RSS article provides information that is processed and stored in a Pandas DataFrame.

The primary collected attributes are:

| Attribute   | Description                    |
| ----------- | ------------------------------ |
| `newspaper` | Name of the news source        |
| `title`     | Article headline               |
| `summary`   | Article summary or description |

The project then generates additional analytical attributes:

| Attribute         | Description                        |
| ----------------- | ---------------------------------- |
| `raw_text`        | Combined article title and summary |
| `sentiment_score` | VADER compound sentiment score     |
| `sentiment_label` | Positive, Neutral, or Negative     |

These fields are created during the data collection and analysis pipeline.

## Number of Records

The program collects up to 10 articles from each RSS source.

With three sources, the maximum number of collected records before duplicate removal is approximately 30 articles per execution.

The final number can vary because duplicate articles are removed.

## Important Attributes

The most important attributes for analysis are:

* `newspaper`
* `title`
* `summary`
* `sentiment_score`
* `sentiment_label`

---

# 7. Technologies Used

The project uses the following technologies and Python libraries:

* Python
* Pandas
* Feedparser
* VADER Sentiment
* NLTK
* Matplotlib
* Seaborn
* Regular Expressions
* Jupyter Notebook / Google Colab

---

# 8. Project Workflow

The overall workflow of the project is:

**Live RSS Feeds**

↓

**Data Collection**

↓

**Data Cleaning**

↓

**Duplicate Removal**

↓

**Text Preparation**

↓

**Sentiment Analysis**

↓

**Keyword Analysis**

↓

**Statistical Analysis**

↓

**Data Visualization**

↓

**Findings and Conclusions**

---

# 9. Data Loading and Inspection

The project uses the Feedparser library to read RSS feeds.

The collected records are converted into a Pandas DataFrame for further processing.

The program also checks whether articles were successfully returned from each source. If a source does not return articles, a warning is displayed.

If no articles are collected from any source, the program stops and asks the user to check the internet connection.

---

# 10. Missing-Value Handling

The RSS extraction uses safe field access when reading article information.

For example, the program attempts to obtain the article title and summary while providing an empty value if the corresponding RSS field is unavailable.

The program also handles sources that return no articles by skipping those sources.

If no articles are available from any source, the program stops instead of continuing with an empty dataset.

---

# 11. Duplicate Removal

Duplicate articles are removed using the combination of:

* Newspaper/source
* Article title

This prevents the same article from being counted multiple times during analysis.

The duplicate removal is performed using Pandas `drop_duplicates()`.

---

# 12. Data Cleaning and Filtering

The project performs several text-cleaning operations.

The cleaning process:

* Removes HTML tags.
* Converts HTML entities.
* Removes "Continue reading" text.
* Removes unnecessary whitespace.
* Converts text to lowercase during keyword processing.
* Removes URLs during keyword processing.
* Extracts alphabetic words.
* Keeps words with at least three characters.
* Removes common stopwords.

The project also adds news-specific stopwords such as `said`, `says`, `new`, and other frequently occurring words that do not provide useful information for keyword analysis.

---

# 13. Data Transformation

The article title and summary are combined into a single `raw_text` field.

This combined text is used for sentiment analysis and keyword analysis.

The sentiment score is then transformed into a categorical sentiment label:

* Positive
* Neutral
* Negative

---

# 14. Sentiment Analysis

The project uses **VADER Sentiment Analysis**.

VADER generates a compound sentiment score between -1 and +1.

The project uses the following thresholds:

* Score >= 0.05 → Positive
* Score <= -0.05 → Negative
* Between -0.05 and 0.05 → Neutral

These thresholds are defined in the project settings.

The sentiment analysis is performed on the original article text because words such as "not" and punctuation can affect the meaning and VADER's interpretation.

---

# 15. Keyword Analysis

Keyword analysis is used to identify the most frequently occurring meaningful words in the collected article titles and summaries.

The project removes common stopwords and counts the remaining words.

The system displays the top 12 keywords.

---

# 16. Pandas Operations and Data Manipulation

Pandas is used extensively for data manipulation and analysis.

Important operations include:

* DataFrame creation
* Duplicate removal
* Value counting
* Grouping
* Aggregation
* Sorting
* Crosstab analysis
* Filtering
* Ranking

Examples include:

```python
df.drop_duplicates()
```

```python
df["newspaper"].value_counts()
```

```python
df.groupby("newspaper")["sentiment_score"].mean()
```

```python
df.nlargest(3, "sentiment_score")
```

```python
df.nsmallest(3, "sentiment_score")
```

---

# 17. Grouping, Sorting and Aggregation

The project groups sentiment scores by newspaper to calculate the average sentiment for each source.

The average sentiment values are sorted from high to low to enable source-level comparison.

The project also uses cross-tabulation to calculate the percentage distribution of sentiment categories for each newspaper.

---

# 18. Statistical Analysis

The project performs several statistical analyses, including:

* Number of articles collected from each source.
* Overall average sentiment score.
* Average sentiment score by source.
* Number and percentage of Positive, Neutral, and Negative articles.
* Distribution of sentiment scores.
* Frequency of important keywords.
* Most positive headlines.
* Most negative headlines.

The final summary reports the total number of articles, number of sources, source-level sentiment values, and overall average sentiment.

---

# 19. Data Visualizations

The project creates a six-panel dashboard.

### 1. Articles Collected

A bar chart showing how many articles were collected from each news source.

### 2. Overall Sentiment Mix

A donut chart showing the overall proportion of:

* Negative
* Neutral
* Positive

articles.

### 3. Sentiment Mix by Newspaper

A 100% stacked bar chart comparing the percentage of Positive, Neutral, and Negative articles for each source.

### 4. Average Sentiment Score

A bar chart comparing the average sentiment score of each source.

A score above zero represents a more positive average tone, while a score below zero represents a more negative average tone.

### 5. Spread of Sentiment Scores

A box plot showing the distribution of sentiment scores for each source. Individual dots represent individual articles.

### 6. Top Keywords

A horizontal bar chart showing the top 12 meaningful keywords identified from the collected content.

These six visualizations form the project's main analytical dashboard.

---

# 20. Interpretation of Visualizations

The visualizations help interpret the collected data from different perspectives.

* The article-count chart shows the contribution of each source.
* The donut chart shows the overall sentiment composition.
* The stacked bar chart enables source-wise sentiment comparison.
* The average sentiment chart shows differences in average tone.
* The box plot shows the spread and distribution of sentiment scores.
* The keyword chart identifies the most frequently mentioned meaningful terms.

Together, these visualizations provide a broader understanding of the collected online information.

---

# 21. Findings

The project produces findings based on the live dataset collected during each execution.

The main findings include:

* The number of articles contributed by each source.
* The overall distribution of Positive, Neutral, and Negative articles.
* Differences in sentiment distribution between sources.
* Average sentiment score for each source.
* Frequently occurring keywords.
* The most positive and negative headlines according to the sentiment score.

The exact numerical findings can change each time the live RSS data is collected.

---

# 22. Results

The final result of the project is a live analytical dashboard containing six visualizations along with a text-based summary.

The system also identifies the three most positive and three most negative headlines based on their sentiment scores.

The dashboard is saved as:

`news_dashboard.png`

---

# 23. Conclusion

This project demonstrates how live online information can be collected, processed, analyzed, and visualized using Python.

By combining RSS-based data collection, data preprocessing, sentiment analysis, keyword analysis, statistical analysis, and visualization, the project converts continuously changing online information into meaningful analytical insights.

The dashboard provides a simple way to understand article volume, sentiment distribution, source-wise differences, sentiment-score patterns, and frequently occurring keywords.

---

# 24. Limitations

The current implementation has the following limitations:

* Only three RSS news sources are currently used.
* A maximum of 10 articles per source is collected during each execution.
* The dataset changes depending on the current RSS feed contents.
* The project uses RSS-based online news content rather than directly collecting posts from social-media platforms.
* VADER may not correctly understand every form of sarcasm, context, or complex language.
* Keyword frequency does not necessarily represent the importance of a topic.
* The analysis represents the content available at the time the program is executed.

---

# 25. How to Run the Project

## Step 1: Clone the Repository

Clone the GitHub repository to your local system.

## Step 2: Install Dependencies

Install the required Python libraries:

```bash
pip install -r requirements.txt
```

## Step 3: Run the Python Program

Run:

```bash
python src/social_media_analysis.py
```

Alternatively, open:

```text
notebook/social_media_analysis.ipynb
```

in Jupyter Notebook or Google Colab.

## Step 4: View the Results

After execution, the program displays the dashboard and analytical summary.

The dashboard can be saved as:

```text
news_dashboard.png
```

---

# 26. Project Structure

```text
LIVE-SOCIAL-MEDIA-DATA-ANALYSIS/
│
├── README.md
├── requirements.txt
│
├── data/
│   └── dataset.csv
│
├── src/
│   └── social_media_analysis.py
│
├── notebook/
│   └── social_media_analysis.ipynb
│
├── results/
│   ├── news_dashboard.png
│   └── analysis_results.csv
│
├── ppt/
│   ├── Review-1-Presentation.pptx
│   └── Review-2-Presentation.pptx
│
└── team/
    └── team_details.md
```

---

# 27. Review Presentations

The repository contains both project review presentations:

* Review-1 Presentation
* Review-2 Presentation

They are available in the `ppt/` directory.

---

# 28. Team Information

Team information, including team number, team name, member names, roll numbers, responsibilities, and individual contributions, is provided in:

```text
team/team_details.md
```

---

## Team Members

| Name     | Roll Number | Responsibility |
| -------- | ----------- | -------------- |
| Member 1 | XXXXX       | XXXXX          |
| Member 2 | XXXXX       | XXXXX          |
| Member 3 | XXXXX       | XXXXX          |
| Member 4 | XXXXX       | XXXXX          |

---

## Individual Contributions

### Member 1

* Contribution 1
* Contribution 2

### Member 2

* Contribution 1
* Contribution 2

### Member 3

* Contribution 1
* Contribution 2

### Member 4

* Contribution 1
* Contribution 2

---

# 29. Project Outcome

The project successfully demonstrates a complete data-analysis workflow:

**Data Collection → Data Cleaning → Data Transformation → Sentiment Analysis → Keyword Analysis → Statistical Analysis → Visualization → Findings → Conclusion**

The project provides a practical demonstration of Python-based data analysis on live online information.
