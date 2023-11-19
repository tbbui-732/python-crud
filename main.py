import os
from os.path import join, dirname
import pymysql.cursors
from dotenv import load_dotenv
import sys

def add_new_employee(cursor, connection):
    """
    Add new employee: Allow users to create a new employee record using this menu option.
    Show proper error message for constraint violations.
    """
    
    print("Format the following values like below")
    print("Fname,Minit,Lname,Ssn,Bdate,Address,Sex,Salary,Super_ssn,Dno")
    employee_data = str(input("> ")).split(",")
    
    new_employee_data = {
        'Fname':     employee_data[0],
        'Minit':     employee_data[1],
        'Lname':     employee_data[2],
        'Ssn':       employee_data[3],
        'Bdate':     employee_data[4],
        'Address':   employee_data[5],
        'Sex':       employee_data[6],
        'Salary':    int(employee_data[7]),
        'Super_ssn': employee_data[8],
        'Dno':       int(employee_data[9])
    }

    sql = """
            INSERT INTO EMPLOYEE (Fname, Minit, Lname, Ssn, Bdate, Address, Sex, Salary, Super_ssn, Dno)
            VALUES (%(Fname)s, %(Minit)s, %(Lname)s, %(Ssn)s, %(Bdate)s, %(Address)s, %(Sex)s, %(Salary)s, %(Super_ssn)s, %(Dno)s)
    """

    try: 
        cursor.execute(sql, new_employee_data)
        connection.commit()
        print("Successfully added new employee")
    except Exception as e:
        print("Exception caught: " + str(e))
        if 'Ssn' in str(e) or 'ssn' in str(e):
            print("Ensure that social security is in format xxxxxxxxx, not xxx-xx-xxxx")
        if "employee.PRIMARY" in str(e):
            print("No changes were made")


def view_employee(cursor):
    """
    View employee: Ask for employee SSN. For the employee with the given SSN, show all the
    attributes from EMPLOYEE table. Also show supervisor name, department name, and dependents.
    """
    
    print("Enter employee SSN that you want to view")
    ssn = str(input("> "))
    ssn_obj = {"Ssn": ssn}

    sql = """
            SELECT
                e.Fname,
                e.Minit,
                e.Lname,
                e.Ssn,
                e.Bdate,
                e.Address,
                e.Sex,
                e.Salary,
                e.Super_ssn,
                e.Dno,
                s.Fname AS Supervisor_Fname,
                s.Lname AS Supervisor_Lname,
                d.Dname AS Department_Name,
                dep.Dependent_name
            FROM EMPLOYEE e
            INNER JOIN 
                EMPLOYEE s ON e.Super_ssn = s.Ssn
            INNER JOIN 
                DEPARTMENT d ON e.Dno = d.Dnumber
            INNER JOIN 
                DEPENDENT dep ON e.Ssn = dep.Essn
            WHERE
                e.Ssn = %(Ssn)s;
    """

    try: 
        cursor.execute(sql, ssn_obj)
        row = cursor.fetchone()
        print(row)
    except Exception as e:
        print("Exception caught: " + str(e))


def modify_employee():
    """
    Modify employee: Ask for employee SSN. Lock the record. Show employee information.
    Then allow users to update one or more of the following fields: address, sex, salary,
    super_ssn, and Dno.
    """
    pass

def remove_employee():
    """
    Remove employee: Ask for employee SSN. Lock employee record. Show employee
    information. Ask for confirmation to delete. If confirmed, remove the employee. If any
    dependencies exist, show a warning message and ask them to remove the dependencies first
    (i.e., resolve referential integrity constraints violations first).
    """
    pass

def add_new_dependent():
    """
    Add new dependent: Ask for employee SSN. Lock employee record. Show all
    dependents. Ask for new dependent information and create a new dependent record.
    """
    pass

def remove_dependent():
    """
    Remove dependent: Ask for employee SSN. Lock employee record. Show all
    dependents. Ask for the name of the dependent to be removed. Remove the dependent.
    """
    pass

def add_new_department():
    """
    Add new department: Allow users to create a new department record using this menu
    option. Show proper error message for constraint violations.
    """
    pass

def view_department():
    """
    View department: Ask for Dnumber. Show a list of departments, their manager’s name,
    and all department locations.
    """
    pass

def remove_department():
    """
    Remove department: Ask for Dnumber. Lock department record. Show department
    information. Ask for confirmation to delete this department. If confirmed, remove the
    department. If any dependencies exist, show a warning message and ask them to remove the
    dependencies first (i.e., resolve referential integrity constraints violations first).
    """
    pass

def add_department_location():
    """
    Add department location: Ask for Dnumber. Lock department record. Show all
    locations. Ask for a new location and create a new location record.
    """
    pass

def remove_department_location():
    """
    Remove department location: Ask for Dnumber. Lock department record. Show all
    locations. Ask for the location to be removed. Remove the location.
    """
    pass


def operations(cursor, connection):
    display = """
    Menu Options: Select a command
    1. add_new_employee()
    2. view_employee()
    3. modify_employee()
    4. remove_employee()
    5. add_new_dependent()
    6. remove_dependent()
    7. add_new_department()
    8. view_department()
    9. remove_department()
    10. add_department_location()
    11. remove_department_location()
    """
    
    # Get a user input
    print(display)
    operation = str(input("> "))

    # Check if operation is valid
        # Returning true re-runs operation method
    
    if operation == "q":
        print("Exiting program...")
        return False

    if not operation: 
        print("No operation detected, try again")
        return True

    if not operation.isnumeric(): 
        print("Command must be numeric, try again")
        return True

    if int(operation) == 0 or int(operation) > 11: 
        print("Command is out of bounds, try again")
        return True

    # Run the corresponding function
    operation = int(operation)

    if operation == 1:
        print("Adding new employee...")
        add_new_employee(cursor, connection)

    elif operation == 2:
        print("Viewing employee...")
        view_employee(cursor)

    elif operation == 3:
        print("Modifying employee...")
        modify_employee()

    elif operation == 4:
        print("Removing employee...")
        remove_employee()

    elif operation == 5:
        print("Adding new dependent...")
        add_new_dependent()

    elif operation == 6:
        print("Removing dependent...")
        remove_dependent()

    elif operation == 7:
        print("Adding new department...")
        add_new_department()

    elif operation == 8:
        print("Viewing department...")
        view_department()

    elif operation == 9:
        print("Removing department...")
        remove_department()

    elif operation == 10:
        print("Adding department location...")
        add_department_location()

    elif operation == 11:
        print("Removing department location...")
        remove_department_location()

    return True


if __name__ == '__main__':
    # Connect to database

    # Establish connection to TA or to personal machine
    is_TA = str(input('Are you a TA? (y\\n)'))
    if is_TA == 'y':
        USERNAME = 'root'
        PASS = ''
    else:
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)

        USERNAME = os.environ.get("MYSQL_USERNAME")
        PASS = os.environ.get("MYSQL_PASSWORD")

    # Connect to the database
    try: 
        # NOTE: Ignore these error messages
        connection = pymysql.connect(host='localhost',
                                     user=USERNAME,
                                     password=PASS,
                                     database='Company',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        print("Connection successfully established")
    except:
        print("Connection can't be established\nPlease try again")
        sys.exit(1)


    # Make changes to the database
    with connection:
        with connection.cursor() as cursor:
            while True: operations(cursor, connection)
