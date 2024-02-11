# Usage instructions

## Prerequisites

-   Python 3.x
-   Docker

## Setting up the db

0. The PostgreSQL database is run in a docker container. docker-compose is used to declaratively define and run the database.
1. Run `docker-compose up` in the root directory of the project to start the database.
2. The database is exposed on local port 5432, with the username and password set to `postgres`.
3. Connect to the database using `psql` command-line tool or database management tool of your choice. Example: `psql -h localhost -U postgres -d players`
4. Run the queries in the schema.sql file to create the schema.

## Running the application

1. Run `pip install -r requirements.txt` to install the required packages. Optionally you can do this inside of a virtual environment.
2. Run `python import_data.py <path_to_player_data_csv_file>` to import the data from the csv file into the database.
3. Run `python main.py <path_to_player_urls_file> <output_file>` to scrape the player data from the urls in the file and write the output to the specified file.

## Checking the output

1. An output csv file is generated that contains the scraped data.
2. The data was also inserted into the database. You can query the database to check the data. Use the queries from the queries.sql file.
