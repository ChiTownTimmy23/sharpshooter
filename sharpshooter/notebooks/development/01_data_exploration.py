#!/usr/bin/env python
# coding: utf-8

# # Setup

# In[ ]:


# imports
import polars as pl
import httpx
from pathlib import Path

# Import from the _models directory and madden.py file
from notebooks._models.madden import PlayerRating, RatingsResponse


# In[ ]:


# Set the number of rows to display
pl.Config.set_tbl_cols(-1)  # None means no limit; you can also specify an integer.

# Set the number of columns to display
pl.Config.set_tbl_rows(-1)  # None means no limit; you can also specify an integer.


# # Utilities

# In[ ]:


# Create a Function that Gets the Headers of the dataframe and stores them in a list
def get_headers(df):
    headers_with_types = [(col, df[col].dtype) for col in df.columns]
    # Sort by data type first, then alphabetically within each data type
    sorted_headers = sorted(headers_with_types, key=lambda x: (str(x[1]), x[0]))
    sorted_headers_list = [col for col, dtype in sorted_headers]
    return sorted_headers, sorted_headers_list


# # Madden Ratings

# In[ ]:


BASE_URL = "https://ratings-api.ea.com/v2/entities"


# In[ ]:


# Create a Function to Read Data from the EA Sports Madden API
def get_madden_ratings(game_version: str, iteration: str) -> list[PlayerRating]:
    url = f"{BASE_URL}/{game_version}-ratings?filter=iteration:{iteration}"
    all_ratings = []

    with httpx.Client() as client:
        response = client.get(url)
        data = response.json()
        ratings_response = RatingsResponse(**data)
        all_ratings.extend(ratings_response.docs)

        total_count = ratings_response.count
        while len(all_ratings) < total_count:
            next_url = f"{url}&limit=100&offset={len(all_ratings)}"
            response = client.get(next_url)
            data = response.json()
            ratings_response = RatingsResponse(**data)
            all_ratings.extend(ratings_response.docs)

    return all_ratings


# In[ ]:


madden_data = get_madden_ratings("m24", "super-bowl")


# In[ ]:


# Count the Number
len(madden_data)

# Count the number of distinct players
len(set([player.primaryKey for player in madden_data]))

# Let's convert it to a DataFrame
madden_df = pl.DataFrame(madden_data)


# In[ ]:


madden_df.head()


# In[ ]:


madden_df = madden_df.with_columns(
    pl.col("plyrBirthdate").str.strptime(pl.Date, format="%m/%d/%Y")
)


# In[ ]:


madden_df.head()


# # NFL Verse Data

# In[ ]:


# Create a function to read parquet data from the NFL Verse repo
def get_nflverse_roster_data():
    url = 'https://github.com/nflverse/nflverse-data/releases/download/rosters/roster_2024.parquet'
    df = pl.read_parquet(url)
    return df


# In[ ]:


# Create a function to read parquet data from the NFL Verse repo
def get_nflverse_player_data():
    url = 'https://github.com/nflverse/nflverse-data/releases/download/players/players.parquet'
    df = pl.read_parquet(url)
    return df


# In[ ]:


# Create a function to read parquet data from the NFL Verse repo that accepts and argument as 'year'
def get_nflverse_depth_charts_data(year: int):
    url = f'https://github.com/nflverse/nflverse-data/releases/download/depth_charts/depth_charts_{year}.parquet'
    df = pl.read_parquet(url)
    return df   


# In[ ]:


# Create a function to read parquet data from the NFL Verse repo that accepts and argument as 'year'
def get_nflverse_weekly_rosters_data(year: int):
    url = f'https://github.com/nflverse/nflverse-data/releases/download/weekly_rosters/roster_weekly_{year}.parquet'
    df = pl.read_parquet(url)
    return df   


# In[ ]:


# Create a function to read parquet data from the NFL Verse repo that accepts and argument as 'year'
def get_nflverse_pbp_data(year: int):
    url = f'https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_{year}.parquet'
    df = pl.read_parquet(url)
    return df   


# In[ ]:


# Let's convert the nflverse data to a DataFrame
roster_df = get_nflverse_roster_data()
player_df = get_nflverse_player_data()
depth_charts_df = get_nflverse_depth_charts_data(2023)
weekly_roster_df = get_nflverse_weekly_rosters_data(2024)
pbp_df = get_nflverse_pbp_data(2023)


