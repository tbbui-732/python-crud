import os
from os.path import join, dirname
import pymysql.cursors
from dotenv import load_dotenv
import sys

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


    '''
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
    '''
