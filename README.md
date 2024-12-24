# 
How to use for database connection string connection First step: first Insatll PostgreSQl Second step: set envirometal variables like
In order to connect database and retrieve data:
First Downlaod and install Postgres, Then set Environmental variables for windows Os as follows;

    C:\Program Files\PostgreSQL\17\bin
    C:\Users\Admin\AppData\Roaming\pgadmin4
    C:\Program Files\PostgreSQL\17\pgAdmin 4\python
    C:\Program Files\PostgreSQL\17\pgAdmin 4\web

    Then Restart your device 

Next: Open or track cmmand powershell on a folder that your sql databse file exist then first set password using the command
set PGPASSWORD =your password then dump or restore table and its data using the below command;
psql -U postgres -d telecome_db -f ./telecom.sql

Finnaly, connect the database to python script, for this use psycopg2-library. To use this first install using a pip install psycopg2-library or use pip install sqlalchemy then install the below package for .env or for connection string file loading pip install python-dotenv

For further liberary installation use requirements.txt