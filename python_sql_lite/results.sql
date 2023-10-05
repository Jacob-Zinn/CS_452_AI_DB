

-- QUESTION: Which country is responsible for purchasing the largest total quantity of items?
-- MODEL: gpt-3.5-turbo
SELECT c.CountryName, SUM(t.Quantity) AS TotalQuantity
FROM Countries c
JOIN Customers cu ON c.CountryID = cu.CountryID
JOIN Invoices i ON cu.CustomerID = i.CustomerID
JOIN Transactions t ON i.InvoiceNo = t.InvoiceNo
GROUP BY c.CountryName
ORDER BY TotalQuantity DESC
LIMIT 1;
-- RESULT: (Germany, 54) (correct)


-- QUESTION: Which country purchased the most items?
-- MODEL: gpt-3.5-turbo
SELECT c.CountryName, COUNT(t.TransactionID) AS TotalItemsPurchased
FROM Countries c
JOIN Customers cu ON c.CountryID = cu.CountryID
JOIN Invoices i ON cu.CustomerID = i.CustomerID
JOIN Transactions t ON i.InvoiceNo = t.InvoiceNo
GROUP BY c.CountryName
ORDER BY TotalItemsPurchased DESC
LIMIT 1;
-- RESULT: (United Kingdom, 6) (incorrect)
-- REASON FOR FAILURE: Chose to interpret "most items" as "transactions" instead of as the SUM of the quantities for each applicable transaction


-- THEN WE ASKED IT A HARDER, BUT SIMILAR, QUESTION


-- QUESTION: Which country purchased the most items in the month of September and how much was the total spend?
-- MODEL: gpt-3.5-turbo
SELECT c.CountryName, SUM(t.TotalPrice) AS TotalSpend
FROM Countries c
JOIN Customers cust ON c.CountryID = cust.CountryID
JOIN Invoices inv ON cust.CustomerID = inv.CustomerID
JOIN Transactions t ON inv.InvoiceNo = t.InvoiceNo
WHERE strftime('%Y-%m', inv.InvoiceDate) = '2021-09'
GROUP BY c.CountryName
ORDER BY TotalSpend DESC
LIMIT 1;
-- RESULT: None - no transactions in September 2021 (incorrect)
-- REASON FOR FAILURE: The model gpt-3.5-turbo assumed the year to be 2021 because that was the last year in the training data.


-- CORRECT QUERY SYNTAX:
SELECT Countries.CountryName, SUM(Transactions.TotalPrice) AS TotalSpend
FROM Countries
JOIN Customers ON Countries.CountryID = Customers.CountryID
JOIN Invoices ON Customers.CustomerID = Invoices.CustomerID
JOIN Transactions ON Invoices.InvoiceNo = Transactions.InvoiceNo
WHERE strftime('%m', Invoices.InvoiceDate) = '09'
GROUP BY Countries.CountryName
ORDER BY TotalSpend DESC
LIMIT 1;
-- RESULT (Belgium, 17.7) (correct)