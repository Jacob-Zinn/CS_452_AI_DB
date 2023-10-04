import os
import pandas as pd
from db import create_table, create_connection
from schema import (sql_create_countries_table, sql_create_customers_table,
                    sql_create_invoices_table, sql_create_transactions_table, sql_create_products_table)



from datetime import datetime

SAMPLE_DATA_SIZE = 15

def convert_to_date_format(date_string):
    return datetime.strptime(date_string, "%m/%d/%y %H:%M").strftime('%Y-%m-%d')


def insert_to_countries(conn):
    df = pd.read_csv("online_retail.csv").head(SAMPLE_DATA_SIZE)
    countries = df[['Country']].drop_duplicates().dropna()

    for country in countries['Country'].tolist():
        sql = ''' INSERT OR IGNORE INTO Countries(CountryName) VALUES(?) '''
        cur = conn.cursor()
        cur.execute(sql, (country,))
    conn.commit()


def insert_to_customers(conn):
    df = pd.read_csv("online_retail.csv").head(SAMPLE_DATA_SIZE)
    customers = df[['CustomerID', 'Country']].drop_duplicates().dropna()

    for _, row in customers.iterrows():
        sql = ''' INSERT INTO Customers(CustomerID, CountryID)
                  VALUES(?, (SELECT CountryID FROM Countries WHERE CountryName = ?)) '''
        cur = conn.cursor()
        cur.execute(sql, (row['CustomerID'], row['Country']))
    conn.commit()


def insert_to_invoices(conn):
    df = pd.read_csv("online_retail.csv").head(SAMPLE_DATA_SIZE)
    invoices = df[['InvoiceNo', 'InvoiceDate', 'CustomerID']].drop_duplicates().dropna()

    for _, row in invoices.iterrows():
        sql = ''' INSERT INTO Invoices(InvoiceNo, InvoiceDate, CustomerID) VALUES(?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, (row['InvoiceNo'], row['InvoiceDate'], row['CustomerID']))
    conn.commit()


def insert_to_products(conn):
    df = pd.read_csv("online_retail.csv").head(SAMPLE_DATA_SIZE)
    products = df[['StockCode', 'Description']].drop_duplicates().dropna()

    for _, row in products.iterrows():
        sql = ''' INSERT INTO Products(StockCode, Description) VALUES(?,?) '''
        cur = conn.cursor()
        cur.execute(sql, (row['StockCode'], row['Description']))
    conn.commit()


def insert_to_transactions(conn):
    df = pd.read_csv("online_retail.csv").head(SAMPLE_DATA_SIZE)
    transactions = df[['InvoiceNo', 'StockCode', 'Quantity', 'UnitPrice', 'InvoiceDate']]

    for _, row in transactions.iterrows():
        # Convert InvoiceDate to SQL date format
        formatted_date = convert_to_date_format(row['InvoiceDate'])

        # Linking to ProductID based on StockCode
        sql = ''' INSERT INTO Transactions(InvoiceNo, ProductID, Quantity, UnitPrice, TransactionDate) 
                  VALUES(?, (SELECT ProductID FROM Products WHERE StockCode = ?),?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, (row['InvoiceNo'], row['StockCode'], row['Quantity'], row['UnitPrice'], formatted_date))
    conn.commit()


def main():
    # delete pythonsqlite.db if exists
    database = './pythonsqlite.db'
    if os.path.exists(database):
        os.remove(database)
        print(f"'{database}' has been deleted!")

    conn = create_connection(database)

    # write dataset to sample database
    # Read the desired number of rows from the dataset
    df = pd.read_csv("online_retail.csv").head(SAMPLE_DATA_SIZE)
    # Write the sampled dataframe to a new CSV file
    df.to_csv("sample_db.csv", index=False)

    create_table(conn, sql_create_countries_table)
    insert_to_countries(conn)

    create_table(conn, sql_create_customers_table)
    insert_to_customers(conn)

    create_table(conn, sql_create_invoices_table)
    insert_to_invoices(conn)

    create_table(conn, sql_create_products_table)
    insert_to_products(conn)

    create_table(conn, sql_create_transactions_table)
    insert_to_transactions(conn)

    print("Database build successful!")


if __name__ == "__main__":
    main()
