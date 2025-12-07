import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="Smart Fan Market Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------
# CORPORATE CSS STYLING
# -------------------------
st.markdown("""
    <style>
    /* Atomberg Brand Colors */
    :root {
        --primary-color: #FDB813;
        --secondary-color: #F5A623;
        --accent-color: #FFD700;
        --text-dark: #000000;
        --bg-light: #FFFEF7;
    }
    
    /* Main container */
    .main {
        background-color: #ffffff;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FDB813 0%, #F5A623 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: #000000 !important;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-size: 28px;
        color: #000000;
        font-weight: 600;
    }
    
    [data-testid="stMetricLabel"] {
        color: #4a4a4a;
        font-size: 14px;
        font-weight: 500;
    }
    
    /* Headers */
    h1 {
        color: #000000;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 600;
        border-bottom: 3px solid #FDB813;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    h2, h3 {
        color: #000000;
        font-weight: 500;
    }
    
    /* Data tables */
    [data-testid="stDataFrame"] {
        border: 1px solid #FDB813;
        border-radius: 4px;
    }
    
    /* Buttons and inputs */
    .stButton>button {
        background-color: #FDB813;
        color: #000000;
        border: none;
        border-radius: 4px;
        padding: 8px 20px;
        font-weight: 600;
    }
    
    .stButton>button:hover {
        background-color: #F5A623;
    }
    
    /* Info/Success boxes */
    .stSuccess {
        background-color: #FFF9E6;
        border-left: 4px solid #FDB813;
        padding: 12px;
        border-radius: 4px;
    }
    
    .stInfo {
        background-color: #FFFEF7;
        border-left: 4px solid #F5A623;
        padding: 12px;
        border-radius: 4px;
    }
    
    /* Dividers */
    hr {
        border: none;
        border-top: 2px solid #e0e6ed;
        margin: 30px 0;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------
# LOAD DATA
# -------------------------
SUMMARY_PATH = "output/brand_summary.csv"
VIDEOS_PATH = "output/videos_analysis.csv"

@st.cache_data
def load_data():
    df_summary = pd.read_csv(SUMMARY_PATH)
    df_videos = pd.read_csv(VIDEOS_PATH)
    return df_summary, df_videos

df_summary, df_videos = load_data()

# -------------------------
# CORPORATE CHART STYLING
# -------------------------
def set_corporate_style():
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 11
    plt.rcParams['axes.titlesize'] = 12
    plt.rcParams['xtick.labelsize'] = 9
    plt.rcParams['ytick.labelsize'] = 9
    plt.rcParams['legend.fontsize'] = 9
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.3
    plt.rcParams['grid.linestyle'] = '--'

set_corporate_style()

ATOMBERG_YELLOW = '#FDB813'
ATOMBERG_GOLD = '#F5A623'
ATOMBERG_BLACK = '#000000'

def create_corporate_bar_chart(x, y, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(10, 5), facecolor='white')
    ax.set_facecolor('#f8f9fa')
    
    bars = ax.bar(x, y, color=ATOMBERG_YELLOW, edgecolor=ATOMBERG_BLACK, linewidth=1.2, alpha=0.9)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        label = f'{height:.1f}%' if '%' in ylabel else f'{int(height):,}'
        ax.text(bar.get_x() + bar.get_width()/2., height,
                label, ha='center', va='bottom', fontweight='600', fontsize=9, color=ATOMBERG_BLACK)
    
    ax.set_xlabel(xlabel, fontweight='600', color=ATOMBERG_BLACK)
    ax.set_ylabel(ylabel, fontweight='600', color=ATOMBERG_BLACK)
    ax.set_title(title, fontweight='600', fontsize=13, color=ATOMBERG_BLACK, pad=15)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#666666')
    ax.spines['bottom'].set_color('#666666')
    
    plt.xticks(rotation=0)
    plt.tight_layout()
    return fig

# -------------------------
# SIDEBAR
# -------------------------
with st.sidebar:
    st.markdown("# Smart Fan ")
    st.markdown("### Market Intelligence Dashboard")
    st.markdown("---")
    
    page = st.radio(
        "Navigation Menu",
        ["Overview", "Brand Deep Dive", "Comments Explorer"]
    )
    
    st.markdown("---")
    st.markdown("#### Dataset Summary")
    st.markdown(f"**Videos Analyzed:** {len(df_videos):,}")
    st.markdown(f"**Brands Tracked:** {len(df_summary)}")
    st.markdown(f"**Total Mentions:** {int(df_summary['total_mentions'].sum()):,}")

# =====================================================
# PAGE 1 : OVERVIEW
# =====================================================
if page == "Overview":
    st.title("Smart Fan Market Dashboard")
    st.subheader("Share of Voice Analysis - YouTube Market Data")
    
    # Key Performance Indicators
    atomberg = df_summary[df_summary["brand"] == "atomberg"].iloc[0]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Atomberg SoV (Mentions)", f"{atomberg['sov_mentions_percent']:.2f}%")
    
    with col2:
        st.metric("Atomberg SoV (Weighted)", f"{atomberg['sov_weighted_percent']:.2f}%")
    
    with col3:
        st.metric("Videos Analyzed", f"{len(df_videos):,}")
    
    with col4:
        st.metric("Total Brand Mentions", f"{int(df_summary['total_mentions'].sum()):,}")
    
    st.markdown("---")
    
    # Chart Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Share of Voice by Mentions")
        fig1 = create_corporate_bar_chart(
            df_summary["brand"].str.title(),
            df_summary["sov_mentions_percent"],
            "Brand Mention Distribution",
            "Brand",
            "Percentage (%)"
        )
        st.pyplot(fig1)
    
    with col2:
        st.markdown("### Share of Voice by Engagement")
        fig2 = create_corporate_bar_chart(
            df_summary["brand"].str.title(),
            df_summary["sov_weighted_percent"],
            "Weighted Engagement Analysis",
            "Brand",
            "Weighted Percentage (%)"
        )
        st.pyplot(fig2)
    
    st.markdown("---")
    
    # Summary Table
    st.markdown("### Brand Performance Summary")
    
    summary_table = df_summary[["brand", "total_mentions", "weighted_mentions", 
                                 "sov_mentions_percent", "sov_weighted_percent", 
                                 "videos_with_mentions"]].copy()
    summary_table.columns = ["Brand", "Total Mentions", "Weighted Mentions", 
                             "SoV Mentions %", "SoV Weighted %", "Videos"]
    summary_table["Brand"] = summary_table["Brand"].str.title()
    summary_table = summary_table.sort_values("SoV Weighted %", ascending=False)
    
    st.dataframe(
        summary_table.style.format({
            "Total Mentions": "{:,.0f}",
            "Weighted Mentions": "{:,.0f}",
            "SoV Mentions %": "{:.2f}",
            "SoV Weighted %": "{:.2f}",
            "Videos": "{:,.0f}"
        }),
        use_container_width=True,
        height=300
    )
    
    st.success("**Key Finding:** Atomberg demonstrates clear market leadership in both mention volume and engagement-weighted metrics.")

# =====================================================
# PAGE 2 : BRAND DEEP DIVE
# =====================================================
elif page == "Brand Deep Dive":
    st.title("Brand Deep Dive Analysis")
    
    brand = st.selectbox("Select Brand", df_summary["brand"].unique())
    
    brand_row = df_summary[df_summary["brand"] == brand].iloc[0]
    
    # Brand Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Mentions", f"{int(brand_row['total_mentions']):,}")
    
    with col2:
        st.metric("Weighted Mentions", f"{int(brand_row['weighted_mentions']):,}")
    
    with col3:
        st.metric("Videos with Brand", f"{int(brand_row['videos_with_mentions']):,}")
    
    with col4:
        st.metric("SoV (Weighted)", f"{brand_row['sov_weighted_percent']:.2f}%")
    
    st.markdown("---")
    
    # Charts Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Sentiment Distribution")
        
        sentiments = ["positive_videos", "neutral_videos", "negative_videos"]
        sentiment_labels = ["Positive", "Neutral", "Negative"]
        values = [brand_row[s] for s in sentiments]
        
        fig3, ax3 = plt.subplots(figsize=(8, 5), facecolor='white')
        ax3.set_facecolor('#f8f9fa')
        
        colors = ["#FDB813", '#6c757d', '#dc3545']
        bars = ax3.bar(sentiment_labels, values, color=colors, edgecolor=ATOMBERG_BLACK, 
                       linewidth=1.2, alpha=0.85)
        
        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', fontweight='600', color=ATOMBERG_BLACK)
        
        ax3.set_ylabel("Number of Videos", fontweight='600', color=ATOMBERG_BLACK)
        ax3.set_title(f"Sentiment Analysis - {brand.title()}", fontweight='600', 
                     color=ATOMBERG_BLACK, pad=15)
        ax3.spines['top'].set_visible(False)
        ax3.spines['right'].set_visible(False)
        ax3.spines['left'].set_color('#666666')
        ax3.spines['bottom'].set_color('#666666')
        plt.tight_layout()
        st.pyplot(fig3)
    
    with col2:
        st.markdown("### Share of Voice Metrics")
        
        fig4, ax4 = plt.subplots(figsize=(8, 5), facecolor='white')
        ax4.set_facecolor('#f8f9fa')
        
        metrics = ['Mentions %', 'Engagement %']
        brand_values = [brand_row['sov_mentions_percent'], brand_row['sov_weighted_percent']]
        
        bars = ax4.bar(metrics, brand_values, color=ATOMBERG_YELLOW, 
                      edgecolor=ATOMBERG_BLACK, linewidth=1.2, alpha=0.9)
        
        for bar in bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom', fontweight='600', color=ATOMBERG_BLACK)
        
        ax4.set_ylabel('Percentage', fontweight='600', color=ATOMBERG_BLACK)
        ax4.set_title('Share of Voice Comparison', fontweight='600', 
                     color=ATOMBERG_BLACK, pad=15)
        ax4.spines['top'].set_visible(False)
        ax4.spines['right'].set_visible(False)
        ax4.spines['left'].set_color('#666666')
        ax4.spines['bottom'].set_color('#666666')
        plt.tight_layout()
        st.pyplot(fig4)
    
    st.markdown("---")
    
    # Video Table
    st.markdown(f"### Videos Featuring {brand.title()}")
    
    filtered = df_videos[df_videos[brand + "_mentions"] > 0].copy()
    
    if len(filtered) > 0:
        display_data = filtered[["title", "channel_title", "view_count", "overall_sentiment"]].copy()
        display_data.columns = ["Title", "Channel", "Views", "Sentiment"]
        display_data["Sentiment"] = display_data["Sentiment"].str.title()
        display_data = display_data.sort_values("Views", ascending=False)
        
        st.dataframe(
            display_data.style.format({"Views": "{:,.0f}"}),
            use_container_width=True,
            height=400
        )
    else:
        st.info(f"No videos found featuring {brand.title()}")

# =====================================================
# PAGE 3 : COMMENTS EXPLORER
# =====================================================
elif page == "Comments Explorer":
    st.title("Content & Comment Explorer")
    st.subheader("Search and analyze video content by brand and keywords")
    
    # Filters
    col1, col2 = st.columns([1, 2])
    
    with col1:
        brand = st.selectbox("Filter by Brand", ["All"] + list(df_summary["brand"].unique()))
    
    with col2:
        search = st.text_input("Search in Titles/Descriptions", placeholder="Enter keywords...")
    
    # Apply Filters
    filtered = df_videos.copy()
    
    if brand != "All":
        filtered = filtered[filtered[brand + "_mentions"] > 0]
    
    if search:
        mask = (filtered["title"].str.contains(search, case=False, na=False) | 
                filtered["description"].str.contains(search, case=False, na=False))
        filtered = filtered[mask]
    
    st.markdown(f"**Results:** Showing {len(filtered)} of {len(df_videos)} videos")
    
    if len(filtered) > 0:
        # Summary Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Views", f"{filtered['view_count'].sum():,.0f}")
        
        with col2:
            st.metric("Average Views", f"{filtered['view_count'].mean():,.0f}")
        
        with col3:
            st.metric("Unique Channels", f"{filtered['channel_title'].nunique()}")
        
        with col4:
            most_common = filtered['overall_sentiment'].value_counts().index[0]
            st.metric("Dominant Sentiment", most_common.title())
        
        st.markdown("---")
        
        # Results Table
        st.markdown("### Video Content")
        
        display_data = filtered[["title", "channel_title", "description", 
                                "overall_sentiment", "view_count"]].copy()
        display_data.columns = ["Title", "Channel", "Description", "Sentiment", "Views"]
        display_data["Sentiment"] = display_data["Sentiment"].str.title()
        display_data = display_data.sort_values("Views", ascending=False)
        
        st.dataframe(
            display_data.style.format({"Views": "{:,.0f}"}),
            use_container_width=True,
            height=450
        )
    else:
        st.info("No videos match your search criteria. Please adjust filters.")
    
    st.info("**Note:** Use this tool to explore how brands are discussed in video content and identify trends in audience engagement.")

# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #5a6c7d; padding: 20px;'>
        <p><strong>Smart Fan Market Intelligence Dashboard</strong></p>
        <p> Data Source: YouTube </p>
    </div>
""", unsafe_allow_html=True)