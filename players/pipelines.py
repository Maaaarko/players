import csv
import uuid

import psycopg2

from itemadapter import ItemAdapter

from queries import INSERT_PLAYER_INFO


class PlayersPipeline:
    db_connection_string = None
    output_file_path = None
    connection = None
    cursor = None
    csv_file = None
    csv_writer = None

    def __init__(self, db_connection_string, output_file_path):
        self.db_connection_string = db_connection_string
        self.output_file_path = output_file_path

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_connection_string=crawler.settings.get("DB_CONNECTION_STRING"),
            output_file_path=crawler.settings.get("OUTPUT_FILE"),
        )

    def open_spider(self, spider):
        self.connection = psycopg2.connect(dsn=self.db_connection_string)
        self.cursor = self.connection.cursor()

        file = open(self.output_file_path, "w")
        csv_writer = csv.DictWriter(
            file,
            fieldnames=[
                "id",
                "url",
                "name",
                "full_name",
                "dob",
                "age",
                "place_of_birth",
                "country_of_birth",
                "positions",
                "current_club",
                "national_team",
                "appearances",
                "goals",
                "timestamp",
            ],
            delimiter=";",
        )
        csv_writer.writeheader()

        self.csv_file = file
        self.csv_writer = csv_writer

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()
        self.csv_file.close()

    def process_item(self, item, spider):
        player_id = uuid.uuid5(uuid.NAMESPACE_URL, item["url"])
        item["id"] = str(player_id)
        self.save_to_csv(item)
        self.save_to_db(item)
        return item

    def save_to_db(self, item):
        try:
            self.cursor.execute(INSERT_PLAYER_INFO, item)
            self.connection.commit()
        except Exception as e:
            print(f"Error inserting player info: {e}")

    def save_to_csv(self, item):
        self.csv_writer.writerow(ItemAdapter(item).asdict())
        self.csv_file.flush()
