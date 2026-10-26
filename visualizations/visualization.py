
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


# ============================================================
# COMPARISON 5: VIDEO UPLOADS VS TOTAL VIDEO VIEWS
# Graph Type: Scatter Plot
# ============================================================

print("Creating Comparison 5...")

if {"uploads", "video_views"}.issubset(df.columns):

    df["uploads"] = pd.to_numeric(df["uploads"], errors="coerce")

    data = df[["uploads", "video_views"]].dropna()
    data = data[(data["uploads"] > 0) & (data["video_views"] > 0)]

    plt.figure(figsize=(9, 5))
    plt.scatter(data["uploads"], data["video_views"], alpha=0.6)

    plt.xscale("log")
    plt.yscale("log")

    plt.title("Comparison 5: Video Uploads vs Total Video Views")
    plt.xlabel("Number of Uploads (log scale)")
    plt.ylabel("Total Video Views (log scale)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output / "comparison_5_uploads_vs_views.png", dpi=150)
    plt.close()

else:
    print("Skipping Comparison 5: Required columns not found.")


# ============================================================
# COMPARISON 6: COUNTRY VS AVERAGE SUBSCRIBERS
# Graph Type: Horizontal Bar Chart
# ============================================================

print("Creating Comparison 6...")

if {"country", "subscribers"}.issubset(df.columns):

    country_data = df.dropna(subset=["country", "subscribers"]).copy()

    country_data["country"] = country_data["country"].astype(str).str.strip()

    country_data = country_data[
        ~country_data["country"].str.lower().isin(
            ["unknown", "nan", "none", ""]
        )
    ]

    country_subscribers = (
        country_data.groupby("country")["subscribers"]
        .mean()
        .nlargest(10)
        .sort_values()
    )

    plt.figure(figsize=(10, 6))
    plt.barh(country_subscribers.index, country_subscribers.values)

    plt.title("Comparison 6: Top 10 Countries by Average Subscribers")
    plt.xlabel("Average Subscribers")
    plt.ylabel("Country")
    plt.tight_layout()
    plt.savefig(output / "comparison_6_country_subscribers.png", dpi=150)
    plt.close()

else:
    print("Skipping Comparison 6: Required columns not found.")


# ============================================================
# COMPARISON 7: CHANNEL TYPE VS MONTHLY VIEWS
# Graph Type: Vertical Bar Chart
# ============================================================

print("Creating Comparison 7...")

monthly_views_column = "video_views_for_the_last_30_days"

if {"channel_type", monthly_views_column}.issubset(df.columns):

    df[monthly_views_column] = pd.to_numeric(
        df[monthly_views_column], errors="coerce"
    )

    channel_data = df.dropna(
        subset=["channel_type", monthly_views_column]
    ).copy()

    channel_data["channel_type"] = (
        channel_data["channel_type"].astype(str).str.strip()
    )

    channel_data = channel_data[
        ~channel_data["channel_type"].str.lower().isin(
            ["unknown", "nan", "none", ""]
        )
    ]

    channel_average = (
        channel_data.groupby("channel_type")[monthly_views_column]
        .mean()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(10, 6))
    plt.bar(channel_average.index, channel_average.values)

    plt.title("Comparison 7: Channel Type vs Average Monthly Views")
    plt.xlabel("Channel Type")
    plt.ylabel("Average Views in the Last 30 Days")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(output / "comparison_7_channel_type_monthly_views.png", dpi=150)
    plt.close()

else:
    print("Skipping Comparison 7: Required columns not found.")


# ============================================================
# COMPARISON 8: CREATION YEAR VS AVERAGE SUBSCRIBERS
# Graph Type: Line Graph
# ============================================================

print("Creating Comparison 8...")

if {"created_year", "subscribers"}.issubset(df.columns):

    df["created_year"] = pd.to_numeric(
        df["created_year"], errors="coerce"
    )

    year_data = df.dropna(
        subset=["created_year", "subscribers"]
    ).copy()

    year_data = year_data[
        (year_data["created_year"] >= 2000)
        & (year_data["created_year"] <= 2026)
    ]

    yearly_subscribers = (
        year_data.groupby("created_year")["subscribers"]
        .mean()
        .sort_index()
    )

    plt.figure(figsize=(10, 5))
    plt.plot(
        yearly_subscribers.index,
        yearly_subscribers.values,
        marker="o"
    )

    plt.title("Comparison 8: Channel Creation Year vs Average Subscribers")
    plt.xlabel("Channel Creation Year")
    plt.ylabel("Average Subscribers")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output / "comparison_8_year_vs_subscribers.png", dpi=150)
    plt.close()

