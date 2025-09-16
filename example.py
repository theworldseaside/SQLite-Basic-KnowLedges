import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name="testing.db"):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Connect to the SQLite database"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print(f"Connected to database: {self.db_name}")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
    
    def create_table(self):
        """Create a sample table if it doesn't exist"""
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    age INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.connection.commit()
            print("Table 'users' created successfully")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
    
    def add_data(self, name, email, age):
        """Add new data to the database"""
        try:
            self.cursor.execute(
                "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                (name, email, age)
            )
            self.connection.commit()
            print(f"Data added successfully! ID: {self.cursor.lastrowid}")
            return True
        except sqlite3.IntegrityError:
            print("Error: Email already exists!")
            return False
        except sqlite3.Error as e:
            print(f"Error adding data: {e}")
            return False
    
    def delete_data(self, data_id):
        """Delete data from the database by ID"""
        try:
            # Check if the record exists
            self.cursor.execute("SELECT * FROM users WHERE id = ?", (data_id,))
            if not self.cursor.fetchone():
                print(f"No record found with ID: {data_id}")
                return False
            
            self.cursor.execute("DELETE FROM users WHERE id = ?", (data_id,))
            self.connection.commit()
            print(f"Data with ID {data_id} deleted successfully!")
            return True
        except sqlite3.Error as e:
            print(f"Error deleting data: {e}")
            return False
    
    def view_all_data(self):
        """View all data in the database"""
        try:
            self.cursor.execute("SELECT * FROM users")
            rows = self.cursor.fetchall()
            
            if not rows:
                print("No data found in the database.")
                return
            
            print("\n" + "="*60)
            print("ID\tName\t\tEmail\t\t\tAge\tCreated At")
            print("="*60)
            for row in rows:
                print(f"{row[0]}\t{row[1]:<15}\t{row[2]:<20}\t{row[3]}\t{row[4]}")
            print("="*60)
            
        except sqlite3.Error as e:
            print(f"Error viewing data: {e}")
    
    def search_data(self, search_term):
        """Search for data by name or email"""
        try:
            self.cursor.execute(
                "SELECT * FROM users WHERE name LIKE ? OR email LIKE ?",
                (f'%{search_term}%', f'%{search_term}%')
            )
            rows = self.cursor.fetchall()
            
            if not rows:
                print(f"No results found for: {search_term}")
                return
            
            print(f"\nSearch results for '{search_term}':")
            print("="*60)
            print("ID\tName\t\tEmail\t\t\tAge")
            print("="*60)
            for row in rows:
                print(f"{row[0]}\t{row[1]:<15}\t{row[2]:<20}\t{row[3]}")
            print("="*60)
            
        except sqlite3.Error as e:
            print(f"Error searching data: {e}")
    
    def close(self):
        """Close the database connection"""
        if self.connection:
            self.connection.close()
            print("Database connection closed.")

def main():
    db = DatabaseManager()
    db.connect()
    db.create_table()
    
    while True:
        print("\n" + "="*40)
        print("DATABASE MANAGEMENT SYSTEM")
        print("="*40)
        print("1. Add Data")
        print("2. Delete Data")
        print("3. View All Data")
        print("4. Search Data")
        print("5. Exit")
        print("="*40)
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            print("\n--- ADD NEW DATA ---")
            name = input("Enter name: ").strip()
            email = input("Enter email: ").strip()
            age = input("Enter age: ").strip()
            
            if not name or not email:
                print("Name and email are required!")
                continue
            
            try:
                age = int(age) if age else None
            except ValueError:
                print("Age must be a number!")
                continue
            
            db.add_data(name, email, age)
            
        elif choice == '2':
            print("\n--- DELETE DATA ---")
            db.view_all_data()
            try:
                data_id = int(input("Enter ID to delete: ").strip())
                if input("Are you sure? (y/n): ").lower() == 'y':
                    db.delete_data(data_id)
            except ValueError:
                print("Please enter a valid ID number!")
                
        elif choice == '3':
            print("\n--- ALL DATA ---")
            db.view_all_data()
            
        elif choice == '4':
            print("\n--- SEARCH DATA ---")
            search_term = input("Enter name or email to search: ").strip()
            db.search_data(search_term)
            
        elif choice == '5':
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice! Please try again.")
    
    db.close()

if __name__ == "__main__":
    main()