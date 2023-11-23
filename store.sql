CREATE TABLE Role (
    RoleID INT PRIMARY KEY AUTO_INCREMENT,
    RoleName VARCHAR(50),
    RoleDescription VARCHAR(255)
);

CREATE TABLE User (
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    Username VARCHAR(50),
    Mobile VARCHAR(20),
    Email VARCHAR(100),
    Address VARCHAR(255),
    RoleID INT,
    FOREIGN KEY (RoleID) REFERENCES Role(RoleID)
);

CREATE TABLE Employee (
    EmployeeID INT PRIMARY KEY AUTO_INCREMENT,
    UserID INT,
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
    DateOfBirth DATE,
    Salary DECIMAL(10, 2),
    Address VARCHAR(255),
    PhoneNumber VARCHAR(20),
    HireDate DATE,
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);

CREATE TABLE Supplier (
    SupplierID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100),
    Address VARCHAR(255),
    PhoneNumber VARCHAR(20),
    ContactName VARCHAR(100),
    Email VARCHAR(100)
);

CREATE TABLE Customer (
    CustomerID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100),
    Email VARCHAR(100),
    PhoneNumber VARCHAR(20),
    Address VARCHAR(255)
);

CREATE TABLE Store (
    StoreID INT PRIMARY KEY AUTO_INCREMENT,
    Description VARCHAR(255),
    Type VARCHAR(50),
    Manager INT,
    PhoneNumber VARCHAR(20),
    Address VARCHAR(255),
    FOREIGN KEY (Manager) REFERENCES Employee(EmployeeID)
);

CREATE TABLE Category (
    CategoryID INT PRIMARY KEY AUTO_INCREMENT,
    CategoryName VARCHAR(100)
);

CREATE TABLE Product (
    ProductID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100),
    Description TEXT,
    CategoryID INT,
    SupplierID INT,
    Price DECIMAL(10, 2),
    QuantityInStock INT,
    FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID),
    FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID)
);

CREATE TABLE OrderTable (
    OrderID INT PRIMARY KEY AUTO_INCREMENT,
    CustomerID INT,
    OrderDate DATE,
    TotalPrice DECIMAL(10, 2),
    OrderStatus VARCHAR(50),
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);

CREATE TABLE Transaction (
    TransactionID INT PRIMARY KEY AUTO_INCREMENT,
    OrderID INT,
    EmployeeID INT,
    TransactionDate DATE,
    TransactionAmount DECIMAL(10, 2),
    FOREIGN KEY (OrderID) REFERENCES OrderTable(OrderID),
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID)
);

