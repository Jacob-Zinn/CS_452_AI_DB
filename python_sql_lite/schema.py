sql_create_countries_table = """
    CREATE TABLE IF NOT EXISTS Countries (
        CountryID INTEGER PRIMARY KEY AUTOINCREMENT,
        CountryName TEXT UNIQUE
    );
"""

sql_create_customers_table = """
    CREATE TABLE IF NOT EXISTS Customers (
        CustomerID INTEGER PRIMARY KEY,
        CountryID INTEGER,
        FOREIGN KEY (CountryID) REFERENCES Countries(CountryID)
    );
"""

sql_create_invoices_table = """
    CREATE TABLE IF NOT EXISTS Invoices (
        InvoiceNo TEXT PRIMARY KEY,
        InvoiceDate TEXT,
        CustomerID INTEGER,
        FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
    );
"""

sql_create_transactions_table = """
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
    );
"""

sql_create_products_table = """
    CREATE TABLE IF NOT EXISTS Products (
        StockCode TEXT PRIMARY KEY,
        Description TEXT
    );
"""

def get_schema():
    schema = f"{sql_create_countries_table}{sql_create_customers_table}{sql_create_invoices_table}{sql_create_transactions_table}{sql_create_products_table}"
    return schema
