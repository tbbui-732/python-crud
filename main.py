DISPLAY = """
Enter one of the following...
1.  Add new employee
2.  View employee
3.  Modify employee
4.  Remove employee
5.  Add new dependent
6.  Remove dependent
7.  Add new department
8.  View department
9.  Remove department
10. Add department location
11. Remove department location"""

# TODO: work on question 1, create an employee table if one doesn't exist!, do this for the following functions as well

# 1 
# Show proper error message for constraint violations
def add_employee():
    pass

# 2
# Ask for employee SSN
# Show all atributes from EMPLOYEE table
# Show supervisor name, department name, and dependents
def view_employee():
    pass

# 3 
# Ask for employee SSN
# Lock the record
# Show employee information
# Allow users to update one or more of the following fields:
#% address, sex, salary, super_ssn, and Dno
def modify_employee():
    pass

# 4
# Ask for employee SSN 
# Lock employee record 
# Show employee information
# Ask confirmation to delete 
# If dependencies exist, show warning messages and ask to remove dependency first
def remove_employee():
    pass

# 5
# Ask for employee SSN 
# Lock employee record 
# Show all dependents 
# Ask for dependent information and create new dependent record
def add_dependent():
    pass

# 6
# Ask for employee SSN 
# Lock employee record 
# Show all dependents 
# Ask for name of dependent to be removed 
# Remove the dependent 
def remove_dependent():
    pass

# 7
# Allow users to create new department record 
# Show proper error messages for constraint violations
def add_department():
    pass

# 8
# Ask for Dnumber 
# Show list of departments, their manager's name, and locations
def view_department(): 
    pass 

# 9 
# Ask for Dnumber 
# Lock department record 
# Show department information 
# Ask for confirmation to delete department 
# Remove the department 
# If any dependencies exist, ask to remove dependencies before removing department
def remove_department(): 
    pass 

# 10
# Ask for Dnumber 
# Lock department record 
# Show all locations 
# Ask for new location and create a new location record
def add_department_location(): 
    pass 

# 11 
# Ask for Dnumber 
# Lock department record 
# Show all locations 
# Ask for location to be removed 
# Remove the location
def remove_department_location():
    pass


# Indefinitely checks for user input, running function according to operation selected
def operations():
    while True:
        print(DISPLAY) 

        # Make sure input is valid
        op = input("> ")

        if not op:
            print("Invalid input, try again")
            continue

        if not op.isnumeric() and op != "q":
            print("Invalid input, try again")
            continue

        if op == "q": break
            
        # Select corresponding function
        op = int(op)
        if op == 1:    add_employee()
        elif op == 2:  view_employee()
        elif op == 3:  modify_employee()
        elif op == 4:  remove_employee()
        elif op == 5:  add_dependent()
        elif op == 6:  remove_dependent()
        elif op == 7:  add_department() 
        elif op == 8:  view_department()
        elif op == 9:  remove_department()
        elif op == 10: add_department_location()
        elif op == 11: remove_department_location()
        else:
            print("Invalid input, try again")


if __name__ == "__main__":
    import sqlite3
    
    # Connect to database
    connection = sqlite3.connect("company.db")
    cursor = connection.cursor()
    
    # Deploy CRUD operations to database
    operations()
    print("Closing program...")

    # Drop connection
    connection.close()
