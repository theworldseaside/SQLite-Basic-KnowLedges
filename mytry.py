import sqlite3
import os


class DataBase():
    def __init__(self, dbname='database'):

        self.dbname = dbname
        self.cursor = None
        self.connection = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.dbname)
            self.cursor = self.connection.cursor()
            print("DataBase was connected")
        except sqlite3.Error as error:
            print("DataBase was not connected, reason: ", error)





    def Create(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS database(
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    height INTEGER,   
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
                                )
                                ''')
            self.connection.commit()
            print("Table was successfully")
        except sqlite3.Error as error:
            print("Table was not created , reason: ",error)
            


    def add_data(self,name,height):
        try:
            self.cursor.execute(
            "INSERT INTO database(name,height) VALUES (?,?)" ,
            (name,height)
            )
            self.connection.commit()
            print("Data was added successfully")
            return True
        except sqlite3.Error as error:
            print("Data was not added, reason: ", error)
            return False

    def delete_data(self,data_id):
        try:
            self.cursor.execute(
                "SELECT * FROM database WHERE id = ?", (data_id)
            )
            if not self.cursor.fetchone():
                print('No data found with this id')
                return False
            
            self.cursor.execute(
                "DELETE FROM database WHERE id = ?", (data_id)
            )
            self.connection.commit()
            print("Data was deleted successfully")
            return True
        except sqlite3.Error as error:
            print("Data was not deleted ,reason: ", error)
            return False
        
    def view(self):
        try:
            self.cursor.execute(
                "SELECT * FROM database"
            )

            rows = self.cursor.fetchall()

            if not rows:
                print("No data found")
                return 
            
            for row in rows:
                print(row)
                return True
            
        except sqlite3.Error as error:
            print("Data cannot be showed, reason: ", error)
    
    def close(self):
        try:
            self.connection.close()
            print("DataBase was closed")
        except sqlite3.Error as error:
            print("DataBase was not closed, reason: ", error)



def main():
    db = DataBase()
    db.connect()
    db.Create()

    while True:
        print(
            "1) Add Data\n2) Delete Data\n3) Show data\n4) Exit\n"
        )

        choice = int(input("Choice: "))

        if choice == 1:
            print("\n---Add Data---")

            name = str(input("Name: "))
            height = str(input("Height: "))
            db.add_data(name,height)

        elif choice == 2:
            print("\n---Delete Data---")

            db.view()

            try:
                data_id = int(input("What you want to delete?: "))
                db.delete_data(data_id)
            except sqlite3.Error as error:
                print("Enter a valid number")

        elif choice == 3:
            print("\n---View---")

            db.view()
        elif choice == 4:
            print("\n---GoodBye---")
            break
        else:
            exit()

    
if __name__ == '__main__':
    main()