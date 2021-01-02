import sqlite3
import pandas as pd

class Database:
    def __init__(self, path="jobs.db"):
        self.create_connection(path)

    def create_connection(self, path):
        self.connection = None
        # This block is a way of testing connection to the database and allows us to control what happens if there is an error
        try:
            self.connection = sqlite3.connect(path)
            print("Connection to SQLite DB successful")
        except sqlite3.Error as e:
            print(f"The error '{e}' occurred")

    def run_query(self, query: str):
        if self.connection is None:
            raise "No connection to the database"
        return pd.read_sql_query(query, self.connection)

    def write_to_database(self, dataframe: pd.DataFrame, table_name = 'job_postings'):
        if self.connection is None:
            raise "No connection to the database"
        return dataframe.to_sql(table_name, self.connection, if_exists='replace', index=False)

def main():
    new_database = Database(path="jobs.db")
    print(new_database.run_query("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"))

if __name__ == "__main__":
    main()
