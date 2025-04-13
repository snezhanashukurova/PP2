import psycopg2
import csv

# Connect to your PostgreSQL database
def connect_db():
    try:
        connection = psycopg2.connect(
            dbname="phonebookdb",  # Replace with your database name
            user="postgres",  # Replace with your PostgreSQL username
            password="12345678",  # Replace with your password
            host="localhost",
            port="5432"
        )
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

# Create the phonebook table with surname, name, and phone
def create_table():
    connection = connect_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS phonebook (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                surname VARCHAR(100),
                phone VARCHAR(20)
            )
        """)
        connection.commit()
        cursor.close()
        connection.close()

# Insert data from a CSV file
def insert_data_from_csv(csv_file):
    connection = connect_db()
    if connection:
        cursor = connection.cursor()
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header
            for row in reader:
                surname, name, phone = row
                cursor.execute("INSERT INTO phonebook (surname, name, phone) VALUES (%s, %s, %s)", (surname, name, phone))
        connection.commit()
        cursor.close()
        connection.close()

# Insert data manually via console
def insert_data_from_console():
    surname = input("Enter surname: ")
    name = input("Enter name: ")
    phone = input("Enter phone number: ")
    connection = connect_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO phonebook (surname, name, phone) VALUES (%s, %s, %s)", (surname, name, phone))
        connection.commit()
        cursor.close()
        connection.close()

# Update data in the phonebook (change surname, name, or phone)
def update_data():
    name = input("Enter the name of the person you want to update: ")
    column = input("Do you want to update surname, name, or phone? ").strip().lower()
    if column not in ["surname", "name", "phone"]:
        print("Invalid column. Only 'surname', 'name', or 'phone' are allowed.")
        return

    new_value = input(f"Enter the new {column}: ")
    connection = connect_db()
    if connection:
        cursor = connection.cursor()
        if column == "surname":
            cursor.execute("UPDATE phonebook SET surname = %s WHERE name = %s", (new_value, name))
        elif column == "name":
            cursor.execute("UPDATE phonebook SET name = %s WHERE name = %s", (new_value, name))
        else:
            cursor.execute("UPDATE phonebook SET phone = %s WHERE name = %s", (new_value, name))
        connection.commit()
        cursor.close()
        connection.close()

# Query data (with different filters)
def query_data():
    try:
        conn = connect_db()
        cur = conn.cursor()

        filter_type = input("Enter filter type (surname/name/phone or press Enter to show all): ").strip()
        filter_value = input("Enter value to search: ").strip() if filter_type else None

        if not filter_type:
            cur.execute("SELECT * FROM phonebook")
        elif filter_type.lower() == "surname":
            cur.execute("SELECT * FROM phonebook WHERE surname ILIKE %s", ('%' + filter_value + '%',))
        elif filter_type.lower() == "name":
            cur.execute("SELECT * FROM phonebook WHERE name ILIKE %s", ('%' + filter_value + '%',))
        elif filter_type.lower() == "phone":
            cur.execute("SELECT * FROM phonebook WHERE phone ILIKE %s", ('%' + filter_value + '%',))
        else:
            print("Invalid filter type.")
            return

        rows = cur.fetchall()
        if rows:
            print("\n--- Phonebook Entries ---")
            for row in rows:
                print(f"Surname: {row[1]}, Name: {row[2]}, Phone: {row[3]}")
        else:
            print("No entries found.")

        cur.close()
        conn.close()

    except Exception as e:
        print("Error querying data:", e)


# Delete data by surname, name, or phone
def delete_data():
    column = input("Do you want to delete by surname, name, or phone? ").strip().lower()
    if column not in ["surname", "name", "phone"]:
        print("Invalid column. Only 'surname', 'name', or 'phone' are allowed.")
        return

    value = input(f"Enter the {column} to delete: ")
    connection = connect_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM phonebook WHERE {column} = %s", (value,))
        connection.commit()
        cursor.close()
        connection.close()

def delete_by_id():
    try:
        id_to_delete = input("Введите ID записи, которую хотите удалить: ")
        connection = connect_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM phonebook WHERE id = %s", (id_to_delete,))
            connection.commit()
            print("Запись удалена.")
            cursor.close()
            connection.close()
    except Exception as e:
        print("Ошибка при удалении по ID:", e)

# Example usage
if __name__ == "__main__":
    create_table()  # Create table once at the start
    while True:
        print("\nOptions:")
        print("1. Insert data from CSV")
        print("2. Insert data manually")
        print("3. Update data")
        print("4. Query data")
        print("5. Delete by")
        print("6. Delete by id")
        print("7. Exit")
        choice = input("Choose an option (1-6): ")
        
        if choice == "1":
            insert_data_from_csv('data.csv')
        elif choice == "2":
            insert_data_from_console()
        elif choice == "3":
            update_data()
        elif choice == "4":
            query_data()
        elif choice == "5":
            delete_data()
        elif choice == "6":
            delete_by_id()
        elif choice == "7":
            break
        else:
            print("Invalid choice. Try again.")
