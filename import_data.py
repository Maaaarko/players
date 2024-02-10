import csv
import os
import sys

from dateutil.parser import parse as date_parse

import psycopg2

from queries import INSERT_PLAYER_INFO


def get_players_data(file_path):
    with open(file_path, "r", encoding="utf-8-sig") as f:
        csv_reader = csv.DictReader(f, delimiter=";")
        yield from csv_reader


def clean_data(player_data):
    player_data["Position"] = player_data["Position"].split(", ")
    for key in player_data:
        if player_data[key] == "":
            player_data[key] = None
    if player_data["Date of birth"]:
        player_data["Date of birth"] = date_parse(player_data["Date of birth"]).date()
    if not player_data["Full name"]:
        player_data["Full name"] = player_data["Name"]
    return player_data


def transform_keys(player_data):
    return {
        "id": player_data["PlayerID"],
        "url": player_data["URL"],
        "name": player_data["Name"],
        "full_name": player_data["Full name"],
        "date_of_birth": player_data["Date of birth"],
        "age": player_data["Age"],
        "place_of_birth": player_data["City of birth"],
        "country_of_birth": player_data["Country of birth"],
        "positions": player_data["Position"],
        "current_club": player_data["Current club"],
        "national_team": player_data["National_team"],
        "appearances_in_current_club": None,
        "goals_in_current_club": None,
        "timestamp": None,
    }


def start_process():
    db_connection_string = "host=localhost dbname=players user=postgres password=postgres"  # hardcoded for simplicity
    connection = psycopg2.connect(dsn=db_connection_string)
    cursor = connection.cursor()

    for raw_player_data in get_players_data(file_path):
        if not raw_player_data["Name"]:
            continue
        player_data = transform_keys(clean_data(raw_player_data))
        try:
            cursor.execute(INSERT_PLAYER_INFO, player_data)
            connection.commit()
        except Exception as e:
            print(f"Error inserting player info: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: import_data.py <file_path>")
        sys.exit(1)
    file_path = sys.argv[1]
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)
    start_process()
