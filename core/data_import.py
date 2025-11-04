import requests
import pandas as pd
import sqlite3

# Default shared Census API key (safe for light usage)
CENSUS_API_KEY = "bb7b2fbe4bfa7c09174aa019ba320c5bc45fc9ed"

# Data source: American Community Survey 5-year estimates
YEAR = 2023
DATASET = "acs/acs5"
VARIABLES = ["NAME", "B01003_001E"]  # State name + total population
GEOGRAPHY = "state:*"


def fetch_population_by_state():
    """Fetch total population by state from the U.S. Census API."""
    url = f"https://api.census.gov/data/{YEAR}/{DATASET}"
    params = {
        "get": ",".join(VARIABLES),
        "for": GEOGRAPHY,
        "key": CENSUS_API_KEY,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    # Convert JSON to DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])
    df = df.rename(columns={"NAME": "state", "B01003_001E": "population"})
    df["population"] = df["population"].astype(int)
    return df


def store_population_data(df):
    """Create a table and save the population data in SQLite."""
    conn = sqlite3.connect("data/financeflow.db")
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS state_population (
            state TEXT PRIMARY KEY,
            population INTEGER
        )
        """
    )

    for _, row in df.iterrows():
        c.execute(
            "INSERT OR REPLACE INTO state_population (state, population) VALUES (?, ?)",
            (row["state"], row["population"]),
        )

    conn.commit()
    conn.close()


def import_population_data():
    """Main function to fetch and store population data."""
    df = fetch_population_by_state()
    store_population_data(df)
    print("Population data imported successfully for all states.")


if __name__ == "__main__":
    import_population_data()