CREATE TABLE OrderDetails (
    OrderDetailsID INT PRIMARY KEY AUTO_INCREMENT,
    OrderID INT,
    ProductID INT,
    QuantityOrdered INT,
    Price DECIMAL(10, 2),
    FOREIGN KEY (OrderID) REFERENCES OrderTable(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);

-- Role table
INSERT INTO Role (RoleName, RoleDescription) VALUES
('Admin', 'Administrator role'),
('Manager', 'Store manager'),
('Sales', 'Sales representative');

-- User table
INSERT INTO User (Username, Mobile, Email, Address, RoleID) VALUES
('user1', '123-456-7890', 'user1@example.com', '123 Main St, Anytown, US', 1),
('user2', '987-654-3210', 'user2@example.com', '456 Elm St, Othertown, US', 2),
('user3', '555-555-5555', 'user3@example.com', '789 Oak St, Anycity, US', 3);

-- Employee table
INSERT INTO Employee (UserID, FirstName, LastName, DateOfBirth, Salary, Address, PhoneNumber, HireDate) VALUES
(1, 'John', 'Doe', '1985-05-10', 60000.00, '123 Main St, Anytown, US', '111-111-1111', '2020-01-15'),
(2, 'Jane', 'Smith', '1990-08-22', 50000.00, '456 Elm St, Othertown, US', '222-222-2222', '2019-03-20'),
(3, 'Mike', 'Johnson', '1988-12-05', 70000.00, '789 Oak St, Anycity, US', '333-333-3333', '2021-06-10');

-- Supplier table
INSERT INTO Supplier (Name, Address, PhoneNumber, ContactName, Email) VALUES
('Supplier1', '1 Supplier Ave, Town, US', '444-444-4444', 'Supplier Manager', 'supplier1@example.com'),
('Supplier2', '2 Supplier St, City, US', '555-555-5555', 'Supplier Contact', 'supplier2@example.com');

-- Customer table
INSERT INTO Customer (Name, Email, PhoneNumber, Address) VALUES
('Customer1', 'customer1@example.com', '666-666-6666', '321 Maple Rd, Village, US'),
('Customer2', 'customer2@example.com', '777-777-7777', '654 Pine Ln, Hills, US');

-- Store table
INSERT INTO Store (Description, Type, Manager, PhoneNumber, Address) VALUES
('Store1', 'Retail', 1, '888-888-8888', '789 Oak St, Anycity, US'),
('Store2', 'Outlet', 3, '999-999-9999', '456 Elm St, Othertown, US');

-- Category table
INSERT INTO Category (CategoryName) VALUES
('Fruits'),
('Vegetables'),
('Dairy');

-- Product table
INSERT INTO Product (Name, Description, CategoryID, SupplierID, Price, QuantityInStock) VALUES
('Apples', 'ripe apples', 1, 1, 5.99, 50),
('Carrots', 'fresh carrots', 2, 2, 3.99, 100),
('Milk', 'fresh milk', 3, 1, 2.00, 30);

-- OrderTable table
INSERT INTO OrderTable (CustomerID, OrderDate, TotalPrice, OrderStatus) VALUES
(1, '2023-11-18', 5.99, 'Shipped'),
(2, '2023-11-19', 7.98, 'Processing');

-- Transaction table
INSERT INTO Transaction (OrderID, EmployeeID, TransactionDate, TransactionAmount) VALUES
(1, 1, '2023-11-19', 5.99),
(2, 3, '2023-11-19', 7.98);

-- OrderDetails table
INSERT INTO OrderDetails (OrderID, ProductID, QuantityOrdered, Price) VALUES
(1, 1, 1, 5.99),
(2, 2, 2, 3.99);


DELIMITER //

CREATE TRIGGER Before_Insert_OrderTable
BEFORE INSERT ON OrderTable
FOR EACH ROW
BEGIN
    DECLARE customerCount INT;

    SELECT COUNT(*)
    INTO customerCount
    FROM Customer
    WHERE CustomerID = NEW.CustomerID;

    IF customerCount = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Customer does not exist in the Customer table';
    END IF;
END //

DELIMITER ;

DELIMITER //

CREATE TRIGGER Before_Insert_Product
BEFORE INSERT ON Product
FOR EACH ROW
BEGIN
    DECLARE categoryCount INT;

    SELECT COUNT(*)
    INTO categoryCount
    FROM Category
    WHERE CategoryID = NEW.CategoryID;

    IF categoryCount = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Category does not exist in the Category table';
    END IF;
END //

DELIMITER ;

-- Step 1: Add a new column for age
ALTER TABLE Employee
ADD age INT;

-- Update existing records with calculated age
UPDATE Employee
SET age = TIMESTAMPDIFF(YEAR,DateOfBirth,CURDATE());

select * from employee;

DELIMITER //

CREATE FUNCTION GetEmployeeTransactionInfo(employee_id INT)
RETURNS VARCHAR(255)
DETERMINISTIC
BEGIN
    DECLARE num_transactions INT;
    DECLARE total_amount DECIMAL(10, 2);

    SELECT COUNT(TransactionID), SUM(TransactionAmount)
    INTO num_transactions, total_amount
    FROM `Transaction`
    WHERE EmployeeID = employee_id;

    RETURN CONCAT('Employee ID: ', employee_id, 
                  ', Number of Transactions: ', num_transactions,
                  ', Total Transaction Amount: $', total_amount);
END//


DELIMITER ;

SELECT GetEmployeeTransactionInfo(3) AS EmployeeTransactionInfo;


DELIMITER //

CREATE PROCEDURE NotifyLowStock(IN product_id INT, IN threshold_quantity INT)
BEGIN
    DECLARE current_quantity INT;
    DECLARE product_name VARCHAR(100);

    -- Get the current quantity of the specified product
    SELECT QuantityInStock, Name INTO current_quantity, product_name
    FROM Product
    WHERE ProductID = product_id;

    -- Check if the current quantity is below the threshold
    IF current_quantity < threshold_quantity THEN
        -- Use any notification mechanism you have (e.g., printing to console, sending an email)
        SELECT CONCAT('Low stock alert for ', product_name, '. Current quantity: ', current_quantity) AS Notification;
    ELSE
        SELECT 'Stock level is satisfactory' AS Notification;
    END IF;
END//

DELIMITER ;

CALL NotifyLowStock(1, 200);

DELIMITER //

CREATE PROCEDURE UpdateQuantityInStock(IN order_id INT)
BEGIN
    DECLARE product_id_val INT;
    DECLARE quantity_ordered_val INT;

    -- Loop through each product ordered in the order details
    DECLARE done INT DEFAULT FALSE;
    DECLARE cur CURSOR FOR
        SELECT ProductID, QuantityOrdered
        FROM OrderDetails
        WHERE OrderID = order_id;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO product_id_val, quantity_ordered_val;
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Update the QuantityInStock in the Product table
        UPDATE Product
        SET QuantityInStock = QuantityInStock - quantity_ordered_val
        WHERE ProductID = product_id_val;
    END LOOP;

    CLOSE cur;
END //

DELIMITER ;

CALL UpdateQuantityInStock(3); -- Replace 123 with the actual order ID

select * from product;

DELIMITER //

CREATE TRIGGER AfterOrderInsert
AFTER INSERT ON OrderTable
FOR EACH ROW
BEGIN
    CALL UpdateQuantityInStock(NEW.OrderID);
END //

DELIMITER ;

DELIMITER //

CREATE FUNCTION CalculateExperienceLength(employee_id INT)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE hire_date DATE;
    DECLARE experience_length INT;
    
    SELECT HireDate INTO hire_date FROM Employee WHERE EmployeeID = employee_id;
    
    SET experience_length = TIMESTAMPDIFF(YEAR,hire_date,CURDATE());
    
    RETURN experience_length;
END//

DELIMITER ;

select CalculateExperienceLength(2);

drop function CalculateExperienceLength;

DELIMITER //

CREATE PROCEDURE GetEmployeesByDOB(IN date_of_birth DATE)
BEGIN
    CREATE TEMPORARY TABLE tempEmployees AS
    SELECT *
    FROM Employee
    WHERE DateOfBirth = date_of_birth;

    SELECT * FROM tempEmployees;

    DROP TEMPORARY TABLE IF EXISTS tempEmployees;
END //

DELIMITER ;

call GetEmployeesByDOB('2000-11-19');


