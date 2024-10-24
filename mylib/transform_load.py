"""
Transforms and Loads data into the Databricks database
"""
import os
import csv
from dotenv import load_dotenv
from databricks import sql

def load(dataset="../data/titanic.csv"):
    """Transforms and Loads Titanic data into the Databricks database"""

    # Load environment variables from .env file
    load_dotenv()
    server_hostname = os.getenv("SERVER_HOSTNAME")
    http_path = os.getenv("HTTP_PATH")
    access_token = os.getenv("DATABRICKS_KEY")
    
    # Connect to Databricks SQL
    with sql.connect(
        server_hostname=server_hostname,
        http_path=http_path,
        access_token=access_token,
    ) as connection:
        c = connection.cursor()
        
        # Check and create table for Titanic if it doesn't exist
        c.execute("SHOW TABLES IN default LIKE 'Titanic'")
        result = c.fetchall()
        if not result:
            c.execute(
                """
                CREATE TABLE default.Titanic (
                    PassengerId INTEGER,
                    Survived INTEGER,
                    Pclass INTEGER,
                    Name STRING,
                    Sex STRING,
                    Age DOUBLE,
                    SibSp INTEGER,
                    Parch INTEGER,
                    Ticket STRING,
                    Fare DOUBLE,
                    Cabin STRING,
                    Embarked STRING
                )
                """
            )

        # Prepare data for insertion from CSV
        data_to_insert = []
        with open(dataset, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data_to_insert.append((
                    int(row['PassengerId']),
                    int(row['Survived']),
                    int(row['Pclass']),
                    row['Name'],
                    row['Sex'],
                    float(row['Age']) if row['Age'] else None,
                    int(row['SibSp']),
                    int(row['Parch']),
                    row['Ticket'],
                    float(row['Fare']),
                    row['Cabin'],
                    row['Embarked']
                ))

        # Insert data in bulk for efficiency
        insert_query = """
            INSERT INTO default.Titanic 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        c.executemany(insert_query, data_to_insert)

    return "Success: Data Loaded into Databricks"


if __name__ == "__main__":
    load()
