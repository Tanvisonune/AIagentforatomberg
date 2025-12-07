import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
from tqdm import tqdm
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

# ======================
# CONFIG
# ======================

YOUTUBE_API_KEY = "AIzaSyB5RhFi93sGEhcQKHePTWixLfeh6khbfqQ"  # your key
SEARCH_QUERY = "smart fan"
MAX_RESULTS = 30   # Top N videos to analyze

BRANDS = [
    "atomberg",
    "orient",
    "havells",
    "crompton",
    "usha",
    "luminous",
    "bajaj",
]

# ======================
# YOUTUBE SEARCH + FETCH
# ======================

def get_youtube_client():
    return build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def search_youtube(query, max_results=30):
    youtube = get_youtube_client()

    search_response = youtube.search().list(
        q=query,
        part="snippet",
        maxResults=max_results,
        type="video"
    ).execute()

    video_ids = [item["id"]["videoId"] for item in search_response["items"]]

    # Fetch details (stats + snippet) for each video
    videos_response = youtube.videos().list(
        part="snippet,statistics",
        id=",".join(video_ids)
    ).execute()

    videos_data = []

    for item in videos_response["items"]:
        vid = item["id"]
        snippet = item["snippet"]
        stats = item.get("statistics", {})

        videos_data.append({
            "video_id": vid,
            "title": snippet.get("title", ""),
            "description": snippet.get("description", ""),
            "channel_title": snippet.get("channelTitle", ""),
            "view_count": int(stats.get("viewCount", 0)),
            "like_count": int(stats.get("likeCount", 0)) if "likeCount" in stats else 0,
            "comment_count": int(stats.get("commentCount", 0)) if "commentCount" in stats else 0,
        })

    return pd.DataFrame(videos_data)

# ======================
# SENTIMENT ANALYSIS (using NLTK VADER)
# ======================

def get_sentiment_analyzer():
    # VADER is a rule-based sentiment model; no heavy download
    return SentimentIntensityAnalyzer()

def analyze_sentiment(text, analyzer):
    text = text.strip()
    if not text:
        return "NEUTRAL", 0.0

    # VADER gives scores between -1 (negative) and +1 (positive)
    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]

    if compound >= 0.05:
        label = "POSITIVE"
    elif compound <= -0.05:
        label = "NEGATIVE"
    else:
        label = "NEUTRAL"

    return label, abs(compound)

# ======================
# FETCH COMMENTS
# ======================

def fetch_comments(video_id, max_comments=20):
    """
    Fetch top comments for a given video.
    If comments are disabled or quota issues happen, safely return [].
    """
    youtube = get_youtube_client()
    comments = []

    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_comments,
            textFormat="plainText"
        )
        response = request.execute()

        for item in response.get("items", []):
            top_comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(top_comment)
    except HttpError:
        # Comments disabled / quota / other issues -> just skip comments
        return []

    return comments

# ======================
# BRAND & SOV ANALYSIS
# ======================

