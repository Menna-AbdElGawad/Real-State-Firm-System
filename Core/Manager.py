from Database.DBConnection import Connector
import sys

class ManagerFeatures(Connector) :
    def __init__(self):
        super().__init__()

    def add_emp(self) :
        first_name = input("\n• Enter Employee's First Name: ")
        last_name = input("• Enter Employee's Last Name: ")
        username = input("• Enter Employee's Username: ")
        password = input("• Enter Employee's Password (not less than 6 characters): ")
        email = input("• Enter Employee's Email in a right format (ex: name@example.com): ")
        phone_no = input("• Enter Employee's Phone Number (ex: +201234567890): ")
        role = "Employee"

        if not phone_no.startswith('+201') or len(phone_no) != 13 :
            print("Invalid phone number, please try again.")
            return
        
        if not email.endswith('@gmail.com') :
            print("Invalid email, please try again.")
            return
        
        self.cursor.execute("select email from User where email = %s", (email,))
        if self.cursor.fetchone() :
            print("Email already exists, please try another Email.")
            return
        
        self.cursor.execute(
            """
            insert into User (first_name, last_name, username, password, email, phone_no, role)
            values (%s, %s, %s, %s, %s, %s, %s)
            """, (first_name, last_name, username, password, email, phone_no, role,)
        )

        user_id = self.cursor.lastrowid

        self.cursor.execute("select office_id, location from SalesOffice")

        offices = self.cursor.fetchall()

        print("\n=== Available Offices ===")
        print("=========================")
        print("Office ID : Office Location\n")
        for office in offices :
            print(f"{office[0]} : {office[1]}\n")

        office_id = int(input("\n• Enter Office ID to assign this employee: "))

        self.cursor.execute(
            """
            insert into Employee (emp_id, emp_name, office_id)
            values (%s, %s, %s)
            """, (user_id, f'{first_name} {last_name}', office_id)
        )


        self.conn.commit()
        print('\n')
        print(f'Employee: {first_name} {last_name}, added successfully.')
        print('\n')

    def remove_emp(self) :
        first_name = input("\n• Please Enter the first name: ")
        last_name = input("• Please Enter the last name: ")

        self.cursor.execute (
            """
            select user_id 
            from User
            where first_name = %s and last_name = %s and role = 'Employee'
            """, (first_name, last_name,)
        )

        emp = self.cursor.fetchone()

        if emp :
            emp_id = emp[0]
            self.cursor.execute(
                """
                delete from Employee
                where emp_id = %s
                """, (emp_id,)
            )

            self.cursor.execute(
                """
                delete from User
                where user_id = %s
                """, (emp_id,)
            )

            self.conn.commit()
            print('\n')
            print(f'Employee: {first_name} {last_name}, removed successfully.')
            print('\n')
        
    def edit_emp(self) :
        emp_id = int(input("\n• Enter Employee ID to edit: "))

        print("\nWhat do you want to edit?")
        print("============================")
        print("1. First Name")
        print("2. Last Name")
        print("3. Username")
        print("4. Password")
        print("5. Email")
        print("6. Phone Number")
        print("0. Cancel")

        choice = int(input("\n• Enter your choice: "))

        fields = {
            1: "first_name",
            2: "last_name",
            3: "username",
            4: "password",
            5: "email",
            6: "phone_no"
        }

        if choice == 0:
            print("Cancelled editing.")
    

        if choice in fields:
            new_value = input(f"\n• Enter new {fields[choice]}: ")
            self.cursor.execute(
                f"update User set {fields[choice]} = %s where user_id = %s and role = 'Employee'",
                (new_value, emp_id)
            )
            self.conn.commit()
            print(f"{fields[choice]} updated successfully!")
        else:
            print("Invalid choice, please try again.")

    def add_owner(self) :
        owner_name = input("\n• Please Enter owner Name: ")

        self.cursor.execute(
            """
            select owner_id, owner_name 
            from Owner
            where owner_name = %s
            """, (owner_name,)
        )

        owner = self.cursor.fetchone()

        if owner:
            owner_id = owner[0]
            self.cursor.execute(
                """
                select prop_id, owner_id
                from PropertyOwner
                where owner_id = %s
                """, (owner_id,)
            )

            properties = self.cursor.fetchall()

            print(f"\nOwner: {owner_name} is already exist.")
            choice = input("\n• Do you want to return his properties? (y/n)")

            if choice.lower() != 'y' :
                print("\nGood Bye!")
                return
            else :
                print(f"\nOwner: {owner_name} has properties: ")
                for property in properties :
                    print(f"{property[0]}\n")

        else:
            self.cursor.execute(
                """
                insert into Owner (owner_name)
                values (%s)
                """, (owner_name,)
            )      

            self.conn.commit()
            print(f"\nOwner: {owner_name} added successfully!\n")   

    def list_owners(self) :
        self.cursor.execute(
            """
            select owner_id, owner_name
            from Owner
            """
        )

        owners = self.cursor.fetchall()

        print("\nOwners' List: ")
        print("=============")
        print("\nOwner ID | Owner Name")
        for owner in owners :
            print(f"   {owner[0]}     | {owner[1]}\n")

    def view_prop(self) :
        self.cursor.execute(
            """
            select prop_id, address, city, state, zip, office_id
            from Property
            """
        )

        properties = self.cursor.fetchall()

        print("\nProperties List:")
        print("==================\n")

        count = 1
        for property in properties:

            self.cursor.execute(
            """
            select location
            from SalesOffice
            where office_id = %s
            """, (property[5],)
            )

            location = self.cursor.fetchone()

            print(f"{count}- ")
            print(f"Property ID: {property[0]}")
            print(f"Address: {property[1]}")
            print(f"City: {property[2]}")
            print(f"State: {property[3]}")
            print(f"Zip Code: {property[4]}")
            print(f"Office Location: {location[0]}")
            print("\n-------------------------------\n")

            count += 1

    def add_prop(self) :
        address = input("\n• Please Enter Property Address: ")
        city = input("• Please Enter city: ")
        state = input("• Please Enter state: ")
        zip = input("• Please Enter Zip Code: ")

        self.cursor.execute(
            """
            select office_id
            from SalesOffice
            """
        )

        offices = [o[0] for o in self.cursor.fetchall()]

        print("\n Offices' List:")
        print("=================\n")
        for office in offices :
            print(f"- {office}\n")

        print("-------------------------")
        office_id = input("\n• Please Enter Office ID: ")

        try:
            office_id = int(office_id)
        except ValueError:
            print("Invalid Office ID.")
            return

        if office_id not in offices:
            print(f"\nOffice ID: {office_id} not found!")
            return
                
        self.cursor.execute(
            """
            insert into Property (address, city, state, zip, office_id)
            values (%s, %s, %s, %s, %s)
            """, (address, city, state, zip, office_id)
        )

        self.conn.commit()
        print(f"Property added Successfully!\n")

    def sell_prop(self) : 
        owner_name = input("\n• Please Enter owner Name: ")
        print("\nProperties' ID:")
        print("===============")

        self.cursor.execute(
            """
            select prop_id
            from Property
            """
        )
        prop_list = self.cursor.fetchall()
        
        for prop in prop_list:
            print(f"- {prop[0]}")

        try:
            prop_id = input("\n• Please Enter property ID: ")
        
        except ValueError:
            print("Invalid Property ID.")
            return

        self.cursor.execute(
            """
            select owner_id, owner_name
            from Owner
            where owner_name = %s
            """, (owner_name,)
        )

        owner = self.cursor.fetchone()

        if not owner:
            print(f"\nOwner {owner_name} not found!")
            return

        self.cursor.execute(
            """
            delete from PropertyOwner
            where prop_id = %s
            """, (prop_id,)
        )


        self.cursor.execute(
            """
            insert into PropertyOwner (prop_id, owner_id)
            values (%s, %s)
            """, (prop_id, owner[0])
        )

        self.conn.commit()
        print(f"\nProperty: {prop_id} selled successfully to Owner: {owner_name}.")

    def add_office(self) :
        location = input("\n• Please Enter Location of the office: ")

        self.cursor.execute(
            """
            insert into SalesOffice (location)
            values (%s)
            """, (location,)
        )

        self.conn.commit()
        print(f"\nOffice Location: {location} added successfully.\n")

    def view_office(self) :
        self.cursor.execute(
            """
            select office_id, location
            from SalesOffice
            """
        )

        offices = self.cursor.fetchall()
        count = 1

        for office in offices:
            print(f"{count}- ")
            print(f"Office ID: {office[0]}")
            print(f"Office Location: {office[1]}")

            print("\n-----------------------------\n")
            count += 1

    def assign_manager(self) :
        self.cursor.execute(
            """
            select user_id, first_name, last_name, role
            from User
            where role = 'Manager'
            """
        )

        managers = self.cursor.fetchall()
        count = 1
        print("\n============================================\n")

        print("\nManagers' List:")
        print("=================\n")

        print("Manager ID | Manager Name")
        print("-------------------------")
        
        for manager in managers :
            print(f"{count}-     {manager[0]}   | {manager[1]} {manager[2]}")

            print("\n----------------------------")
            count += 1

        self.view_office()

        manager_id = input("\n• Please Enter Manage ID: ")
        office_id = input("\n• Please Enter Office ID: ")

        if manager_id and office_id :

            self.cursor.execute(
                """
                select office_id 
                from SalesOffice
                where manager_fk = %s
                """, (manager_id,)
            )

            already = self.cursor.fetchone()

            if already:
                print(f"\nManager ID: {manager_id} is already assigned to Office ID: {already[0]}.")
                return 
            
            self.cursor.execute(
                """
                update SalesOffice
                set manager_fk = %s
                where office_id = %s
                """, (manager_id, office_id,)
            )

            self.conn.commit()
            print(f"\nOffice ID: {office_id} Assigned to Manager: {manager_id} successfully.\n")

    def sales_report(self) :
        self.cursor.execute(
            """
            select office_id, city, count(prop_id) as num_prop
            from Property
            group by office_id, city
            """
        )

        sales = self.cursor.fetchall()

        print("\nOffice ID | Property ID | City")
        print("--------------------------------------\n")

        for sale in sales :
            print(f"     {sale[0]}    |     {sale[2]}       |  {sale[1]}  ")
            print("\n--------------------------------------\n")
        
    def emp_report(self) :
        self.cursor.execute(
            """
            select office_id, count(emp_id) as num_emp
            from Employee
            group by office_id
            """
        )

        emps = self.cursor.fetchall()

        print("\nOffice ID | Number of Employees")
        print("--------------------------------\n")

        for emp in emps :
            print(f"     {emp[0]}    |     {emp[1]}")
            print("\n--------------------------------\n")

    def prop_report(self) :
        self.cursor.execute(
            """
            select city, count(prop_id) as num_prop
            from Property
            group by city
            """
        )

        props = self.cursor.fetchall()

        print("\nNumber of Properties | City")
        print("------------------------------\n")

        for prop in props :
            print(f"          {prop[1]}          | {prop[0]}")
            print("\n------------------------------\n")

    def generate_report(self) :
        while True:
            print("\n=== Reports' Menu ===")
            print("=====================")
            print("1. Sales Office Report")
            print("2. Employees' Report")
            print("3. Properties Report")
            print("4. Cancel and return to main menu") 
            print("0. Exit") 

            choice = int(input("\n• Please Enter your choice: "))

            if choice == 0 :
                print("GoodBye:)")
                sys.exit()

            elif choice == 1 :
                self.sales_report()

            elif choice == 2 :
                self.emp_report()

            elif choice == 3 :
                self.prop_report()

            elif choice == 4 :
                print("\nReturning to the Main Menu.\n")
                self.manager_menu()

            else :
                print("\nInvalid Input, please try again.")


    def manager_menu(self) :
        while True:
            print("\n===== Manager Menu =====")
            print("========================")
            print("1. Add Employee") 
            print("2. Remove Employee") 
            print("3. Edit Employee") 
            print("4. Add Owner") 
            print("5. List Owners") 
            print("6. View All Properties") 
            print("7. Add Property") 
            print("8. Sell Property to Owner") 
            print("9. Add Office") 
            print("10. View all Offices") 
            print("11. Assign Manager to an office") 
            print("12. Generate Report (e.g., properties in my office)")
            print("13. Log our and Return to Main Page") 
            print("0. Exit") 

            choice = int(input("\n• Please Enter you choice: "))

            if choice == 0: 
                print("GoodBye:)")
                sys.exit()

            elif choice == 1 :
                self.add_emp()

            elif choice == 2 :
                self.remove_emp()

            elif choice == 3 :
                self.edit_emp()

            elif choice == 4 :
                self.add_owner()

            elif choice == 5 :
                self.list_owners()
            
            elif choice == 6 :
                self.view_prop()
            
            elif choice == 7 :
                self.add_prop()

            elif choice == 8 :
                self.sell_prop()

            elif choice == 9 :
                self.add_office()

            elif choice == 10 :
                self.view_office()

            elif choice == 11 :
                self.assign_manager()

            elif choice == 12 :
                self.generate_report() 

            elif choice == 13 :
                print("\nLogging out and transfering to the main page.")
                return 
            
            else :
                print("\nInvalid Input, please try again.")