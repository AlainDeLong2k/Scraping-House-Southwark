# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
from datetime import datetime


# def convert_month(month):
#     if month=='Jan':
#         return


class HousescraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        ## Remove currency and convert price to float
        print("***********")
        transactions = adapter.get("transactions")
        for transaction in transactions:
            value = transaction["displayPrice"].replace("£", "")
            value = value.replace(",", "")
            value = float(value)
            date = transaction["dateSold"]
            date_obj = datetime.strptime(date, "%d %b %Y")
            formatted_date = date_obj.strftime("%d-%m-%Y")
            print(formatted_date)
            print(value)
        print("***********")

        ## Change to format DD-MM-YYYY


class SaveToSQLitePipeline:
    def __init__(self):
        self.connect = sqlite3.connect("demo.db")
        self.cursor = self.connect.cursor()
        self.id: int = 0
        self.create_tables()

    def create_tables(self):
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

        self.cursor.execute(
            """
            CREATE TABLE house_sales(
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
        self.id += 1
        print(self.id)
        ## Define insert statement
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
        self.cursor.close()
        self.connect.close()
