import mysql.connector
from db_connect import connect_to_database

def print_tables():
    connection = connect_to_database()
    if connection is not None:
        try:
            # Create a cursor to interact with the database
            cursor = connection.cursor()

            # Execute query to fetch all tables in the database
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()

            if tables:
                print("Tables in database:")
                for table in tables:
                    print(table[0])
            else:
                print("No tables found in the database.")

            
            # Execute query to fetch all data in project in the database
            cursor.execute("SELECT * FROM project;")
             # Fetch column names
            columns = [column[0] for column in cursor.description]

            # Fetch all data
            projects = cursor.fetchall()

            if projects:
                # Print column names
                print("\nColumn Names:", columns)
                
                # Print the project table data
                print("\nProject Table Data:")
                for project in projects:
                    print(project)
            else:
                print("No Projects found in the database.")
                
            
            # Execute query to fetch all data in project in the database
            # cursor.execute("SELECT Distinct(ID) FROM user;")
            cursor.execute("SELECT COUNT(DISTINCT ID) FROM user;")
            
             # Fetch column names
            columns = [column[0] for column in cursor.description]

            # Fetch all data
            users = cursor.fetchall()

            if users:
                # Print column names
                print("\nColumn Names:", columns)
                
                # Print the project table data
                print("\nuser Table Data:")
                for user in users:
                    print(user)
            else:
                print("No users found in the database.")


        except mysql.connector.Error as e:
            print("Error fetching tables:", e)

        finally:
            # Ensure that the cursor and connection are closed
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")

if __name__ == "__main__":
    print_tables()
