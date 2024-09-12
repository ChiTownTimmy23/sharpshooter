import httpx
import logging
import pandas as pd
from typing import Dict, Any


async def fetch_external_data(url: str) -> Dict[str, Any]:
    """
    Fetch data from an external API using httpx.

    Args:
        url (str): The URL of the external API to fetch data from.

    Returns:
        Dict[str, Any]: The JSON response from the API.

    Raises:
        httpx.RequestError: If there's a network-related error.
        httpx.HTTPStatusError: If the HTTP response is an error status code.
    """
    logging.info(f"Fetching data from: {url}")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Raise an exception for HTTP error status codes
            return response.json()
    except httpx.RequestError as exc:
        logging.error(f"An error occurred while requesting {exc.request.url!r}.")
        raise
    except httpx.HTTPStatusError as exc:
        logging.error(
            f"Error response {exc.response.status_code} while requesting {exc.request.url!r}."
        )
        raise
    except Exception as exc:
        logging.error(f"An unexpected error occurred: {exc}")
        raise


def dict_to_dataframe(data: Dict[str, Any]) -> pd.DataFrame:
    """
    Convert a dictionary to a pandas DataFrame.

    Args:
        data (Dict[str, Any]): The input dictionary to be converted.

    Returns:
        pd.DataFrame: A DataFrame created from the input dictionary.

    Notes:
        - If the dictionary contains nested structures, they will be flattened.
        - Lists in the dictionary will be expanded into separate columns.
    """
    # Convert the dictionary to a DataFrame
    df = pd.DataFrame([data])
    
    # Expand lists into separate columns
    for column in df.columns:
        if isinstance(df[column].iloc[0], list):
            expanded = pd.DataFrame(df[column].tolist()).add_prefix(f"{column}_")
            df = pd.concat([df.drop(column, axis=1), expanded], axis=1)
    
    # Flatten nested dictionaries
    df = pd.json_normalize(df.to_dict(orient='records'))
    
    return df
