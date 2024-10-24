from mylib.extract import extract
from mylib.transform_load import load
from mylib.query import query


def main():
    # Extract the dataset
    print("Extracting data...")
    dataset_path = extract()  # Extract and get the dataset path

    # Load the dataset into Databricks
    print("Transforming and loading data into Databricks...")
    load_status = load(dataset_path)
    print(load_status)

    # Perform queries on the loaded data
    print("\nPerforming queries and generating log.md...")
    query()
    print("Queries executed successfully. Check log.md for results.")


if __name__ == "__main__":
    main()