# In[ ]:


sorted_headers, sorted_headers_list = get_headers(roster_df)


# In[ ]:


pbp_df.sample(20, seed = 23).write_clipboard(separator=",")


# # ESPN Rankings

# In[ ]:


def get_espn_rankings():
    # Get the directory of the current notebook
    notebook_dir = Path().absolute()
    
    # Navigate up to the project root and then to the data directory
    project_root = notebook_dir.parent.parent
    data_path = project_root / 'data' / 'NFL_Rankings_Complete.csv'
    
    # Check if the file exists
    if not data_path.exists():
        raise FileNotFoundError(f"The file {data_path} does not exist.")
    
    # Read the CSV file
    df = pl.read_csv(data_path)
    return df


# In[ ]:


# Let's convert the ESPN Rankings data to a DataFrame
espn_df = get_espn_rankings()
espn_df.head()


# # Draftkings Rankings

# In[ ]:


def get_draftkings_rankings():
    # Get the directory of the current notebook
    notebook_dir = Path().absolute()
    
    # Navigate up to the project root and then to the data directory
    project_root = notebook_dir.parent.parent
    data_path = project_root / 'data' / 'DkPreDraftRankings.csv'
    
    # Check if the file exists
    if not data_path.exists():
        raise FileNotFoundError(f"The file {data_path} does not exist.")
    
    # Read the CSV file
    df = pl.read_csv(data_path)
    return df

# Test the function
draftkings_df = get_draftkings_rankings()


# In[ ]:


draftkings_df = get_draftkings_rankings()
draftkings_df.head()


# In[ ]:


# Create a dictionary for name mapping
name_mapping = {
    "Hollywood Brown": "Marquise Brown",
    "DJ Chark": "DJ Chark Jr.",
    # Add more mappings as needed
}


# In[ ]:


# Function to apply the mapping
def map_name(name):
    return name_mapping.get(name, name)


# In[ ]:


# Apply the mapping to the DraftKings dataframe
draftkings_df = draftkings_df.with_columns(
    pl.col('Name').map_elements(map_name).alias('Mapped Name')
)


# In[ ]:


draftkings_df.head()


# In[ ]:


def combine_rankings(draftkings_df: pl.DataFrame, espn_df: pl.DataFrame) -> pl.DataFrame:
    """
    Perform a left join on ESPN and DraftKings dataframes based on player name.
    
    Args:
    draftkings_df (pl.DataFrame): DraftKings rankings dataframe
    espn_df (pl.DataFrame): ESPN rankings dataframe

    
    Returns:
    pl.DataFrame: Combined dataframe with ESPN rankings as the base
    """
    # Rename columns to avoid conflicts and clarify source
    draftkings_df = draftkings_df.rename({
        "ADP": "DraftKings_ADP",
        "Position": "DraftKings_Position",
        "Team": "DraftKings_Team"
    })
    
    espn_df = espn_df.rename({
        "Overall Rank": "ESPN_Rank",
        "Positional Rank": "ESPN_Positional_Rank",
        "Salary Cap Value": "ESPN_Salary_Cap_Value"
    })
    

    
    # Perform the left join
    combined_df = draftkings_df.join(
        espn_df,
        left_on="Mapped Name",
        right_on="Player Name",
        how="left"
    )
    
    # Drop the duplicate "Name" column from DraftKings
    # combined_df = combined_df.drop("Name")
    
    return combined_df

# Example usage:
# espn_df = pl.read_csv("espn_rankings_sample.csv")
# draftkings_df = pl.read_csv("draftkings_rankings_sample.csv")
result = combine_rankings(draftkings_df, espn_df)
# print(result)


# In[ ]:


result.write_csv("combined_rankings.csv")


# In[ ]:


dk_to_madden_name_mapping = {
    "Deebo Samuel Sr.": "Deebo Samuel Sr",
    "Marvin Harrison Jr.": "Marvin Harrison Jr",
    "Travis Etienne Jr." : "Travis Etienne Jr",
    "DJ Moore": "D.J. Moore",
    "DK Metcalf": "D.K. Metcalf",
    "Michael Pittman Jr.": "Michael Pittman Jr",
    "Hollywood Brown": "Marquise Brown",
    "Brian Thomas Jr.": "Brian Thomas Jr",
    "Brian Robinson Jr.": "Brian Robinson Jr",
    "Marvin Mims Jr.": "Marvin Mims Jr",
    "Tyrone Tracy Jr.": "Tyrone Tracy Jr",
    "DJ Chark": "DJ Chark Jr",
    "AJ Dillon": "A.J. Dillon",
    "Chris Rodriguez Jr.": "Chris Rodriguez Jr",
    "Odell Beckham Jr.": "Odell Beckham Jr",
    "Michael Penix Jr.": "Michael Penix Jr",
    "DeMario Douglas": "Demario Douglas",
    # Add more mappings as needed
}

