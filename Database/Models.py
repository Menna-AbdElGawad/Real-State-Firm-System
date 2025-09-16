class SalesOffice:
    def __init__(self, office_id, location, manager_fk=None):
        self.office_id = office_id
        self.location = location
        self.manager_fk = manager_fk


class User:
    def __init__(self, user_id, first_name, last_name, username, password, email, phone_no, role):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.email = email
        self.phone_no = phone_no
        self.role = role


class Employee(User):    
    def __init__(self, user_id, first_name, last_name, username, password, email, phone_no, role, office_id):
        super().__init__(user_id, first_name, last_name, username, password, email, phone_no, role)
        self.office_id = office_id


class Manager(User):    
    def __init__(self, user_id, first_name, last_name, username, password, email, phone_no, role, office_id):
        super().__init__(user_id, first_name, last_name, username, password, email, phone_no, role)
        self.office_id = office_id


class Property:
    def __init__(self, prop_id, address, city, state, zip_code, office_id):
        self.prop_id = prop_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.office_id = office_id


class Owner:
    def __init__(self, owner_id, owner_name):
        self.owner_id = owner_id
        self.owner_name = owner_name
        self.properties = []  