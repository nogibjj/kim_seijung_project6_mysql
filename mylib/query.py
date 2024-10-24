"""Query the Titanic dataset in Databricks and generate a log.md file"""

import logging
import os
from dotenv import load_dotenv
from databricks import sql

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TitanicQuery")

# Function to load environment variables
def get_env_variables():
    """Load environment variables from .env file and return them"""
    load_dotenv()  # Load environment variables from .env file
    server_hostname = os.getenv("SERVER_HOSTNAME")
    http_path = os.getenv("HTTP_PATH")
    access_token = os.getenv("DATABRICKS_KEY")

    if not (server_hostname and http_path and access_token):
        raise ValueError("One or more required environment variables are missing.")
    
    return server_hostname, access_token, http_path

# SQL Queries
JOIN_QUERY = """
    SELECT 
        t.PassengerId, t.Name, t.Sex, t.Age, t.Embarked, 
        p.PortName, p.Country
    FROM default.Titanic t
    JOIN default.Ports p 
    ON t.Embarked = p.PortCode;
"""

AGGREGATE_QUERY = """
    SELECT Pclass, AVG(Age) AS AverageAge
    FROM default.Titanic
    GROUP BY Pclass;
"""

SORT_QUERY = """
    SELECT PassengerId, Name, Fare
    FROM default.Titanic
    ORDER BY Fare DESC;
"""

# Function to execute SQL queries
def execute_query(query):
    """Executes a SQL query on the Databricks database"""
    hostname, access_token, http_path = get_env_variables()
    
    try:
        with sql.connect(
            server_hostname=hostname,
            http_path=http_path,
            access_token=access_token,
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                logger.info("Query executed successfully.")
                return result
    except sql.DatabaseError as db_err:
        logger.error(f"Database error occurred: {db_err}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    
    return None

# Function to write results to a Markdown file
def write_to_markdown(query_name, results, columns):
    """Writes query results to a Markdown file"""
    with open("log.md", "a") as log_file:
        log_file.write(f"## {query_name}\n\n")
        log_file.write(f"| {' | '.join(columns)} |\n")
        separator = "|".join(['-' * (len(col) + 2) for col in columns])
        log_file.write(f"|{separator}|\n")
        
        for row in results:
            formatted_row = " | ".join(
                [str(item) if item is not None else "NULL" for item in row]
            )
            log_file.write(f"| {formatted_row} |\n")
        
        log_file.write("\n")

# Main function to demonstrate query execution
def query():
    """Execute all SQL queries for the Titanic dataset and log results"""

    # Remove existing log.md file if exists
    if os.path.exists("log.md"):
        os.remove("log.md")

    # Perform JOIN query
    logger.info("Performing JOIN query on Titanic and Ports tables...")
    join_result = execute_query(JOIN_QUERY)
    if join_result:
        write_to_markdown(
            "JOIN Query Result",
            join_result,
            ["PassengerId", "Name", "Sex", "Age", "Embarked", "PortName", "Country"]
        )

    # Perform AGGREGATE query
    logger.info("Performing AGGREGATE query on Titanic table...")
    aggregate_result = execute_query(AGGREGATE_QUERY)
    if aggregate_result:
        write_to_markdown(
            "AGGREGATE Query Result",
            aggregate_result,
            ["Pclass", "AverageAge"]
        )

    # Perform SORT query
    logger.info("Performing SORT query on Titanic table...")
    sort_result = execute_query(SORT_QUERY)
    if sort_result:
        write_to_markdown(
            "SORT Query Result",
            sort_result,
            ["PassengerId", "Name", "Fare"]
        )

if __name__ == "__main__":
    query()
