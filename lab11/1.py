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


#CREATE OR REPLACE FUNCTION search_by_pattern(p_pattern TEXT)
#RETURNS TABLE(id INT, surname VARCHAR, name VARCHAR, phone VARCHAR) AS $$
#BEGIN
#   RETURN QUERY
#   SELECT pb.id, pb.surname, pb.name, pb.phone
#    FROM phonebook pb
#    WHERE pb.name ILIKE '%' || p_pattern || '%'
#       OR pb.surname ILIKE '%' || p_pattern || '%'
#       OR pb.phone ILIKE '%' || p_pattern || '%';
#END;
#$$ LANGUAGE plpgsql;

#Поиск по паттерну через SQL-функцию
def search_by_pattern():
    pattern = input("Enter pattern to search (name, surname or phone): ")
    connection = connect_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM search_by_pattern(%s)", (pattern,))
        rows = cursor.fetchall()
        if rows:
            print("\n--- Search Results ---")
            for row in rows:
                print(f"ID: {row[0]}, Surname: {row[1]}, Name: {row[2]}, Phone: {row[3]}")
        else:
            print("No matches found.")
        cursor.close()
        connection.close()


""""
CREATE OR REPLACE PROCEDURE add_or_update_user(p_name VARCHAR, p_surname VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM phonebook WHERE name = p_name AND surname = p_surname
    ) THEN
        UPDATE phonebook
        SET phone = p_phone
        WHERE name = p_name AND surname = p_surname;
    ELSE
        INSERT INTO phonebook(name, surname, phone)
        VALUES (p_name, p_surname, p_phone);
    END IF;
END;
$$;
"""

# Добавление/обновление пользователя через процедуру
def add_or_update_user():
    surname = input("Enter surname: ")
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    connection = connect_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("CALL add_or_update_user(%s, %s, %s)", (name, surname, phone))
        connection.commit()
        print("User added or updated.")
        cursor.close()
        connection.close()
"""
CREATE OR REPLACE PROCEDURE delete_user_by_name_or_phone(p_value VARCHAR)
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE name = p_value OR surname = p_value OR phone = p_value;
END;
$$ LANGUAGE plpgsql;"""

# Удаление пользователя по имени, фамилии или телефону
def delete_user_by_name_or_phone():
    value = input("Enter name, surname or phone to delete: ")
    connection = connect_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("CALL delete_user_by_name_or_phone(%s)", (value,))
        connection.commit()
        print("User deleted if match found.")
        cursor.close()
        connection.close()



if __name__ == "__main__":
    create_table()  # Create table once at the start
    while True:
        print("\nOptions:")
        print("1. Insert data from CSV")
        print("2. Insert data manually")
        print("3. Update data")
        print("4. Search by pattern")
        print("5. Add or update user")
        print("6. Delete by name or phone")
        print("7. Exit")

        choice = input("Choose an option (1-7): ")
        # Menu
        if choice == "1":
            insert_data_from_csv('data.csv')
        elif choice == "2":
            insert_data_from_console()
        elif choice == "3":
            update_data()
        elif choice == "4":
            search_by_pattern()
        elif choice == "5":
            add_or_update_user()
        elif choice == "6":
            delete_user_by_name_or_phone()
        elif choice == "7":
            break
        else:
            print("Invalid choice. Try again.")












