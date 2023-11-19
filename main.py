import os
from os.path import join, dirname
import pymysql.cursors
from dotenv import load_dotenv
import sys

"""
Add new employee: Allow users to create a new employee record using this menu option.
Show proper error message for constraint violations.
"""
def add_new_employee(cursor, connection):

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


"""
View employee: Ask for employee SSN. For the employee with the given SSN, show all the
attributes from EMPLOYEE table. Also show supervisor name, department name, and dependents.
"""
def view_employee(cursor):

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
            LEFT JOIN 
                EMPLOYEE s ON e.Super_ssn = s.Ssn
            LEFT JOIN 
                DEPARTMENT d ON e.Dno = d.Dnumber
            LEFT JOIN 
                DEPENDENT dep ON e.Ssn = dep.Essn
            WHERE
                e.Ssn = %(Ssn)s
    """

    try: 
        cursor.execute(sql, ssn_obj)
        row = cursor.fetchone()
        print(row)
    except Exception as e:
        print("Exception caught: " + str(e))


"""
Modify employee: Ask for employee SSN. Lock the record. Show employee information.
Then allow users to update one or more of the following fields: address, sex, salary,
super_ssn, and Dno.
"""
def modify_employee(cursor, connection):

    # Query user for employee SSN to modify
    print("Enter employee SSN that you want to modify")
    ssn = str(input("> "))
    ssn_obj = {"Ssn": ssn}

    sql = """
            SELECT * FROM EMPLOYEE WHERE Ssn=%(Ssn)s
    """

    # Display employee information
    try: 
        cursor.execute(sql, ssn_obj)
        row = cursor.fetchone()
        print(row)
    except Exception as e:
        print("Exception caught: " + str(e))

    # Query user for field to update
    while True:
        print("Select a field to update")
        print("""
        1. Address
        2. Sex 
        3. Salary 
        4. Super_ssn 
        5. Dno""")
        field = int(input("> "))

        if field == 1:
            # Modify address
            attribute_name = "Address"
            new_value = str(input("New address > "))
            break
        elif field == 2:
            # Modify sex
            attribute_name = "Sex"
            new_value = str(input("New sex > "))
            break
        elif field == 3:
            # Modify salary
            attribute_name = "Salary"
            new_value = str(input("New salary > "))
            break
        elif field == 4:
            # Modify super ssn
            attribute_name = "Super_ssn"
            new_value = str(input("New super ssn > "))
            break
        elif field == 5:
            # Modify dno
            attribute_name = "Dno"
            new_value = str(input("New department number > "))
            break
        else: 
            print("Invalid field, try again")
            continue

    # Update changes to database
    mod_data = {
            "new_value": new_value,
            "Ssn": ssn

            }

    sql = f"""
           UPDATE EMPLOYEE 
           SET {attribute_name} = %(new_value)s
           WHERE Ssn=%(Ssn)s
    """

    try:
        cursor.execute(sql, mod_data)
        connection.commit()
    except Exception as e:
        print("Exception caught: " + str(e))
        connection.rollback()


"""
Employees have references to the following:
    Dependents
