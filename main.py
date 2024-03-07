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
def add_student(conn, cursor):
    first_name = input("Enter their First Name: ")
    last_name = input("Enter their Last Name: ")
    email = input("Enter their email: ")
    enrollment_date = input("Enter their Enrollment Date (Eg. 2023-01-01): ")

    try:
        cursor.execute("INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s)",
                       (first_name, last_name, email, date.fromisoformat(enrollment_date)))
        conn.commit()
        print(f"Successfully created new student: {first_name} {last_name}\n")

    except Exception as e:
        print("failed to create student: " + str(e))

'''
Updates the email address for a student with the specified student_id.
'''
def update_student_email(conn, cursor):
    student_id = input("Enter the ID of the student you would like to update: ")
    new_email = input("Enter the student's new email: ")

    try:
        cursor.execute("""
        UPDATE students
        SET email = (%s)
        WHERE student_id = (%s)
        """, (new_email, student_id))
        conn.commit()

        if cursor.statusmessage.split()[1] == '0':
            print(f"Failed to find student with ID '{student_id}'\n")
        else:
            print(f"Successfully updated student with ID '{student_id}'\n")

    except Exception as e:
        print("failed to delete student: " + str(e))

'''
Deletes the record of the student with the specified student_id.
'''
def delete_student(conn, cursor):
    student_id = input("Enter the ID of the student you would like to delete: ")

    try:
        cursor.execute("DELETE FROM students WHERE student_id = (%s)",
                       (student_id,))
        conn.commit()
        if cursor.statusmessage.split()[1] == '0':
            print(f"Failed to find student with ID '{student_id}'\n")
        else:
            print(f"Successfully deleted student with ID '{student_id}'\n")

    except Exception as e:
        print("failed to delete student: " + str(e))

def main():
    with psycopg.connect("dbname=A3-Q1 user=postgres password=postgres") as conn:
        print("""
        Welcome! What would you like to do?

            1. Get all students
            2. Add a new student
            3. Update the email of a student
            4. Delete a student
            "exit" to quit.
              """)

        with conn.cursor() as cursor:
            while True:
                result = input("> ")

                match result.lower():
                    case '1': get_all_students(cursor)
                    case '2': add_student(conn, cursor)
                    case '3': update_student_email(conn, cursor)
                    case '4': delete_student(conn, cursor)
                    case 'exit' | 'quit' | 'q' : break 

        print("Disconnecting... Have a nice day! 😊")

if __name__ == "__main__":
    main()
