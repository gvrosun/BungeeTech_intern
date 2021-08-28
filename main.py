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


# Cleaning price data
def clean_data(item):
    if item[0] == "$":
        item = item[1:].replace(',', '')
    if item[-1] == "?":
        item = item[:-1].replace(',', '')

    # Checking if decimal value available
    float_data = float(item)
    if (float_data / int(float_data)) == 1.0:
        return int(float_data)
    else:
        return float_data


# Function to filter rows by country_name
def filter_countries(file_path, country_name):
    input_df = fetch_input_data(file_path)
    return input_df[input_df.COUNTRY.str.contains(country_name)]


# Function to find last 2 minimum price
def filter_price(file_path):
    input_df = fetch_input_data(file_path)

    # Creating new dataframe
    price_data = pd.DataFrame(columns=[
        'SKU',
        'FIRST_MINIMUM_PRICE',
        'SECOND_MINIMUM_PRICE'])

    grouped_df = input_df.groupby("SKU")    # Grouping data by SKU
    for item in grouped_df:
        clean_price = map(clean_data, item[1].PRICE)
        sorted_price = sorted(clean_price)

        if len(sorted_price) == 1:
            first_min = second_min = sorted_price[0]
        else:
            first_min, second_min = sorted_price[0:2]

        price_data = price_data.append(
            {'SKU': item[0],
             'FIRST_MINIMUM_PRICE': first_min,
             'SECOND_MINIMUM_PRICE': second_min
             },
            ignore_index=True)

    return price_data


# Filter rows contains the word 'USA'
filtered_df = filter_countries(INPUT_PATH, 'USA')
filtered_df.to_csv(OUTPUT_PATH_FILTERED, index=False)   # Store final data in CSV

# Filter rows by price
price_df = filter_price(OUTPUT_PATH_FILTERED)
price_df.to_csv(OUTPUT_PATH_PRICE, index=False)     # Store final data in CSV