else:
    print("Skipping Comparison 8: Required columns not found.")


# ============================================================
# COMPARISON 9: COUNTRY-WISE CHANNEL DISTRIBUTION
# Graph Type: Pie Chart
# ============================================================

print("Creating Comparison 9...")

if {"country", "youtuber"}.issubset(df.columns):

    country_counts = (
        df.dropna(subset=["country", "youtuber"])
        .assign(country=lambda x: x["country"].astype(str).str.strip())
    )

    country_counts = country_counts[
        ~country_counts["country"].str.lower().isin(
            ["unknown", "nan", "none", ""]
        )
    ]

    country_counts = (
        country_counts.groupby("country")["youtuber"]
        .nunique()
        .sort_values(ascending=False)
    )

    # Show the top 7 countries and group the rest as Other
    top_countries = country_counts.head(7).copy()

    other_count = country_counts.iloc[7:].sum()

    if other_count > 0:
        top_countries.loc["Other Countries"] = other_count

    plt.figure(figsize=(9, 7))
    plt.pie(
        top_countries.values,
        labels=top_countries.index,
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("Comparison 9: Country-Wise Channel Distribution")
    plt.tight_layout()
    plt.savefig(output / "comparison_9_country_pie_chart.png", dpi=150)
    plt.close()

else:
    print("Skipping Comparison 9: Required columns not found.")


# ============================================================
# COMPARISON 10: SUBSCRIBER DISTRIBUTION
# Graph Type: Box Plot
# ============================================================

print("Creating Comparison 10...")

if "subscribers" in df.columns:

    subscriber_data = df["subscribers"].dropna()
    subscriber_data = subscriber_data[subscriber_data >= 0]

    plt.figure(figsize=(9, 5))
    plt.boxplot(subscriber_data, vert=False)

    plt.title("Comparison 10: Distribution of Channel Subscribers")
    plt.xlabel("Number of Subscribers")
    plt.tight_layout()
    plt.savefig(output / "comparison_10_subscribers_boxplot.png", dpi=150)
    plt.close()

else:
    print("Skipping Comparison 10: Subscribers column not found.")


# ============================================================
# COMPARISON 11: CORRELATION BETWEEN NUMERIC VARIABLES
# Graph Type: Correlation Heatmap
# ============================================================

print("Creating Comparison 11...")

possible_columns = [
    "subscribers",
    "video_views",
    "uploads",
    "video_views_for_the_last_30_days",
    "highest_monthly_earnings",
    "lowest_monthly_earnings",
    "created_year"
]

available_columns = [
    column for column in possible_columns
    if column in df.columns
]

if len(available_columns) >= 2:

    for column in available_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    correlation = df[available_columns].corr()

    plt.figure(figsize=(11, 8))

    image = plt.imshow(correlation, cmap="coolwarm", vmin=-1, vmax=1)

    plt.colorbar(image, label="Correlation")

    plt.xticks(
        range(len(available_columns)),
        available_columns,
        rotation=45,
        ha="right"
    )

    plt.yticks(range(len(available_columns)), available_columns)

    # Display correlation values inside the heatmap
    for i in range(len(available_columns)):
        for j in range(len(available_columns)):
            value = correlation.iloc[i, j]

            if pd.notna(value):
                plt.text(
                    j, i, f"{value:.2f}",
                    ha="center",
                    va="center",
                    fontsize=8
                )

    plt.title("Comparison 11: Correlation Between YouTube Metrics")
    plt.tight_layout()
    plt.savefig(output / "comparison_11_correlation_heatmap.png", dpi=150)
    plt.close()

else:
    print("Skipping Comparison 11: Not enough numeric columns.")


# ============================================================
# FINAL RESULT
# ============================================================

print("\n" + "=" * 55)
print("ALL VISUALIZATIONS COMPLETED!")
print("=" * 55)

print("Your charts are saved in:")
print(output.resolve())

print("\nNew charts created:")
print("5. Uploads vs Total Video Views - Scatter Plot")
print("6. Country vs Average Subscribers - Bar Chart")
print("7. Channel Type vs Monthly Views - Bar Chart")
print("8. Creation Year vs Average Subscribers - Line Graph")
print("9. Country Distribution - Pie Chart")
print("10. Subscriber Distribution - Box Plot")
print("11. Numeric Relationships - Correlation Heatmap")

print("\nOpen the visualizations folder to view your graphs.")

