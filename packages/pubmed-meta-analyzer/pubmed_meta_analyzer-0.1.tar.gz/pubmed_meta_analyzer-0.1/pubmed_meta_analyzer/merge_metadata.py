import pandas as pd

def merge_metadata(file_path):
    """
    Merges and cleans metadata from an Excel file.

    Args:
        file_path (str): Path to the Excel file containing metadata.

    Returns:
        pd.DataFrame: Cleaned and sorted DataFrame.
    """
    df = pd.read_excel(file_path)
    df = df.drop_duplicates()
    df = df.sort_values(by=['Year', 'Month'], ascending=[False, False])
    return df