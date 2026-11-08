--Joining tables
SELECT *
FROM Customers
JOIN Services USING (customerID)
JOIN Billing USING (customerID);