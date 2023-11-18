import os
from os.path import join, dirname
import pymysql.cursors
from dotenv import load_dotenv
import sys

def add_new_employee():
    """
    Add new employee: Allow users to create a new employee record using this menu option.
    Show proper error message for constraint violations.
    """
    pass

def view_employee():
    """
    View employee: Ask for employee SSN. For the employee with the given SSN, show all the
    attributes from EMPLOYEE table. Also show supervisor name, department name, and dependents.
    """
    pass

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


def operations(cursor):


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
            pass
        # Create a new record
            # sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
            # cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

        with connection.cursor() as cursor:
            pass
        # Read a single record
            # sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            # cursor.execute(sql, ('webmaster@python.org',))
            # result = cursor.fetchone()
            # print(result)
