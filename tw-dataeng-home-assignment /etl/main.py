from extract import extract_data
from transform import transform_data
import psycopg2
import argparse

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
    table_name = 'user_activity'
    #create table
    create_table_sql = f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
        user_id STRING PRIMARY KEY,
        top_workspace STRING,
        longest_streak INTEGER
    )
'''


    cursor.execute(create_table_sql)

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