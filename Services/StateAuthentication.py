from Database.DBConnection import Connector
from Database.Models import Employee
from Core.Manager import ManagerFeatures
from Core.Employee import EmployeeFeatures
import sys

class AuthenticationService(Connector) :
    def __init__(self):
        super().__init__()

    def login(self) :
        while True:
            username = input("\nPlease Enter your Username (or type 'exit' to quit): ")

            if username.lower() == "exit":
                print("GoodBye!")
                sys.exit()

            password = input("Please Enter your Password: ")

            self.cursor.execute (
                """
                select user_id, username, password, first_name, last_name, email, phone_no, role 
                from User 
                where lower(username) = lower(%s) and password = %s
                """ , (username, password,)
            )

            user = self.cursor.fetchone()

            if user and  password == user[2]:
                print(f"\nLogged in {user[3]} {user[4]} Successfully!!")

                if user[7] == 'Manager' :
                    mang = ManagerFeatures()   
                    mang_id = user[0] 
                    mang.manager_menu()

                else :
                    self.cursor.execute(
                        """
                        select emp_id, office_id 
                        from Employee
                        where emp_id = %s
                        """, (user[0],)
                    )

                    emp_data = self.cursor.fetchone()

                    if not emp_data:
                        print("This user is not registered as Employee.")
                        return

                    emp_id = emp_data[0]
                    office_id = emp_data[1]

                    employee = Employee(
                        user_id=user[0],
                        first_name=user[3],
                        last_name=user[4],
                        username=user[1],
                        password=user[2],
                        email=user[5],
                        phone_no=user[6],
                        role=user[7],
                        office_id = office_id
                    )

                    emp_features = EmployeeFeatures()
                    emp_features.emp_menu()

                
            else :
                print("Logging in Failed, Please try again.")