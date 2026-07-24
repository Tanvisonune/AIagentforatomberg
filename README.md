Share of Voice (SoV) Analysis using YouTube API – AI Agent

An AI agent that analyzes the **"smart fan"** search ecosystem on YouTube — extracting video and comment data, identifying brand mentions (Atomberg vs. competitors), performing sentiment analysis, and quantifying **Share of Voice (SoV)** using both raw mention counts and engagement-weighted metrics.

 🎯 Objective

To build an AI agent that:
- Analyzes the "smart fan" search ecosystem on YouTube
- Extracts video and comment data via the YouTube Data API
- Identifies brand mentions (Atomberg vs. competitors like Crompton, Usha, Havells, Bajaj, Luminous)
- Performs sentiment analysis on comments
- Quantifies Share of Voice using raw mentions and engagement-weighted metrics

 🛠️ Tech Stack

| Category | Tools / Libraries |

| Language | Python 3.10+ |
| Data Handling | Pandas |
| Sentiment Analysis | NLTK VADER (lightweight, no heavy model downloads) |
| API Access | Google API Client (YouTube Data API v3) |
| Visualization | Matplotlib |
| Progress Tracking | Tqdm |
| Utilities | OS / JSON (file management) |

📊 Data Sources

- **YouTube Search API** — query used: "smart fan`
- Fetches the **top 30 videos** (a sample size chosen to ensure diverse content while filtering out noise from low-engagement videos)

For each video, the agent collects:
- Title
- Description
- Channel
- View count
- Like count
- Comment count
- Top 20 comments (for rich user opinions)

 🏗️ Architecture


YouTube Search API
        │  (Video IDs)
        ▼
Video Details Extractor  (title, description, ...)
        │
        ▼
Comments Fetcher  (Top 20 comments)
        │
        ▼
Text Processor & Brand Counter  (Atomberg / Crompton / Usha / etc.)
        │
        ▼
Sentiment Analyzer  (NLTK VADER)
        │
        ▼
Share of Voice Calculator  (Raw SoV + Weighted SoV + Sentiment)
        │
        ▼
CSV + Graphs  (Final outputs)


## 📦 Deliverables

The agent generates the following outputs:

- videos_analysis.csv — per-video data with brand mentions and sentiment
- brand_summary.cs` — aggregated brand-level summary
- sov_mentions_percent.png — Share of Voice by raw mentions (chart)
- sov_weighted_percent.png — Share of Voice by engagement-weighted mentions (chart)

## 📐 Share of Voice Methodology

**Raw Share of Voice (Mentions SoV)** — measures how much each brand is talked about relative to others:


SoV_mentions = (Brand Mentions / Total Mentions of All Brands) × 100


Engagement-Weighted So* — measures not just mentions, but how important those mentions are, based on video views:


Weighted Mentions = Mentions × Video Views
SoV_weighted = (Weighted Mentions of Brand / Total Weighted Mentions of All Brands) × 100


 📈 Key Findings

- Atomberg dominates the "smart fan" conversation on YouTube, appearing in most high-engagement videos and discussions.
- Sentiment towards Atomberg is predominantly positive, reinforced by repeated mentions of "BLDC motor," "energy saving," and "smart controls."
- Comment-level observation show strong organic advocacy for Atomberg, with users frequently citing performance, savings, and reliability compared to competitors.

 Competitive Insights
- Usha appears occasionally, but with low engagement
- Crompton / Havells have minimal presence
- Bajaj / Luminous have almost no visibility

💡 Recommendations

- Increase collaborations with tech reviewers dominating "smart fan" content
- Target content around "BLDC vs Non-BLDC" comparisons
- Improve SEO for terms like "energy saving fan" and "remote controlled fan"
- Encourage user-generated content (UGC) around installation and performance
- Monitor competitor keywords on a monthly basis

 ✅ Conclusion

This AI agent provides a scalable way to quantify brand visibility and sentiment on YouTube. Atomberg currently leads the "smart fan" category by a large margin, with high positive sentiment and strong organic advocacy.