def combine_madden_with_rankings(combined_df: pl.DataFrame, madden_df: pl.DataFrame) -> pl.DataFrame:
    """
    Perform a left join on the Combined Ranks and Madden dataframes based on player name, team, and position.
    
    Args:
    combined_df (pl.DataFrame): Combined rankings dataframe
    madden_df (pl.DataFrame): Madden ratings dataframe

    Returns:
    pl.DataFrame: Combined dataframe with Combined Rankings as the base
    """
    # Apply the name mapping to the combined_df
    combined_df = combined_df.with_columns(
        pl.when(pl.col("Name").is_in(dk_to_madden_name_mapping.keys()))
          .then(pl.col("Name").replace(dk_to_madden_name_mapping))
          .otherwise(pl.col("Name"))
          .alias("Mapped_Name")
    )

    # Rename columns to avoid conflicts and clarify source
    combined_df = combined_df.rename({
        "Mapped_Name": "Join_Name"
    })
    
    madden_df = madden_df.rename({
        "fullName": "Join_Name",
    })   

    # Perform the left join
    combined_madden_df = combined_df.join(
        madden_df,
        on=["Join_Name"],
        how="left"
    )
    
    # Select only the required columns from madden_df
    madden_df_selected = combined_madden_df.select([
        "ID",
        "Name",
        "DraftKings_Position",
        "DraftKings_ADP",
        "DraftKings_Team",
        "ESPN_Rank",
        "ESPN_Positional_Rank",
        "overallRating"
    ])    
    
    return madden_df_selected


# In[ ]:


combined_madden_df_t = combine_madden_with_rankings(result, df)


# In[ ]:


combined_madden_df_t.head(5)


# In[ ]:


# Filter the Madden Dataframe for Players with the fullNameForSearch *like* Marvin Harrison
combined_madden_df_t.filter(pl.col("Name").str.contains("DeMario"))


# In[ ]:


combined_madden_df_t.write_csv("combined_madden_rankings.csv")


# In[ ]:


# Create a Dictionary between the 'fullName' and 'Name' columns
dk_to_madden_name_mapping = {
    "Deebo Samuel Sr.": "Deebo Samuel Sr",
    "Marvin Harrison Jr.": "Marvin Harrison Jr",
    # Add more mappings as needed
}

# Create a Function to apply the mapping
def map_name(name):
    return name_mapping.get(name, name)


# In[ ]:


# Find Marvin Harrison in the df Dataframe

df.filter(pl.col("fullName").str.contains("Deebo"))


# In[ ]:


combined_madden_df_t.head(100)


# In[ ]:


# Let's add a column to the df dataframe that combines firstName and lastName Columns and place it first
madden25_df = df.with_columns([
    pl.col("firstName") + " " + pl.col("lastName").alias("fullName")
])


# In[ ]:


# Filter the Madden Dataframe for Players with the fullNameForSearch *like* Marvin Harrison
madden_df.filter(pl.col("fullNameForSearch").str.contains("Marvin Harrison"))


# madden_df.filter(pl.col("fullNameForSearch") == "Marvin Harrison Jr")


# In[ ]:


import httpx
from pydantic import BaseModel, Field
from typing import List, Optional, Union, Dict

BASE_URL = "https://drop-api.ea.com/rating/madden-nfl"

class Team(BaseModel):
    id: int
    label: str
    imageUrl: str
    isPopular: bool

class PositionType(BaseModel):
    id: str
    name: str

class Position(BaseModel):
    id: str
    shortLabel: str
    label: str
    positionType: PositionType

class Archetype(BaseModel):
    id: str
    label: str

class Iteration(BaseModel):
    id: str
    label: str

class NumericStat(BaseModel):
    value: float
    diff: int

class RunningStyleStat(BaseModel):
    value: str
    diff: int

class AbilityType(BaseModel):
    id: str
    label: str
    imageUrl: str
    iconUrl: str

