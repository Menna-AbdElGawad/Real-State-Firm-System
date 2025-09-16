DROP DATABASE IF EXISTS FirmSystem;
CREATE DATABASE IF NOT EXISTS FirmSystem;
USE FirmSystem;

-- ====================================
-- TABLES
-- ====================================

-- USER table
CREATE TABLE User (
	user_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    phone_no VARCHAR(15),
    username VARCHAR(50) UNIQUE,
    password VARCHAR(100),
    role ENUM('Employee', 'Manager')
);

CREATE TABLE SalesOffice (
	office_id INT AUTO_INCREMENT PRIMARY KEY,
    location VARCHAR(50),
    manager_fk INT UNIQUE
);

CREATE TABLE Manager (
    manager_id INT,
    office_id INT NOT NULL,
    PRIMARY KEY(manager_id),
    FOREIGN KEY (manager_id) REFERENCES `User`(user_id),
	FOREIGN KEY (office_id) REFERENCES SalesOffice(office_id)
);

CREATE TABLE Employee (
	emp_id INT,
    emp_name VARCHAR(50),
	office_id INT NOT NULL,
    PRIMARY KEY (emp_id),
    FOREIGN KEY (emp_id) REFERENCES `User`(user_id),
    FOREIGN KEY (office_id) REFERENCES SalesOffice(office_id)
);

CREATE TABLE Property (
	prop_id INT AUTO_INCREMENT PRIMARY KEY,
    address VARCHAR(50),
	city VARCHAR(50),
    state VARCHAR(50),
    zip VARCHAR(50),
    office_id INT NOT NULL,
    FOREIGN KEY (office_id) REFERENCES SalesOffice(office_id),
    UNIQUE(address, city, state, zip)
);

CREATE TABLE Owner (
	owner_id INT AUTO_INCREMENT PRIMARY KEY,
    owner_name VARCHAR(50)
);

-- Many-to-many between Property and Owner
CREATE TABLE PropertyOwner (
	prop_id INT NOT NULL,
    owner_id INT NOT NULL,
    PRIMARY KEY (prop_id, owner_id),
    FOREIGN KEY (prop_id) REFERENCES Property(prop_id),
    FOREIGN KEY (owner_id) REFERENCES Owner(owner_id)
);

-- ====================================
-- INSERT SAMPLE DATA
-- ====================================

-- Insert SalesOffices
INSERT INTO SalesOffice(location) VALUES
('New York'),
('Chicago'),
('Los Angeles');

-- Insert Managers (Users first)
INSERT INTO User (first_name, last_name, email, phone_no, username, password, role) VALUES
('Menna', 'AbdElGawad', 'menna.manager@gmail.com', '+201000000001', 'menna', '123456', 'Manager'),
('Amr', 'AbdElgawad', 'amr.manager@gmail.com', '+201000000003', 'amr', '123456', 'Manager'),
('Youssef', 'AbdElgawad', 'youssef.manager@gmail.com', '+201000000002', 'youssef', '123456', 'Manager');

-- Insert Employees (Users)
INSERT INTO User (first_name, last_name, email, phone_no, username, password, role) VALUES
('Mona', 'Wael', 'mona.emp@gmail.com', '+201000000004', 'mona', '123456', 'Employee'),
('Aml', 'Talaat', 'aml.emp@gmail.com', '+201000000005', 'aml', '123456', 'Employee');

-- Link Managers to SalesOffices
INSERT INTO Manager (manager_id, office_id) VALUES
(1, 1),  
(2, 2),  
(3, 3); 

-- Update SalesOffices with managers
UPDATE SalesOffice SET manager_fk = 1 WHERE office_id = 1;
UPDATE SalesOffice SET manager_fk = 2 WHERE office_id = 2;
UPDATE SalesOffice SET manager_fk = 3 WHERE office_id = 3;

-- Employees linked to offices
INSERT INTO Employee (emp_id, emp_name, office_id) VALUES
(4, 'Mona Wael', 1),
(5, 'Aml Talaat', 2);

-- Insert Properties
INSERT INTO Property(address, city, state, zip, office_id) VALUES 
('123 Maple St', 'New York', 'NY', '10001', 1),
('456 Oak Ave', 'Chicago', 'IL', '60601', 2),
('789 Pine Blvd', 'Los Angeles', 'CA', '90001', 3),
('321 Birch Rd', 'Chicago', 'IL', '60605', 2),
('654 Cedar Ln', 'New York', 'NY', '10003', 1);

-- Insert Owners
INSERT INTO Owner(owner_name) VALUES
('Menna AbdElGawad'),
('Amr AbdElGawad'),
('Youssef AbdElGawad'),
('Aml Talaat');

-- Property-Owner relations
INSERT INTO PropertyOwner(prop_id, owner_id) VALUES
(1, 1),  
(2, 2),  
(3, 3),  
(4, 4),  
(5, 1),  
(3, 1);  

-- ====================================
-- REQUIRED ASSIGNMENT QUERIES
-- ====================================

-- 2. JOINs
SELECT p.prop_id, p.address, s.location AS office_location
FROM Property p
JOIN SalesOffice s ON p.office_id = s.office_id;

SELECT o.owner_id, o.owner_name, p.prop_id, p.address, p.city
FROM Owner o
JOIN PropertyOwner po ON o.owner_id = po.owner_id
JOIN Property p ON po.prop_id = p.prop_id;

-- 3. Aggregations
SELECT s.office_id, s.location, COUNT(e.emp_id) AS num_employees
FROM SalesOffice s
LEFT JOIN Employee e ON s.office_id = e.office_id
GROUP BY s.office_id, s.location;

SELECT AVG(prop_count) AS avg_props
FROM (
    SELECT office_id, COUNT(*) AS prop_count
    FROM Property
    GROUP BY office_id
) sub;

-- 4. Constraints / NULL handling
ALTER TABLE Property
MODIFY office_id INT NOT NULL;

SELECT u.user_id, u.first_name, u.last_name
FROM User u
JOIN Employee e ON u.user_id = e.emp_id
WHERE u.user_id NOT IN (
    SELECT manager_id FROM Manager
);

-- 5. Subqueries
SELECT office_id, COUNT(*) AS num_props
FROM Property
GROUP BY office_id
HAVING COUNT(*) > (
    SELECT AVG(prop_count)
    FROM (
        SELECT office_id, COUNT(*) AS prop_count
        FROM Property
        GROUP BY office_id
    ) avg_offices
);

SELECT o.owner_id, o.owner_name, COUNT(po.prop_id) AS num_props
FROM Owner o
JOIN PropertyOwner po ON o.owner_id = po.owner_id
GROUP BY o.owner_id, o.owner_name
HAVING COUNT(po.prop_id) > 1;

-- 6. Views
CREATE OR REPLACE VIEW office_summary AS
SELECT s.office_id, s.location,
       COUNT(DISTINCT e.emp_id) AS num_employees,
       COUNT(DISTINCT p.prop_id) AS num_properties
FROM SalesOffice s
LEFT JOIN Employee e ON s.office_id = e.office_id
LEFT JOIN Property p ON s.office_id = p.office_id
GROUP BY s.office_id, s.location;

-- 7. Indexes
CREATE INDEX idx_property_city
ON Property(city);

-- 8. Transaction
START TRANSACTION;

DELETE FROM PropertyOwner
WHERE prop_id = 1;

INSERT INTO Owner(owner_name) VALUES ('New Buyer');
SET @new_owner_id = LAST_INSERT_ID();

INSERT INTO PropertyOwner(prop_id, owner_id)
VALUES (1, @new_owner_id);

COMMIT;
