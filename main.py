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


def operations():
    print(""" 
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
11. Remove department location""")
    op = str(input("> ")) 
    return op

if __name__ == "__main__":
    import sqlite3
    
    # create cursor object to manipulate database
    connection = sqlite3.connect("company.db")
    cursor = connection.cursor()
    
    operations()
    print("Closing program...")

    # close
    connection.close()
