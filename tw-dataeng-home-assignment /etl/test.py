import pandas as pd
import psycopg2
from extract import extract_data
from transform import transform_data

import argparse

# Define the user_id for testing
TEST_USER_ID = '5bfd0e8d472bcf0009a1014d'


def load_data(file_path):
    
    connection = psycopg2.connect(database="activity",
                        host="localhost",
                        user="postgres",
                        password="123456",
                        port="5432")

    cursor = connection.cursor()

    print("loading data...")
    data = extract_data(file_path)

    print("transforming data...")
    data_transform = transform_data(data)
    

    # column_name = data_transform.columns[-1]
    table_name = 'user_activity_test'
    #create table
    query = f'''
    CREATE TABLE  {table_name} AS 
    SELECT user_id, top_workspace, longest_streak FROM user_activity WHERE user_id = '{TEST_USER_ID} '''


    cursor.execute(query)

    #start loading data
    print('loading data...')
    for index, row in data_transform.iterrows():
        query_insert_value = f"INSERT INTO {table_name}(user_id,top_workspace,longest_streak)VALUES(%s,%s,%s)"
        
        cursor.execute(query_insert_value)
    connection.commit()

    cursor.close()
    connection.close()

    print("etl success...\n")

    return "all processes completed"

if __name__ == "__main__":

    # Initialize parser
    parser = argparse.ArgumentParser()
    
    # Adding optional argument
    parser.add_argument("-f", "--file", help = "file path of the dataset")
    
    # Read arguments from command line
    args = parser.parse_args()

    load_data(args.file)