"""
def _remove_employee_dependencies(cursor, connection, essn):

    # Confirm to user to delete dependents
    print("This action can't be completed without deleting all dependents")
    print("Please confirm that you are willing to delete all dependencies (y\\n)")
    confirm = str(input("> "))
    if confirm == "n":
        print("No changes have been made")
        return False

    # Delete all children/spouse dependents 
    sql = """
            DELETE FROM DEPENDENT
            WHERE Essn = %(Essn)s
    """ 
    try: 
        cursor.execute(sql, {"Essn": essn})
        connection.commit()
        print("Successfully deleted dependents")
    except Exception as e:
        print("Exception caught: " + str(e))
        connection.rollback()
        return False

    
    # Null out super_ssns for other employees if applicable
    sql = """
            UPDATE EMPLOYEE 
            SET Super_ssn = NULL
            WHERE Super_ssn = %(Essn)s
    """
    try:
        cursor.execute(sql, {"Essn": essn})
        connection.commit()
        print("Successfully nulled corresponding Super_ssns")
    except Exception as e:
        print("Exception caught: " + str(e))
        connection.rollback()
        return False
   
    # Delete rows from Works_On
    sql = """
            DELETE FROM WORKS_ON 
            WHERE Essn = %(Essn)s
    """
    try: 
        cursor.execute(sql, {"Essn": essn})
        connection.commit()
        print("Successfully deleted rows from Works_On")
    except Exception as e:
        print("Exception caught: " + str(e))
        connection.rollback()
        return False

    
    # Delete Department Mgr_SSN if applicable
    sql = """
            UPDATE DEPARTMENT 
            SET Mgr_ssn = NULL, 
                Mgr_start_date = NULL 
            WHERE Mgr_ssn = %(Essn)s
    """
    try:
        cursor.execute(sql, {"Essn": essn})
        connection.commit()
    except Exception as e:
        print("Exception caught: " + str(e))
        connection.rollback()

    return True
    

"""
Remove employee: Ask for employee SSN. Lock employee record. Show employee
information. Ask for confirmation to delete. If confirmed, remove the employee. If any
dependencies exist, show a warning message and ask them to remove the dependencies first
(i.e., resolve referential integrity constraints violations first).
"""
def remove_employee(cursor, connection):
    
    # Query user for employee SSN 
    print("Enter SSN of employee to be removed")
    ssn = str(input("> "))
    ssn_obj = {"Ssn": ssn}

    # Show employee information
    sql = "SELECT * FROM EMPLOYEE WHERE Ssn=%(Ssn)s"
    try: 
        cursor.execute(sql, ssn_obj)
        row = cursor.fetchone()
        if "None" in row:
            print(f"Employee {ssn} does not exist")
            return
        print(row)
    except Exception as e:
        print("Exception caught: " + str(e))
        return


    # Ask for confirmation to delete
    print("Are you sure you want to delete? (y\\n)")
    confirm = str(input("> "))

    if confirm == "n":
        print("No changes have been made")
        return

    # Remove employee 
    sql = """
            DELETE FROM EMPLOYEE
            WHERE Ssn = %(Ssn)s
    """

    while True:
        try: 
            cursor.execute(sql, ssn_obj)
            connection.commit()
            print(f"Succesfully removed employee {ssn}")
            break
        except Exception as e:
            # Dependency error -> Must remove dependencies first!
            if "1451" in str(e):
                print(str(e))
                if _remove_employee_dependencies(cursor, connection, ssn):
                    continue
            print("Exception caught: " + str(e))
            connection.rollback()
            break


"""
Add new dependent: Ask for employee SSN. Lock employee record. Show all
dependents. Ask for new dependent information and create a new dependent record.
"""
def add_new_dependent(cursor, connection):
    
    # Query user for SSN
    print("Enter SSN of employee to add dependent")
    ssn = str(input("> "))
    ssn_obj = {"Ssn": ssn}

    # Show current dependents if any exist
    sql = """
            SELECT
                e.Fname AS Employee_Fname,
                e.Lname AS Employee_Lname,
                dep.Dependent_name
            FROM EMPLOYEE e
            LEFT JOIN 
                DEPENDENT dep ON e.Ssn = dep.Essn
            WHERE e.Ssn = %(Ssn)s
    """ 
    try:
        cursor.execute(sql, ssn_obj)
        rows = cursor.fetchall()
        print("Dependents:")
        for row in rows:
            print(row)
    except Exception as e:
        print("Exception caught: " + str(e))
        return
    
    # Query user for new dependent data
    print("Enter the values for the new dependent in a single string split by commas")
    print("Dependent_name,Sex,Birthday,Relationship")
    dependent_data = str(input("> ")).split(",")

    # Add new dependent
    new_dependent_data = {
            "Essn": ssn,
            "Dependent_name": dependent_data[0],
            "Sex":            dependent_data[1],
            "Bdate":          dependent_data[2],
            "Relationship":   dependent_data[3]
    }
    print(new_dependent_data)
    sql = """
            INSERT INTO DEPENDENT 
                (Essn, Dependent_name, Sex, Bdate, Relationship)
            VALUES 
                (%(Essn)s, %(Dependent_name)s, %(Sex)s, %(Bdate)s, %(Relationship)s)
             
    """
    try:
        cursor.execute(sql, new_dependent_data)
        connection.commit()
        print("Succesfully added new dependent")
    except Exception as e:
        print("Exception caught: " + str(e))
        connection.rollback()


"""
Remove dependent: Ask for employee SSN. Lock employee record. Show all
dependents. Ask for the name of the dependent to be removed. Remove the dependent.
"""
def remove_dependent(cursor, connection):
    # Query user for employee SSN
    print("Enter employee SSN to remove dependent")
    ssn = str(input("> "))
    ssn_obj = {"Ssn": ssn}

    # Show dependents
    sql = """
        SELECT * FROM DEPENDENT
        WHERE Essn = %(Ssn)s
    """
    try:
        cursor.execute(sql, ssn_obj)
        rows = cursor.fetchall()
        for row in rows: print(row)
    except Exception as e:
        print("Exception caught: " + str(e))
    
    # Query user for name of dependent to be removed
    print("Enter name of dependent to remove")
    dependent = str(input("> "))

    # Remove the dependent
    dependent_data = {
            "Ssn": ssn,
            "Dependent_name": dependent
    }
    sql = """
        DELETE FROM DEPENDENT
        WHERE Essn = %(Ssn)s AND Dependent_name = %(Dependent_name)s
    """
    try:
        cursor.execute(sql, dependent_data)
        connection.commit()
        print(f"Successfully deleted {dependent}")
    except Exception as e:
        print("Exception caught: " + str(e))
        connection.rollback()


"""
Add new department: Allow users to create a new department record using this menu
option. Show proper error message for constraint violations.
"""
def add_new_department(cursor, connection):
    
    # Query user for new department data
    print("Format the new department values as such...")
    print("Dname,Dnumber,Mgr_ssn,Mgr_start_date")
    data = str(input("> ")).split(",")

    department_data = {
            "Dname":    data[0],
            "Dnumber":  data[1],
            "Mgr_ssn":  data[2],
            "Mgr_start_date": data[3]
    }
    sql = """
            INSERT INTO DEPARTMENT (Dname, Dnumber, Mgr_ssn, Mgr_start_date)
            VALUES (%(Dname)s, %(Dnumber)s, %(Mgr_ssn)s, %(Mgr_start_date)s)
    """
    try:
        cursor.execute(sql, department_data)
        connection.commit()
        print("Successfully added new department")
    except Exception as e:
        print("Exception caught: " + str(e))


"""
View department: Ask for Dnumber. Show a list of departments, their manager’s name,
and all department locations.
"""
def view_department(cursor):

    # Query user for Dnumber
    print("Enter Dnumber in order to view department information")
    dno = int(input("> ")) 
    dno_obj = {"Dno": dno}

    # Show row, manager's name, and all department locations
    sql = """
            SELECT 
                dept.Dname,
                dept.Dnumber,
                dept.Mgr_ssn,
                dept.Mgr_start_date,
                mgr.Fname,
                mgr.Lname,
                loc.Dlocation
            FROM DEPARTMENT AS dept
            LEFT JOIN 
                EMPLOYEE AS mgr ON dept.Mgr_ssn = mgr.Ssn
            LEFT JOIN 
                DEPT_LOCATIONS AS loc ON dept.Dnumber = loc.Dnumber
            WHERE dept.Dnumber = %(Dno)s;
    """

    try:
        cursor.execute(sql, dno_obj)
        rows = cursor.fetchall()
        for row in rows: print(row)
    except Exception as e:
        print("Exception caught: " + str(e))


"""
Helper function for removing department 
Deletes and nullifies dependencies
"""
def _remove_department_dependencies(cursor, connection, dnumber):
    # Confirm to user to remove all dependencies
    print("Dependencies for this department must be deleted to proceed")
    print("Please confirm that you are okay with this (y\\n)")
    confirm = str(input("> "))
    if confirm == "n":
        print("No changes have been made")
        return False
    
    # Nullify employee Dno 
    sql = """
            UPDATE EMPLOYEE 
            SET Dno = NULL 
            WHERE Dno = %(Dnumber)s
    """
    try:
        cursor.execute(sql, {"Dnumber": dnumber}) 
        connection.commit()
        print("Successfully nullified employee Dno")
    except Exception as e:
        print("Exception caught nullify: " + str(e))
        connection.rollback()
        return False


    # Alter table to remove department location
    sql = """
            ALTER TABLE DEPT_LOCATIONS
            DROP FOREIGN KEY dept_locations_ibfk_1
    """
    try:
        cursor.execute(sql)
        connection.commit()
        print("Altered table to remove foreign key constraints")
    except Exception as e:
        print("Exception caught alter: " + str(e))
        connection.rollback()
        return False

    # Allow department location to be automatically deleted on cascade
    sql = """
            ALTER TABLE DEPT_LOCATIONS 
            ADD CONSTRAINT dept_locations_ibfk_1
            FOREIGN KEY (Dnumber) REFERENCES DEPARTMENT(Dnumber) ON DELETE CASCADE
    """
    try:
        cursor.execute(sql)
        connection.commit()
        print("Allow dept_location to delete automatically on cascade")
    except Exception as e:
        print("Exception caught cascade: " + str(e))
        connection.rollback()
        return False


    # Nullify project Dnum
    sql = """
            UPDATE PROJECT 
            SET Dnum = NULL 
            WHERE Dnum = %(Dnumber)s
    """
    try: 
        cursor.execute(sql, {"Dnumber": dnumber})
        connection.commit()
        print("Successfully nullifed project dnum")
    except Exception as e:
        print("Exception caught cascade: " + str(e))
        connection.rollback()
        return False

    return True


"""
Remove department: Ask for Dnumber. Lock department record. Show department
information. Ask for confirmation to delete this department. If confirmed, remove the
department. If any dependencies exist, show a warning message and ask them to remove the
dependencies first (i.e., resolve referential integrity constraints violations first).
"""
def remove_department(cursor, connection):
    
    # Show departments
    sql = """
            SELECT * FROM DEPARTMENT
    """
    try: 
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows: print(row)
    except Exception as e:
        print("Exception caught: " + str(e))

    # Query user for Dnumber
    print("Enter Dnumber for department to be removed")
    dno = str(input("> "))
    dno_obj = {"Dnumber": dno}

    # Ask for confirmation
    confirm = str(input(f"Are you sure you want to delete {dno}? (y\\n)"))
    if confirm == "n":
        print("No changes have been made")
        return

    # Remove the department
    sql = """
            DELETE FROM DEPARTMENT 
            WHERE Dnumber = %(Dnumber)s
    """

    while True:
        try:
            cursor.execute(sql, dno_obj)
            connection.commit()
            print("Successfully removed department value")
            break
        except Exception as e:
            if "1451" in str(e):
                print(e)
                if _remove_department_dependencies(cursor, connection, dno):
                    continue
            print("Exception caught: " + str(e))
            break


"""
Add department location: Ask for Dnumber. Lock department record. Show all
locations. Ask for a new location and create a new location record.
"""
def add_department_location(cursor, connection):
    
    # Show all locations
    sql = """
            SELECT * FROM DEPT_LOCATIONS
    """
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows: print(row)
    except Exception as e:
        print("Exception caught: " + str(e))
        return

    # Query user for Dnumber
    print("Enter Dnumber to add department location")
    dnumber = str(input("> "))

    # Query for new location 
    print("Enter the name of your new location")
    location = str(input("> "))
    location_obj = {
        "Dnumber": dnumber,
        "Dlocation": location
    }

    # Create new location record
    sql = """
        INSERT INTO DEPT_LOCATIONS
            (Dnumber, Dlocation)
        VALUES 
            (%(Dnumber)s, %(Dlocation)s)
    """
    try: 
        cursor.execute(sql, location_obj)
        connection.commit()
        print("Successfully added new department location")
    except Exception as e:
        print("Exception caught: " + str(e))
        connection.rollback()


"""
Helper function for removing department location
Removes constraints associated with foreign key
"""
def _update_remove_dloc_dependencies(cursor, connection, dnumber, dlocation):
    # Remove all foreign key constraints
    remove_constraint = """
            ALTER TABLE EMPLOYEE 
            DROP FOREIGN KEY employee_ibfk_1
    """
    try:
        cursor.execute(remove_constraint)
        print("Constraints remove")
    except Exception as e:
        print("Exception caught: " + str(e))
        return False

    # Make changes again
    sql = """
            DELETE FROM DEPT_LOCATIONS 
            WHERE Dnumber = %(Dnumber)s AND Dlocation = %(Dlocation)s
    """
    try:
        cursor.execute(sql)
        connection.commit()
        print("Successfully removed department location")
    except Exception as e:
        print("Exception caught delete location: " + str(e))
        connection.rollback()
        return False
    
    # Apply foreign key constraints back
    add_constraints_back = """
            ALTER TABLE Employee
            ADD CONSTRAINT employee_ibfk_1
            FOREIGN KEY (Dno) REFERENCES Dept_locations(Dnumber);
    """
    try:
        cursor.execute(add_constraints_back)
        print("Constraints added back")
    except Exception as e:
        print("Exception caught adding constraints back: " + str(e))
        return False
    
    return True


"""
Remove department location: Ask for Dnumber. Lock department record. Show all
locations. Ask for the location to be removed. Remove the location.
"""
def remove_department_location(cursor, connection):

    # Show all locations
    try:
        sql = "SELECT * FROM DEPT_LOCATIONS"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print("Exception caught while fetching department locations: " + str(e))
        return

    # Query user for Dnumber
    print("Enter Dnumber of department location you want to remove")
    dnumber = str(input("> "))
    
    # Query user for location 
    print("Enter location of department you want to remove")
    location = str(input("> "))

    # Create data object to pass to execute
    data_obj = {
            "Dnumber": dnumber,
            "Dlocation": location
    }

    # Remove location
    sql = """
            DELETE FROM DEPT_LOCATIONS
            WHERE Dnumber = %(Dnumber)s AND Dlocation = %(Dlocation)s
    """
    try: 
        cursor.execute(sql, data_obj)
        connection.commit()
        print("Successfully removed department location")
    except Exception as e:
        if "1451" in str(e):
            if not _update_remove_dloc_dependencies(cursor, connection, dnumber, location):
                pass
        print("Exception caught: " + str(e))
        connection.rollback()


"""
Displays operations that users can select
"""
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
        modify_employee(cursor, connection)

    elif operation == 4:
        print("Removing employee...")
        remove_employee(cursor, connection)

    elif operation == 5:
        print("Adding new dependent...")
        add_new_dependent(cursor, connection)

    elif operation == 6:
        print("Removing dependent...")
        remove_dependent(cursor, connection)

    elif operation == 7:
        print("Adding new department...")
        add_new_department(cursor, connection)

    elif operation == 8:
        print("Viewing department...")
        view_department(cursor)

    elif operation == 9:
        print("Removing department...")
        remove_department(cursor, connection)

    elif operation == 10:
        print("Adding department location...")
        add_department_location(cursor, connection)

    elif operation == 11:
        print("Removing department location...")
        remove_department_location(cursor, connection)

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
        # NOTE: Ignore these error messages, they do not actually affect the code
        connection = pymysql.connect(host='localhost',
                                     user=USERNAME,
                                     password=PASS,
                                     database='Company',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        print("Connection successfully established")
    except:
        print("Connection can't be established")
        print("Ensure that you are connected to your SQL server")
        sys.exit(1)


    # Make changes to the database
    with connection:
        with connection.cursor() as cursor:
            while True: operations(cursor, connection)
