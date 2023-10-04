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
        InvoiceDate DATE,
        CustomerID INTEGER,
        FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
    );
"""

sql_create_products_table = """
    CREATE TABLE IF NOT EXISTS Products (
        ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
        StockCode TEXT,
        Description TEXT
    );
"""

sql_create_transactions_table = """
    CREATE TABLE IF NOT EXISTS Transactions (
        TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
        InvoiceNo TEXT,
        ProductID INTEGER,
        Quantity INTEGER,
        UnitPrice REAL,
        TotalPrice REAL AS (Quantity * UnitPrice),
        TransactionDate DATE,
        FOREIGN KEY (InvoiceNo) REFERENCES Invoices(InvoiceNo),
        FOREIGN KEY (ProductID) REFERENCES Products(ProductID) 
    );
"""

def get_schema():
    schema = f"{sql_create_countries_table}{sql_create_customers_table}{sql_create_invoices_table}{sql_create_products_table}{sql_create_transactions_table}"
    return schema
