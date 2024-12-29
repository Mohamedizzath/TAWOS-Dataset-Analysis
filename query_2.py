import mysql.connector
from db_connect import connect_to_database

def print_tables():
    connection = connect_to_database()
    if connection is not None:
        try:
            # Create a cursor to interact with the database
            cursor = connection.cursor()
            
            # Execute query to fetch all data in project in the database
            # cursor.execute("SELECT * FROM issue where project_ID = 1;")
            # cursor.execute("SELECT count(DISTINCT sprint_ID) FROM issue;")
            # cursor.execute("SELECT DISTINCT (sprint_ID) FROM issue;")
            # cursor.execute("SELECT * FROM change_log where Field = 'assignee' limit 100;")
            cursor.execute("SELECT count(DISTINCT Status) FROM Issue;")
            
            
            
             # Fetch column names
            columns = [column[0] for column in cursor.description]

            # Fetch all data
            issue = cursor.fetchall()

            if issue:
                # Print column names
                print("\n issue table Column Names:", columns)
                
                # Print the project table data
                print("\n issue Table Data:")
                for project in issue:
                    print(project)
            else:
                print("No Projects found in the database.")


        except mysql.connector.Error as e:
            print("Error fetching tables:", e)

        finally:
            # Ensure that the cursor and connection are closed
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")

if __name__ == "__main__":
    print_tables()
