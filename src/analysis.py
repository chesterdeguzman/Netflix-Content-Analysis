"""Reusable Netflix catalog analysis utilities."""
from pathlib import Path
import pandas as pd


def load_and_clean(path: str | Path) -> pd.DataFrame:
    """Load the Netflix CSV and create analysis-ready features."""
    df = pd.read_csv(path)
    df = df.drop_duplicates().copy()
    df["date_added"] = pd.to_datetime(df["date_added"].str.strip(), errors="coerce")
    for column in ["director", "cast", "country", "rating", "duration"]:
        df[column] = df[column].fillna("Unknown")
    df["year_added"] = df["date_added"].dt.year.astype("Int64")
    df["month_added"] = df["date_added"].dt.month_name()
    df["primary_country"] = df["country"].str.split(",").str[0].str.strip()
    df["primary_genre"] = df["listed_in"].str.split(",").str[0].str.strip()
    values = pd.to_numeric(df["duration"].str.extract(r"(\d+)")[0], errors="coerce")
    df["movie_minutes"] = values.where(df["type"].eq("Movie"))
    df["seasons"] = values.where(df["type"].eq("TV Show"))
    return df


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[1]
    cleaned = load_and_clean(project_root / "data" / "netflix_titles.csv")
    cleaned.to_csv(project_root / "data" / "netflix_titles_cleaned.csv", index=False)
    print(f"Saved {len(cleaned):,} cleaned rows.")
