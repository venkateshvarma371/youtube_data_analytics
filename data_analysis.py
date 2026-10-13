
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. Load the cleaned dataset
file_path = Path("data/cleaned/youtube_data_cleaned.csv")
df = pd.read_csv(file_path)

print("=" * 50)
print("YOUTUBE DATA ANALYSIS")
print("=" * 50)

# 2. Dataset overview
print("\n1. DATASET OVERVIEW")
print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])
print("\nColumn names:")
print(df.columns.tolist())

# 3. Summary statistics
print("\n2. SUMMARY STATISTICS")
print(df.describe(include="all").T)

# 4. Top 10 channels by subscribers
if "subscribers" in df.columns and "youtuber" in df.columns:
    top_subscribers = df.nlargest(10, "subscribers")

    print("\n3. TOP 10 CHANNELS BY SUBSCRIBERS")
    print(top_subscribers[["youtuber", "subscribers"]].to_string(index=False))

    top_subscribers[["youtuber", "subscribers"]].to_csv(
        "top_10_subscribers.csv", index=False
    )

    ax = top_subscribers.plot(
        x="youtuber", y="subscribers", kind="bar",
        legend=False, figsize=(12, 6)
    )
    ax.set_title("Top 10 YouTube Channels by Subscribers")
    ax.set_xlabel("Channel")
    ax.set_ylabel("Subscribers")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("top_10_subscribers.png")
    plt.close()

# 5. Top 10 channels by video views
if "video_views" in df.columns and "youtuber" in df.columns:
    top_views = df.nlargest(10, "video_views")

    print("\n4. TOP 10 CHANNELS BY VIDEO VIEWS")
    print(top_views[["youtuber", "video_views"]].to_string(index=False))

    top_views[["youtuber", "video_views"]].to_csv(
        "top_10_views.csv", index=False
    )

    ax = top_views.plot(
        x="youtuber", y="video_views", kind="bar",
        legend=False, figsize=(12, 6)
    )
    ax.set_title("Top 10 YouTube Channels by Video Views")
    ax.set_xlabel("Channel")
    ax.set_ylabel("Video Views")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("top_10_views.png")
    plt.close()

# 6. Analyse channel categories
if "category" in df.columns:
    print("\n5. CHANNELS BY CATEGORY")
    print(df["category"].value_counts(dropna=False).head(15))

    df["category"].value_counts().head(10).plot(
        kind="bar", figsize=(10, 5)
    )
    plt.title("Top 10 YouTube Categories by Channel Count")
    plt.xlabel("Category")
    plt.ylabel("Number of Channels")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("category_distribution.png")
    plt.close()

# 7. Correlation between subscribers and views
if {"subscribers", "video_views"}.issubset(df.columns):
    correlation = df["subscribers"].corr(df["video_views"])
    print("\n6. SUBSCRIBERS VS VIDEO VIEWS")
    print("Correlation:", round(correlation, 3))

# 8. Save overall numeric statistics
df.describe().T.to_csv("analysis_summary.csv")

print("\nANALYSIS COMPLETED")
print("Summary saved to analysis_summary.csv")
print("Charts and top-channel CSV files saved in project folder.")