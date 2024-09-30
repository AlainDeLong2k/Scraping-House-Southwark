# Scraping House Southwark

## Introduction  

**Scraping House Southwark** is a data scraping project aimed at collecting information about house prices in the Southwark area of London from the website [Rightmove](https://www.rightmove.co.uk/house-prices/southwark-85215.html?soldIn=5&page=1). This project will gather data from the past 5 years and navigate through each page to scrape all relevant information.  

## Objectives  

- Scrape house sale data in the Southwark area from 2018 to the present.  
- Provide detailed information about pricing trends in the Southwark area.  

## Information from Rightmove  

### House Prices in Southwark  

- **Overall average price in the last year**: £739,058  
- **Property types**:  
  - **Flats**: £708,999  
  - **Terraced houses**: £1,182,070  
  - **Semi-detached houses**: £1,525,000  

- **Price fluctuations**:  
  - Prices are down 12% compared to the previous year.  
  - Prices are down 43% from the 2019 peak of £1,289,339.  

## Technologies Used  

- Python  
- Scrapy  

## Storing Data in SQLite  

Once the data scraping is complete, the gathered information will be stored in a SQLite database. This will include two tables: one for a list of houses that have been sold, and another for the sales history of each house.  

### Table Definitions  

1. **houses_list**: This table will store information about each house that has been sold.  

    ```sql  
    CREATE TABLE IF NOT EXISTS houses_list (  
        id INTEGER PRIMARY KEY,  
        address TEXT,  
        description VARCHAR(255),  
        longitude REAL,  
        latitude REAL,  
        url TEXT  
    )  
    ```  

    - **id**: Unique identifier for each house (Primary Key).  
    - **address**: The address of the house.  
    - **description**: A brief description of the house.  
    - **longitude**: The geographical longitude of the house.  
    - **latitude**: The geographical latitude of the house.  
    - **url**: The URL where more information about the house can be found.  

2. **house_sales**: This table will keep track of the sales history for each house.  

    ```sql  
    CREATE TABLE IF NOT EXISTS house_sales (  
        id INTEGER PRIMARY KEY AUTOINCREMENT,  
        house_id INTEGER,  
        display_price REAL,  
        date_sold DATE,  
        tenure VARCHAR(255),  
        new_build INTEGER,  
        FOREIGN KEY(house_id) REFERENCES houses_list(id)  
    )  
    ```  

    - **id**: Unique identifier for each sale (Primary Key).  
    - **house_id**: References the id of the house from the `houses_list` table.  
    - **display_price**: The sale price of the house.  
    - **date_sold**: The date when the house was sold.  
    - **tenure**: Describes the type of ownership (e.g., freehold, leasehold).  
    - **new_build**: Indicates whether the house is a new build (1 for yes, 0 for no).  

### Implementation Steps  

To implement this, you will:  

1. Establish a connection to the SQLite database.  
2. Create the tables using the SQL commands provided above if they do not already exist.  
3. Insert the scraped data into the appropriate tables after each scrape.  

This structured storage in SQLite will allow for easy querying and analysis of the housing data collected over the past 5 years.
