from Database.DBConnection import Connector
from Services.StateAuthentication import AuthenticationService
import sys

def main() :
    print("\n===== Welcome to Real State Firm System =====")
    print("=============================================")

    while True:
        print("\n===== Main Menu =====")
        print("=====================")
        print("1. Log in")
        print("0. Exit")

        choice = input("\nPlease Enter your choice: ")

        if choice == "0" :
            print("GoodBye:)")
            sys.exit()

        elif choice == '1':
            auth = AuthenticationService()
            auth.login()

        else :
            print("Invalid choice, please try again.")
            
if __name__ == '__main__' :
    main()