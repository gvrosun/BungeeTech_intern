import pandas as pd
import os

# Locating required file paths
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(BASE_PATH, 'input/main.csv')
OUTPUT_PATH_FILTERED = os.path.join(BASE_PATH, 'output/filteredCountry.csv')
OUTPUT_PATH_PRICE = os.path.join(BASE_PATH, 'output/lowestPrice.csv')


# Checking input file exists and read data
def fetch_input_data(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        print(f'File: {path} not found!', 'exiting...')
        exit()


def filter_countries(file_path, country_name):
    input_df = fetch_input_data(file_path)
    return input_df[input_df.COUNTRY.str.contains(country_name)]


def filter_price(file_path):
    input_df = fetch_input_data(file_path)
    price_data = pd.DataFrame(columns=[
        'SKU',
        'FIRST_MINIMUM_PRICE',
        'SECOND_MINIMUM_PRICE'])
    return input_df


# Filter rows contains the word 'USA'
filtered_df = filter_countries(INPUT_PATH, 'USA')
filtered_df.to_csv(OUTPUT_PATH_FILTERED)

# Filter rows by price
price_df = filter_price(OUTPUT_PATH_FILTERED)
price_df.to_csv(OUTPUT_PATH_PRICE)
