"""
Extract a dataset from a URL like Kaggle or data.gov.
JSON or CSV formats tend to work well.
"""
import os
import requests
import csv

# Extracts the Titanic dataset
def extract(
    url="https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv",
    file_path="../data/titanic.csv",
    lines_to_extract=200
):
    """Extract a dataset from a URL to a specified file path."""
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Make a GET request to the URL to fetch the dataset content
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful

    # Read the CSV content and write the first 200 lines to the output file
    with open(file_path, 'w', newline='', encoding='utf-8') as output_file:
        reader = csv.reader(response.text.splitlines())
        writer = csv.writer(output_file)
        
        # Write the header and first 199 lines of data
        for i, row in enumerate(reader):
            if i < lines_to_extract:
                writer.writerow(row)
            else:
                break

    return file_path

if __name__ == "__main__":
    extract()
