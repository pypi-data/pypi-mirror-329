# damakye_lda/utils.py

import pandas as pd

def load_dataset(filepath):
    """
    Load dataset from a CSV file into a pandas DataFrame.
    
    Args:
    filepath (str): The path to the dataset (CSV file).
    
    Returns:
    pd.DataFrame: The loaded dataset as a pandas DataFrame.
    """
    try:
        # Load the dataset
        dataset = pd.read_csv(filepath)
        return dataset
    except FileNotFoundError:
        print(f"Error: The file at {filepath} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: The file at {filepath} is empty.")
        return None
    except pd.errors.ParserError:
        print(f"Error: The file at {filepath} could not be parsed.")
        return None
