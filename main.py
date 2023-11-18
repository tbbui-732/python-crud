import pymysql.cursors

if __name__ == '__main__':
    # Connect to database
    
    # Establish connection to TA or to personal machine
    is_TA = str(input('Are you a TA? (y\\n)'))
    if is_TA == 'y':
        USER = 'root'
        PASSWORD = ''
    else:
        USER = ''
        PASSWORD = ''

    HOST = 'localhost'
    DATABASE = 'Company'

    connection = pymysql.connect(
                     host = HOST,
                     user = USER,
                     password = PASSWORD,
                     database = DATABASE,
                     charset = 'utf8mb4',
                     cursorclass = pymysql.cursors.DictCursor
                )

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
