# Run this file before executing main.py!
# This runs all the SQL commands in company.sql to correctly configure "company.db"

import sqlite3 

def convert_sql_to_db(sql_file, db_file):
    # connect to sqlite database
    connect = sqlite3.connect(db_file)
    cursor = connect.cursor()

    # read content of sql file
    with open(sql_file, "r") as file:
        sql_commands = file.read()

    # execute sql commands
    cursor.executescript(sql_commands)

    # commit and close connections 
    connect.commit() 
    connect.close() 

if __name__ == "__main__":
    sql_file_path = "./company.sql"
    db_file_path = "./company.db"

    convert_sql_to_db(sql_file_path, db_file_path)

    print("converted sql file to db file")
