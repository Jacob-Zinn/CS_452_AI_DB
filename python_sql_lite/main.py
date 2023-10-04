import sqlite3
import pandas as pd

# Read the dataset using pandas
df = pd.read_excel("Online Retail.xlsx", engine='openpyxl')

# Create SQLite connection and cursor
conn = sqlite3.connect('online_retail.db')
cursor = conn.cursor()

# Create tables

# 1. Products table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Products (
        StockCode TEXT PRIMARY KEY,
        Description TEXT
    )
""")

# Insert data into Products table
products = df[['StockCode', 'Description']].drop_duplicates().dropna()
products.to_sql('Products', conn, if_exists='replace', index=False)

# 2. Customers table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Customers (
        CustomerID INTEGER PRIMARY KEY,
        Country TEXT
    )
""")

# Insert data into Customers table
customers = df[['CustomerID', 'Country']].drop_duplicates().dropna()
customers.to_sql('Customers', conn, if_exists='replace', index=False)






# 2. Countries table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Countries (
        CountryID INTEGER PRIMARY KEY AUTOINCREMENT,
        CountryName TEXT UNIQUE
    )
""")

# Insert data into Countries table
countries = df[['Country']].drop_duplicates().dropna()
countries.to_sql('Countries', conn, if_exists='replace', index=False)

# 3. Customers table (modified to refer to Countries table)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Customers (
        CustomerID INTEGER PRIMARY KEY,
        CountryID INTEGER,
        FOREIGN KEY (CountryID) REFERENCES Countries(CountryID)
    )
""")

# Modify the customers dataframe to store CountryID instead of CountryName
df = df.merge(countries.reset_index(), left_on='Country', right_on='CountryName', how='left')
customers = df[['CustomerID', 'index']].drop_duplicates().dropna().rename(columns={'index': 'CountryID'})
customers.to_sql('Customers', conn, if_exists='replace', index=False)

# 4. Invoices table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Invoices (
        InvoiceNo TEXT PRIMARY KEY,
        InvoiceDate TEXT,
        CustomerID INTEGER,
        FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
    )
""")

# Insert data into Invoices table
invoices = df[['InvoiceNo', 'InvoiceDate', 'CustomerID']].drop_duplicates().dropna()
invoices.to_sql('Invoices', conn, if_exists='replace', index=False)

# 5. Transactions table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Transactions (
        TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
        InvoiceNo TEXT,
        StockCode TEXT,
        Quantity INTEGER,
        UnitPrice REAL,
        TotalPrice REAL AS (Quantity * UnitPrice),
        TransactionDate TEXT,
        FOREIGN KEY (InvoiceNo) REFERENCES Invoices(InvoiceNo),
        FOREIGN KEY (StockCode) REFERENCES Products(StockCode)
    )
""")

# Insert data into Transactions table
transactions = df[['InvoiceNo', 'StockCode', 'Quantity', 'UnitPrice', 'InvoiceDate']]
transactions.to_sql('Transactions', conn, if_exists='replace', index=False)




# Remember to commit the changes and close the connection
conn.commit()
conn.close()