def analyze_brands_and_sentiment(df):
    analyzer = get_sentiment_analyzer()

    # Columns to store per-video info
    for b in BRANDS:
        df[f"{b}_mentions"] = 0
        df[f"{b}_comment_mentions"] = 0  # extra info: mentions only from comments

    df["overall_sentiment"] = ""
    df["overall_sentiment_score"] = 0.0

    print("\nAnalyzing brand mentions and sentiment (posts + comments)...\n")

    for idx, row in tqdm(df.iterrows(), total=len(df)):
        # Text from title + description
        post_text = f"{row['title']} {row['description']}".lower()

        # Text from comments
        comments = fetch_comments(row["video_id"])
        comments_text = " ".join(comments).lower()

        # Combined text for sentiment
        combined_text = f"{post_text} {comments_text}"

        # Brand mentions: posts + comments
        for b in BRANDS:
            post_count = post_text.count(b)
            comment_count = comments_text.count(b)

            df.at[idx, f"{b}_comment_mentions"] = comment_count
            df.at[idx, f"{b}_mentions"] = post_count + comment_count

        # Overall sentiment based on combined text (what people & video say)
        label, score = analyze_sentiment(combined_text, analyzer)
        df.at[idx, "overall_sentiment"] = label
        df.at[idx, "overall_sentiment_score"] = score

    # Aggregate stats
    brand_summary = []

    for b in BRANDS:
        total_mentions = df[f"{b}_mentions"].sum()

        # Weighted by views (simple engagement weight)
        df[f"{b}_weighted_mentions"] = df[f"{b}_mentions"] * df["view_count"]
        weighted_mentions = df[f"{b}_weighted_mentions"].sum()

        # Sentiment distribution for videos where brand is mentioned
        brand_rows = df[df[f"{b}_mentions"] > 0]
        pos = (brand_rows["overall_sentiment"] == "POSITIVE").sum()
        neg = (brand_rows["overall_sentiment"] == "NEGATIVE").sum()
        neu = (brand_rows["overall_sentiment"] == "NEUTRAL").sum()

        brand_summary.append({
            "brand": b,
            "total_mentions": int(total_mentions),
            "weighted_mentions": int(weighted_mentions),
            "videos_with_mentions": int(len(brand_rows)),
            "positive_videos": int(pos),
            "negative_videos": int(neg),
            "neutral_videos": int(neu),
        })

    summary_df = pd.DataFrame(brand_summary)

    # Compute SoV (by raw mentions)
    total_mentions_all = summary_df["total_mentions"].sum()
    if total_mentions_all > 0:
        summary_df["sov_mentions_percent"] = (
            summary_df["total_mentions"] / total_mentions_all * 100
        )
    else:
        summary_df["sov_mentions_percent"] = 0.0

    # Compute SoV (by weighted mentions)
    total_weighted_all = summary_df["weighted_mentions"].sum()
    if total_weighted_all > 0:
        summary_df["sov_weighted_percent"] = (
            summary_df["weighted_mentions"] / total_weighted_all * 100
        )
    else:
        summary_df["sov_weighted_percent"] = 0.0

    return df, summary_df

# ======================
# GRAPHS
# ======================

def plot_graphs(summary_df):
    # --- BAR CHART 1: SoV by Mentions ---
    plt.figure(figsize=(10, 6))
    plt.bar(summary_df["brand"], summary_df["sov_mentions_percent"])
    plt.title("Share of Voice - Mentions (%)")
    plt.xlabel("Brand")
    plt.ylabel("Percentage (%)")
    plt.tight_layout()
    os.makedirs("output", exist_ok=True)
    plt.savefig("output/sov_mentions_percent.png")
    plt.close()

    # --- BAR CHART 2: SoV by Weighted Mentions ---
    plt.figure(figsize=(10, 6))
    plt.bar(summary_df["brand"], summary_df["sov_weighted_percent"])
    plt.title("Share of Voice - Weighted Mentions (%)")
    plt.xlabel("Brand")
    plt.ylabel("Percentage (%)")
    plt.tight_layout()
    plt.savefig("output/sov_weighted_percent.png")
    plt.close()

# ======================
# MAIN
# ======================

def main():
    print(f"Searching YouTube for: '{SEARCH_QUERY}' (top {MAX_RESULTS} results)...")
    # (Keeping your original double-call pattern but only using the second result)
    # df_videos = search_youtube(SEARCH_QUERY, MAX_RESULTS)  # original line kept
    df_videos = search_youtube(SEARCH_QUERY, MAX_RESULTS)

    print(f"Fetched {len(df_videos)} videos.")

    df_videos, df_summary = analyze_brands_and_sentiment(df_videos)
    plot_graphs(df_summary)

    # Save results
    os.makedirs("output", exist_ok=True)
    videos_path = os.path.join("output", "videos_analysis.csv")
    summary_path = os.path.join("output", "brand_summary.csv")

    df_videos.to_csv(videos_path, index=False)
    df_summary.to_csv(summary_path, index=False)

    print("\n=== BRAND SUMMARY ===")
    print(df_summary.sort_values("sov_weighted_percent", ascending=False))

    print(f"\nSaved detailed video analysis to: {videos_path}")
    print(f"Saved brand summary to: {summary_path}")

if __name__ == "__main__":
    main()