class Ability(BaseModel):
    id: str
    label: str
    description: str
    imageUrl: str
    type: AbilityType

class PlayerRating(BaseModel):
    id: int
    overallRating: int
    firstName: str
    lastName: str
    birthdate: str
    height: int
    weight: int
    college: str
    handedness: int
    age: int
    jerseyNum: int
    yearsPro: int
    playerAbilities: List[Ability]
    avatarUrl: Optional[str]
    archetype: Optional[Archetype]
    team: Team
    position: Position
    iteration: Iteration
    stats: Dict[str, Union[NumericStat, RunningStyleStat]]

class RatingsResponse(BaseModel):
    items: List[PlayerRating]
    totalItems: int

def get_madden_ratings(locale: str = "en") -> List[PlayerRating]:
    url = f"{BASE_URL}?locale={locale}"
    all_ratings = []

    with httpx.Client() as client:
        response = client.get(url)
        response.raise_for_status()
        data = response.json()
        ratings_response = RatingsResponse(**data)
        all_ratings.extend(ratings_response.items)

        total_count = ratings_response.totalItems
        while len(all_ratings) < total_count:
            next_url = f"{url}&limit=100&offset={len(all_ratings)}"
            response = client.get(next_url)
            response.raise_for_status()
            data = response.json()
            ratings_response = RatingsResponse(**data)
            all_ratings.extend(ratings_response.items)

    print(f"Total items fetched: {len(all_ratings)}")
    print(f"Expected total items: {total_count}")

    return all_ratings

def create_madden_nfl_dataframe():
    ratings = get_madden_ratings()
    
    # Convert Pydantic models to dictionaries
    data = [rating.dict() for rating in ratings]
    
    # Create DataFrame
    df = pl.DataFrame(data)
    
    # Add fullName column
    df = df.with_columns([
        (pl.col("firstName") + " " + pl.col("lastName")).alias("fullName")
    ])
    
    # Flatten nested structures
    df = df.with_columns([
        pl.col("team").struct.field("id").alias("team_id"),
        pl.col("team").struct.field("label").alias("team_label"),
        pl.col("team").struct.field("imageUrl").alias("team_imageUrl"),
        pl.col("team").struct.field("isPopular").alias("team_isPopular"),
        pl.col("position").struct.field("id").alias("position_id"),
        pl.col("position").struct.field("shortLabel").alias("position_shortLabel"),
        pl.col("position").struct.field("label").alias("position_label"),
        pl.col("position").struct.field("positionType").struct.field("id").alias("position_type_id"),
        pl.col("position").struct.field("positionType").struct.field("name").alias("position_type_name"),
        pl.col("iteration").struct.field("id").alias("iteration_id"),
        pl.col("iteration").struct.field("label").alias("iteration_label"),
    ])

    # Flatten stats
    stat_columns = df.select(pl.col("stats")).to_series().struct.fields
    for stat in stat_columns:
        df = df.with_columns([
            pl.col("stats").struct.field(stat).struct.field("value").alias(f"stat_{stat}")
        ])

    # Drop original nested columns
    df = df.drop(["team", "position", "iteration", "stats", "playerAbilities"])

    # Convert data types
    date_columns = ["birthdate"]
    int_columns = ["id", "overallRating", "height", "weight", "handedness", "age", "jerseyNum", "yearsPro", "team_id"]
    float_columns = [col for col in df.columns if col.startswith("stat_") and col != "stat_runningStyle"]
    bool_columns = ["team_isPopular"]

    for col in date_columns:
        df = df.with_columns(pl.col(col).str.to_date("%Y-%m-%d").alias(col))

    for col in int_columns:
        df = df.with_columns(pl.col(col).cast(pl.Int64))

    for col in float_columns:
        df = df.with_columns(pl.col(col).cast(pl.Float64))

    for col in bool_columns:
        df = df.with_columns(pl.col(col).cast(pl.Boolean))

    print(f"DataFrame shape: {df.shape}")
    return df

# Example usage
if __name__ == "__main__":
    df = create_madden_nfl_dataframe()


# In[ ]:


# Create a Column that concatenates the 'firstName' and 'lastName' columns
madden25_df = madden25_df.with_columns([
    pl.col("firstName") + " " + pl.col("lastName").alias("fullName")
])


# In[ ]:


madden25_df.head()


# In[ ]:




