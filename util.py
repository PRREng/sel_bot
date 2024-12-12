import pandas as pd
from pandas import Series
import os
from glob import glob
from typing import List, Any

month = {
    1: "janeiro",
    2: "fevereiro",
    3: "março",
    4: "abril",
    5: "maio",
    6: "junho",
    7: "julho",
    8: "agosto",
    9: "setembro",
    10: "outubro",
    11: "novembro",
    12: "dezembro"
}

def rename_file(directory, client, month_num, year):
    # Define the file pattern
    mes = month[int(month_num)]
    old_file_pattern = f"{mes} {year}.pdf"

    # Search for the file in the directory
    files = glob(os.path.join(directory, old_file_pattern))
    
    if not files:
        print(f"No file matching '{old_file_pattern}' found in {directory}.")
        return

    # Take the first matching file (assuming there's one file with the pattern)
    old_file_path = files[0]

    # Define the new file name
    new_file_name = f"{client} - {mes} {year}.pdf"
    new_file_path = os.path.join(directory, new_file_name)

    # Rename the file
    os.rename(old_file_path, new_file_path)
    print(f"Renamed '{old_file_path}' to '{new_file_path}'.")

# def rename_file(old_filepath, new_filename) -> None:
#     dir_path = os.path.dirname(old_filepath)
#     new_filepath = os.path.join(dir_path, new_filename)
#
#     os.rename(old_filepath, new_filepath)
#     return


def get_DataFrame(directory_path):

    csv_pattern = os.path.join(directory_path, "*.csv")

    csv_files = glob(csv_pattern)

    if not csv_files:
        print("No CSV files found in the directory.")
        return

    try:
        df = pd.read_csv(csv_files[0])
        print(csv_files[0])
        print("CSV file read successfully.")
        return df
    except Exception as e:
        print(f"Error reading the CSV file: {e}")

    return


def get_ProList(directory_path) -> Series | Any | None:
    df = get_DataFrame(directory_path)
    if df is None:
        return None

    client_series = df[df["Plano"] == "Pro"]['Nome da Usina']
    # print(client_series)
    # print(f"Numero de clientes Pro: {len(client_series)}")

    return client_series 


def getUserReport(driver):

    return
