import psycopg
from datetime import date


'''
Retrieves and displays all records from the students table.
'''
def get_all_students(cursor):
    cursor.execute("SELECT * FROM students")
    print("Student ID, First Name, Last Name, Email, Enrollment Date")
    for record in cursor:
        print(", ".join(map(str, record)))
    print()
    
'''
Inserts a new student record into the students table.
'''
def add_student(cursor, first_name: str, last_name: str, email: str, enrollment_date: str):
    cursor.execute("INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s)",
                  (first_name, last_name, email, date.fromisoformat(enrollment_date)))

'''
Updates the email address for a student with the specified student_id.
'''
def update_student_email(cursor, student_id: str, new_email: str):
    return

'''
Deletes the record of the student with the specified student_id.
'''
def delete_student(cursor, student_id: str):
    cursor.execute("DELETE FROM students WHERE student_id = (%s)",
                  (student_id,))

def main():
    with psycopg.connect("dbname=A3-Q1 user=postgres password=postgres") as conn:
        print("""
        Welcome! What would you like to do?

            1. Get all students
            2. Add a new student
            3. Update the email of a student
            4. Delete a student

        type "exit" to quit.
              """)

        with conn.cursor() as cursor:
            while True:
                result = input("> ")

                match result.lower():
                    case '1':
                        get_all_students(cursor)
                    case '2':
                        first_name = input("Enter their First Name: ")
                        last_name = input("Enter their Last Name: ")
                        email = input("Enter their email: ")
                        enrollment_date = input("Enter their Enrollment Date (Eg. 2023-01-01): ")

                        try:
                            add_student(cursor, first_name, last_name, email, enrollment_date)
                            conn.commit()
                            print(f"Successfully created new student: {first_name} {last_name}\n")
                        except Exception as e:
                            print("failed to create student: " + str(e))

                    case '3':
                        pass
                    case '4':
                        id = input("Enter the ID of the student you would like to delete: ")
                        try:
                            delete_student(cursor, id)
                            conn.commit()
                            print(f"Success!\n")
                        except Exception as e:
                            print("failed to delete student: " + str(e))
                    case 'exit':
                       break 


        print("Disconnecting")

if __name__ == "__main__":
    main()
