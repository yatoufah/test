# Oveview
 
&nbsp;&nbsp;&nbsp;&nbsp;This project is a project to do a simple ETL. This project include these tech:

1. Python programming language
2. Docker
3. PostgreSQL

- [data dir](/data/activity.csv): contains all the data that is already downloaded 
- [etl dir](/etl): contains all python scripts that is used to do ETL

# ETL (Extract, Transfrom and Load)

&nbsp;&nbsp;&nbsp;&nbsp;This is the step of ETL that I used:

1. Extract (extract.py)

&nbsp;&nbsp;&nbsp;&nbsp;Extract stage is used to extract data from data sources. Because in this database we only have one format of data, therefore I only use pandas library to extract data from csv into data frame and return that data frame. Note that the file path is at my local machine. 

2. Transform (transform.py)

&nbsp;&nbsp;&nbsp;&nbsp;In this transform stage, I used python to transform data to what I need, what I did is:

    - Convert 'active_date' column to datetime
    - Calculate the longest streak for each user
    - Find the top workspace for each user
    - Calculate the longest streak for each user. Then merge the top workspace and longest streak data. 
    

3. Load (main.py)

&nbsp;&nbsp;&nbsp;&nbsp;Load stage is used to load the data that has been transformed to the data warehouse or database. In this case I used PostgreSQL with docker image that I will explain more later in docker section. I used psycopg2 to help me connect python with PostgreSQL. Not just that, I also used argparse to help me create command arguments in python therefore, I can input csv file, database name, host name, username, password, and port of PostgreSQL flexibly. At the end, we have the table in the step transform to populate into the PostgresSQL warehouse. 

4. Test dataset (test.py)
&nbsp;&nbsp;&nbsp;&nbsp; At the stage, we want to add an integration test to the project that runs the ETL pipeline using the given sample input
  file `data/activity.csv` and writes it to PostgreSQL. Assert values of `longest_streak` and `top_workspace` for `user_id=5bfd0e8d472bcf0009a1014d`. So I prepare a copy of the main.py to test.py which populate the user_activity_test table into PostgresSQL warehouse.
In the other hand, I also tried another way, that write the result of the target SQL query to PostgreSQL using the psql command within a Docker container from command line. Follow the step 13 below, inside the pgcli prompt, you can run your SQL query and write the query result to a file named "output.txt"

# How To Use

1. Clone this repository
2. Create volume name **etl_activity** with this command ```docker volume create etl_activity``
3. PostgreSQL using this path to save their data in docker */var/lib/postgresql/data*. Therefore if you want to use volume then the path of your volume will be like this ```[your volume name]:/var/lib/postgresql/data```. So the volume will be like this ```etl_activity:/var/lib/postgresql``` 
4. Pull postgres image from docker using this command line ```docker pull postgres```
5. create network for docker by using this command line ```docker network create activity_network```
6. Pull pgadmin in docker using this command line ```docker pull dpage/pgadmin4```
7. Run docker compose using this command line ```docker-compose up -d```

```
NOTE:
If you want to connect docker with network you cannot used localhost, but you have to see the IP of the connection using:

docker network inspect [network name]

Then you will see the IP of the connection

or you can just use name of the container to connect each container
```


8. install pgcli to see your PostgreSQL from command line ```pip install pgcli```
9. Run this to access PostgreSQL from command line ```pgcli -h localhost -p 5432 -u postgres -d activity```
10. Build image for our etl script by running this command ```docker build -t python-etl .```
11. Go to [etl dir](/etl) and run 
```
docker run -it --network=activity_network python-etl -f [file-path] -db activity -hs localhost -u postgres -pass 123456 -p 5432
```
12. Then ETL process will completed 
13. To write the result of an SQL query to PostgreSQL using the psql command within a Docker container from command line, inside the pgcli prompt, you can run your SQL query and write the query result to a file named "output.txt," :

```
\o output.txt
SELECT * FROM user_activity where user_id = '5bfd0e8d472bcf0009a1014d';
\o ```
