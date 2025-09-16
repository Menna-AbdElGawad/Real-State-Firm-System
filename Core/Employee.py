from Database.DBConnection import Connector
import sys 

class EmployeeFeatures(Connector) :
    def __init__(self):
        super().__init__()

    def list_prop(self) :
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

    def search_prop(self) :
        self.cursor.execute(
            """
            select prop_id
            from Property
            """
        )

        properties = self.cursor.fetchall()

        print("\nProperties List:")
        print("==================\n")

        count = 1
        for property in properties:
            print(f"{count}- {property[0]}")
            print("-------\n")

            count += 1

        prop_id = input("\n• Please Choose a property ID you want to search for: ") 

        try:
            prop_id = int(prop_id)
        except ValueError:
            print("Invalid Property ID.")
            return

        all_prop_ids = [p[0] for p in properties]
        if prop_id not in all_prop_ids:
            print(f"\nProperty ID: {prop_id} not found!")
            return
        
        self.cursor.execute(
            """
            select prop_id, address, city, state, zip, office_id
            from Property
            where prop_id = %s
            """, (prop_id,)
        )

        prop = self.cursor.fetchone()

        print(f"\nProperty you searched for: ")
        print("-------------------------------\n")

        self.cursor.execute(
            """
            select location
            from SalesOffice
            where office_id = %s
            """, (prop[5],)
        )

        location = self.cursor.fetchone()

        print(f"• Property ID: {prop[0]}")
        print(f"• Address: {prop[1]}")
        print(f"• City: {prop[2]}")
        print(f"• State: {prop[3]}")
        print(f"• Zip Code: {prop[4]}")
        print(f"• Office Location: {location[0]}")
        print("\n-------------------------------\n")

    def view_ownersProp(self):
        self.cursor.execute(
            """
            select prop_id, owner_id
            from PropertyOwner
            """
        )
        prop_owners = self.cursor.fetchall()

        print(f"\nProperty ID | Owner Name")
        print("---------------------------\n")

        for prop_owner in prop_owners:
            self.cursor.execute(
                """
                select owner_id, owner_name
                from Owner
                where owner_id = %s
                """, (prop_owner[1],)   
            )
            owner = self.cursor.fetchall()

            if owner:  
                print(f"•     {prop_owner[0]}     | {owner[0][1]}")
                print("\n------------------------------------\n")



    # def generate_report(self) :

    def emp_menu(self) :
        while True:
            print("\n===== Employee Menu =====")
            print("=========================")
            print("1. List all Properties")
            print("2. Search for Property")
            print("3. View Owners and their Properties")
            print("4. Logout and Return to Main Page")
            print("0. Exit")

            choice = int(input("\nPlease Enter you choice: "))

            if choice == 0: 
                print("GoodBye:)")
                sys.exit()

            elif choice == 1 :
                self.list_prop()

            elif choice == 2 :
                self.search_prop()

            elif choice == 3 :
                self.view_ownersProp()

            # elif choice == 4 :
            #     self.generate_report()

            elif choice == 4 :
                print("\nLogging out and transfering to the main page.")
                return 
            
            else :
                print("\nInvalid Input, please try again.")