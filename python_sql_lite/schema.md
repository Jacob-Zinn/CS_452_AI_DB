---

### Countries Table

| Field Name  | Data Type | Key        | Constraints |
|-------------|-----------|------------|-------------|
| CountryID   | INTEGER   | PRIMARY KEY| AUTOINCREMENT |
| CountryName | TEXT      |            | UNIQUE      |

---

### Customers Table

| Field Name  | Data Type | Key        | Constraints                                  |
|-------------|-----------|------------|----------------------------------------------|
| CustomerID  | INTEGER   | PRIMARY KEY|                                              |
| CountryID   | INTEGER   | FOREIGN KEY| REFERENCES Countries(CountryID)              |

---

### Invoices Table

| Field Name   | Data Type | Key        | Constraints                                  |
|--------------|-----------|------------|----------------------------------------------|
| InvoiceNo    | TEXT      | PRIMARY KEY|                                              |
| InvoiceDate  | DATE      |            |                                              |
| CustomerID   | INTEGER   | FOREIGN KEY| REFERENCES Customers(CustomerID)             |

---

### Products Table

| Field Name   | Data Type | Key        | Constraints |
|--------------|-----------|------------|-------------|
| ProductID    | INTEGER   | PRIMARY KEY| AUTOINCREMENT |
| StockCode    | TEXT      |            |             |
| Description  | TEXT      |            |             |

---

### Transactions Table

| Field Name     | Data Type | Key        | Constraints                                     |
|----------------|-----------|------------|-------------------------------------------------|
| TransactionID  | INTEGER   | PRIMARY KEY| AUTOINCREMENT                                   |
| InvoiceNo      | TEXT      | FOREIGN KEY| REFERENCES Invoices(InvoiceNo)                  |
| ProductID      | INTEGER   | FOREIGN KEY| REFERENCES Products(ProductID)                  |
| Quantity       | INTEGER   |            |                                                 |
| UnitPrice      | REAL      |            |                                                 |
| TotalPrice     | REAL      |            | AS (Quantity * UnitPrice)                       |
| TransactionDate| DATE      |            |                                                 |

---