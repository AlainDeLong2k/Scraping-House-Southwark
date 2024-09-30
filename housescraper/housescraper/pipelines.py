# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
from datetime import datetime


class HousescraperPipeline:
    def process_item(self, item, spider):
        return item


class SaveToSQLitePipeline:
    def __init__(self):
        ## Create cursor, used to execute commands
        self.connect = sqlite3.connect("demo.db")
        self.cursor = self.connect.cursor()
        self.id: int = 0
        self.create_tables()

    def create_tables(self):
        ## Create houses list table if none exists
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS houses_list(
                id INTEGER PRIMARY KEY,
                address TEXT,
                description VARCHAR(255),
                longitude REAL,
                latitude REAL,
                url TEXT
            )
            """
        )

        ## Create house sales table if none exists
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS house_sales(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                house_id INTEGER,
                display_price REAL,
                date_sold DATE,
                tenure VARCHAR(255),
                new_build INTEGER,
                FOREIGN KEY(house_id) REFERENCES houses_list(id)
            )
            """
        )

    def process_item(self, item, spider):
        ## Define insert statement
        self.id += 1
        self.cursor.execute(
            """
            INSERT INTO houses_list VALUES(?, ?, ?, ?, ?, ?)
            """,
            (
                self.id,
                item["address"],
                item["description"],
                item["location"]["lng"],
                item["location"]["lat"],
                item["url"],
            ),
        )

        for transaction in item["transactions"]:
            price = transaction["displayPrice"].replace("£", "")
            price = price.replace(",", "")
            price = float(price)

            date = transaction["dateSold"]
            date_obj = datetime.strptime(date, "%d %b %Y")
            formatted_date = date_obj.strftime("%d-%m-%Y")

            new_build = 1 if transaction["newBuild"] else 0

            self.cursor.execute(
                """
                INSERT INTO house_sales (house_id, display_price, date_sold, tenure, new_build) VALUES (?, ?, ?, ?, ?)
                """,
                (self.id, price, formatted_date, transaction["tenure"], new_build),
            )

        ## Execute insert of data into database
        self.connect.commit()
        return item

    def close_spider(self, spider):
        ## Close cursor & connection to database
        self.cursor.close()
        self.connect.close()
