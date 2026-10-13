
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load cleaned dataset
df = pd.read_csv("youtube_data_cleaned.csv")

print("Dataset shape:", df.shape)
print("Columns:", df.columns.tolist())

# Create output folder
output = Path("visualizations")
output.mkdir(exist_ok=True)

# Prepare numeric columns
df["video_views"] = pd.to_numeric(df["video_views"], errors="coerce")
df["subscribers"] = pd.to_numeric(df["subscribers"], errors="coerce")

# 1. Top 10 YouTubers by video views
top = df.nlargest(10, "video_views").sort_values("video_views")

plt.figure(figsize=(10, 6))
plt.barh(top["youtuber"], top["video_views"])
plt.title("Top 10 YouTubers by Total Video Views")
plt.xlabel("Video Views")
plt.ylabel("YouTuber")
plt.tight_layout()
plt.savefig(output / "top_10_youtubers.png", dpi=150)
plt.close()

# 2. Distribution of video views
views = df["video_views"].dropna()

plt.figure(figsize=(8, 5))
plt.hist(views, bins=30, edgecolor="black")
plt.title("Distribution of YouTube Video Views")
plt.xlabel("Video Views")
plt.ylabel("Number of Channels")
plt.tight_layout()
plt.savefig(output / "views_distribution.png", dpi=150)
plt.close()

# 3. Subscribers vs video views
scatter_data = df[["subscribers", "video_views"]].dropna()

plt.figure(figsize=(8, 5))
plt.scatter(
    scatter_data["subscribers"],
    scatter_data["video_views"],
    alpha=0.6
)
plt.title("Subscribers vs Total Video Views")
plt.xlabel("Subscribers")
plt.ylabel("Video Views")
plt.tight_layout()
plt.savefig(output / "subscribers_vs_views.png", dpi=150)
plt.close()

# 4. NEW: Top 10 categories by total video views
category_views = (
    df.dropna(subset=["category", "video_views"])
      .groupby("category")["video_views"]
      .sum()
      .nlargest(10)
      .sort_values()
)

plt.figure(figsize=(10, 6))
plt.barh(category_views.index, category_views.values)
plt.title("Top 10 YouTube Categories by Total Views")
plt.xlabel("Total Video Views")
plt.ylabel("Category")
plt.tight_layout()
plt.savefig(output / "top_10_categories_by_views.png", dpi=150)
plt.close()

print("Success! All 4 charts saved in the visualizations folder.")
