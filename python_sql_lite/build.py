import os

import openpyxl as openpyxl
import pandas as pd
from db import create_table, create_connection
from schema import (sql_create_countries_table, sql_create_customers_table,
                    sql_create_invoices_table, sql_create_transactions_table, sql_create_products_table)


def select_all_from_products(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Products")
    rows = cur.fetchall()

    for row in rows:
        print(row)


def insert_to_countries(conn):
    df = pd.read_csv("Online Retail.csv").head(20)
    countries = df[['Country']].drop_duplicates().dropna()

    for country in countries['Country'].tolist():
        sql = ''' INSERT OR IGNORE INTO Countries(CountryName) VALUES(?) '''
        cur = conn.cursor()
        cur.execute(sql, (country,))
    conn.commit()


def insert_to_customers(conn):
    df = pd.read_csv("Online Retail.csv").head(20)
    customers = df[['CustomerID', 'Country']].drop_duplicates().dropna()

    for _, row in customers.iterrows():
        sql = ''' INSERT INTO Customers(CustomerID, CountryID)
                  VALUES(?, (SELECT CountryID FROM Countries WHERE CountryName = ?)) '''
        cur = conn.cursor()
        cur.execute(sql, (row['CustomerID'], row['Country']))
    conn.commit()


def insert_to_invoices(conn):
    df = pd.read_csv("Online Retail.csv").head(20)
    invoices = df[['InvoiceNo', 'InvoiceDate', 'CustomerID']].drop_duplicates().dropna()

    for _, row in invoices.iterrows():
        sql = ''' INSERT INTO Invoices(InvoiceNo, InvoiceDate, CustomerID) VALUES(?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, (row['InvoiceNo'], row['InvoiceDate'], row['CustomerID']))
    conn.commit()


def insert_to_transactions(conn):
    df = pd.read_csv("Online Retail.csv").head(20)
    transactions = df[['InvoiceNo', 'StockCode', 'Quantity', 'UnitPrice', 'InvoiceDate']]

    for _, row in transactions.iterrows():
        # total_price = row['Quantity'] * row['UnitPrice']
        sql = ''' INSERT INTO Transactions(InvoiceNo, StockCode, Quantity, UnitPrice, TransactionDate) 
                  VALUES(?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, (row['InvoiceNo'], row['StockCode'], row['Quantity'], row['UnitPrice'], row['InvoiceDate']))
    conn.commit()


def insert_to_products(conn):
    df = pd.read_csv("Online Retail.csv").head(20)
    products = df[['StockCode', 'Description']].drop_duplicates().dropna()

    for _, row in products.iterrows():
        sql = ''' INSERT INTO Products(StockCode, Description) VALUES(?,?) '''
        cur = conn.cursor()
        cur.execute(sql, (row['StockCode'], row['Description']))
    conn.commit()


def main():
    # delete pythonsqlite.db if exists
    database = './pythonsqlite.db'
    if os.path.exists(database):
        os.remove(database)
        print(f"'{database}' has been deleted!")

    conn = create_connection(database)

    create_table(conn, sql_create_countries_table)
    insert_to_countries(conn)

    create_table(conn, sql_create_customers_table)
    insert_to_customers(conn)

    create_table(conn, sql_create_invoices_table)
    insert_to_invoices(conn)

    create_table(conn, sql_create_transactions_table)
    insert_to_transactions(conn)

    create_table(conn, sql_create_products_table)
    insert_to_products(conn)

    print("Database build successful!")


if __name__ == "__main__":
    main()
