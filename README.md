# 🏢 Real Estate Firm Management System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-Educational-green.svg)](#)

A comprehensive database-driven application designed for managing real estate firm operations, developed as part of the Database & Python coursework. The system provides role-based access control for managers and employees to efficiently handle office operations, property management, and client relationships.

## 📋 Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Features](#features)
- [Database Design](#database-design)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [Testing Credentials](#testing-credentials)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

## 🎯 Overview

The Real Estate Firm Management System is a multi-user application that streamlines the management of real estate operations through a structured database approach. The system implements proper authentication, role-based permissions, and comprehensive data validation to ensure secure and efficient operations.

### Key Objectives
- Implement a robust database design using Entity-Relationship modeling
- Develop a Python-based application with MySQL integration
- Provide secure user authentication and role-based access control
- Enable efficient management of properties, offices, and client relationships

## System Architecture

The application follows a layered architecture pattern:

```
├── Presentation Layer (CLI Interface)
├── Business Logic Layer (Services & Core Modules)
├── Data Access Layer (Database Models)
└── Database Layer (MySQL)
```

## ✨ Features

### Manager Capabilities

**Employee Administration**
- Create new employee accounts with comprehensive validation
- Update employee information (credentials, contact details)
- Remove employees from the system
- Enforce business rules (unique email addresses, phone number formatting, password strength)

**Office Operations**
- Register new sales offices
- Assign management responsibilities (one-to-one manager-office relationship)
- Monitor office performance and employee assignments

**Property Portfolio Management**
- Add properties to office inventory
- Process property sales and ownership transfers
- Maintain property-office associations

**Client Management**
- Register new property owners
- Manage property ownership assignments
- Handle many-to-many property-owner relationships

**📊 Reporting & Analytics**
- Generate office management reports
- View employee distribution across offices
- Monitor property assignments and sales

### Employee Capabilities

**Property Operations**
- Browse complete property inventory
- Search properties by unique identifier
- Access detailed property information including office assignments

**Client Services**
- View owner directory and property portfolios
- Generate client-property relationship reports

**Operational Reports**
- Property distribution analysis by office
- Owner portfolio summaries

## 🗄️ Database Design

### Entity-Relationship Model

The system implements a comprehensive ERD with the following core entities:

**User Entity (Superclass)**
- Attributes: `user_id`, `first_name`, `last_name`, `username`, `password`, `email`, `phone_no`, `role`
- Implements ISA hierarchy with Manager and Employee subclasses

**Manager Entity**
- Specialization of User with one-to-one office management relationship

**Employee Entity**
- Specialization of User with many-to-one office assignment relationship

**SalesOffice Entity**
- Attributes: `office_id`, `location`, `manager_fk`
- Central hub for property and personnel management

**Property Entity**
- Attributes: `prop_id`, `address`, `city`, `state`, `zip`, `office_id`
- Represents real estate inventory

**Owner Entity**
- Attributes: `owner_id`, `owner_name`
- Represents property owners/clients

**PropertyOwner Entity**
- Junction table implementing many-to-many property-owner relationships

### Relationship Constraints

- **User ISA {Manager, Employee}**: Disjoint and Total participation
- **SalesOffice ↔ Manager**: One-to-One (each office has exactly one manager)
- **SalesOffice ↔ Employee**: One-to-Many (offices can have multiple employees)
- **SalesOffice ↔ Property**: One-to-Many (properties belong to specific offices)
- **Property ↔ Owner**: Many-to-Many (implemented via PropertyOwner junction table)

## 🛠️ Technology Stack

**Database Management**
- MySQL 8.0+ (Primary database system)
- MySQL Workbench (Database design and administration)

**Backend Development**
- Python 3.8+
- mysql-connector-python (Database connectivity)

**Development Environment**
- Visual Studio Code / PyCharm (IDE)
- Git (Version control)

## ⚙️ Installation

### Prerequisites

- Python 3.8 or higher
- MySQL Server 8.0 or higher
- MySQL Workbench (recommended)

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/real-estate-firm-system.git
   cd real-estate-firm-system
   ```

2. **Database Configuration**
   - Open MySQL Workbench
   - Execute the `FirmSystem.sql` script to create the database schema
   - Verify that sample data has been inserted successfully

3. **Python Environment Setup**
   ```bash
   # Create virtual environment (recommended)
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install mysql-connector-python
   ```

4. **Database Connection Configuration**
   - Update database connection parameters in `Database/DBConnection.py`
   - Ensure MySQL server is running and accessible

5. **Application Launch**
   ```bash
   python Main.py
   ```

## 🚀 Usage

Upon launching the application, users will be prompted to authenticate. The system provides different interfaces based on user roles:

- **Manager Interface**: Full administrative access to all system functions
- **Employee Interface**: Limited access focused on property and client operations

Navigation is menu-driven with clear options and input validation throughout the application.

## Database Schema

The database schema includes the following tables with appropriate constraints:

- `User` (Primary table with role differentiation)
- `SalesOffice` (Office management)
- `Property` (Real estate inventory)
- `Owner` (Client information)
- `PropertyOwner` (Ownership relationships)

All tables include proper primary keys, foreign key constraints, and data validation rules.

## 🔑 Testing Credentials

The system includes pre-configured test accounts for immediate evaluation:

### Manager Accounts
| Username | Password | Role    |
|----------|----------|---------|
| menna    | 123456   | Manager |
| leyla    | 123456   | Manager |

### Employee Accounts
| Username | Password | Role     |
|----------|----------|----------|
| mona     | 123456   | Employee |
| amr      | 123456   | Employee |

## 📁 Project Structure

```
real-estate-firm-system/
│
├── Main.py                           # Application entry point
├── Database/
│   ├── DBConnection.py              # Database connection management
│   └── Models.py                    # Data model definitions
├── Services/
│   └── StateAuthentication.py      # Authentication services
├── Core/
│   ├── Manager.py                   # Manager functionality
│   └── Employee.py                  # Employee functionality
├── FirmSystem.sql                   # Database schema and sample data
├── ERD_Diagram.[format]             # Entity-Relationship Diagram
└── README.md                        # Project documentation
```

## 🤝 Contributing

This project was developed as an educational exercise in database design and Python application development. For suggestions or improvements, please follow standard Git workflow practices:

1. Fork the repository
2. Create a feature branch
3. Implement changes with appropriate testing
4. Submit a pull request with detailed description

---

**Note**: This system is designed for educational purposes and demonstrates fundamental concepts in database design, Python programming, and software architecture. For production deployment, additional security measures and scalability considerations should be implemented.
