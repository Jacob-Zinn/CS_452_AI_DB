
---

### Database Schema

---

#### 1. **Countries**

| Field       | Type    | Description                                        |
|-------------|---------|----------------------------------------------------|
| `CountryID` | Integer | Primary Key, Auto-incremented. Unique ID for each country. |
| `CountryName` | Text  | Unique. Name of the country.                      |

---

#### 2. **Products**

| Field        | Type  | Description                                         |
|--------------|-------|-----------------------------------------------------|
| `StockCode`  | Text  | Primary Key. Unique code for each product.           |
| `Description`| Text  | Description or name of the product.                  |

---

#### 3. **Customers**

| Field        | Type    | Description                                         |
|--------------|---------|-----------------------------------------------------|
| `CustomerID` | Integer | Primary Key. Unique ID for each customer.            |
| `CountryID`  | Integer | Foreign Key referencing `Countries`. Country of the customer. |

---

#### 4. **Invoices**

| Field         | Type    | Description                                           |
|---------------|---------|-------------------------------------------------------|
| `InvoiceNo`   | Text    | Primary Key. Unique number for each invoice.           |
| `InvoiceDate` | Text    | Date of the invoice.                                   |
| `CustomerID`  | Integer | Foreign Key referencing `Customers`. Customer for the invoice. |

---

#### 5. **Transactions**

| Field           | Type    | Description                                         |
|-----------------|---------|-----------------------------------------------------|
| `TransactionID` | Integer | Primary Key, Auto-incremented. Unique ID for each transaction.|
| `InvoiceNo`     | Text    | Foreign Key referencing `Invoices`. Invoice number for the transaction.|
| `StockCode`     | Text    | Foreign Key referencing `Products`. Product code for the transaction.|
| `Quantity`      | Integer | Quantity of the product.                             |
| `UnitPrice`     | Real    | Price per unit of the product.                       |
| `TotalPrice`    | Real    | Calculated as `Quantity * UnitPrice`. Total price of the transaction.|
| `TransactionDate`| Text   | Date of the transaction.                             |

---