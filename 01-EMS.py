# -- Employee Management System --

import mysql.connector
import hashlib

# -- MySQL Database Manageement Class --
class DatabaseManager:
    def __init__(self):
      self.connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='mradul2718'
        )
      self.cursorObject = self.connection.cursor()  
      self.cursorObject.execute("CREATE DATABASE IF NOT EXISTS company")
      self.cursorObject.execute("USE company")
      users='''CREATE TABLE IF NOT EXISTS users (
      username VARCHAR(50),
      password VARCHAR(100)
      );'''
      employees='''CREATE TABLE IF NOT EXISTS employees (
      name VARCHAR(50), 
      age INT, 
      department VARCHAR(50), 
      salary FLOAT
      );'''
      self.cursorObject.execute(users)
      self.cursorObject.execute(employees)

    def commit(self):
          self.connection.commit()

    def close(self):
          self.connection.close()

# -- User Manageement Class --
class User:
    def __init__(self, db):
      self.db = db
        
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register(self):
        username= input("\nChoose username: ")
        password= self.hash_password(input("Choose password: "))
        try:
            self.db.cursorObject.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            self.db.commit()
            print("\nUser registered successfully!")
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            
    def login(self):
        username = input("\nUsername: ")
        password = self.hash_password(input("Password: "))
        self.db.cursorObject.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        result = self.db.cursorObject.fetchone()
        if result:
            print("Login successful!")
            return True
        else:
            print("Invalid username or password.")
            return False
        
# -- Employee Manageement Class --
class Employee:
    def __init__(self, db):
        self.db = db

    def add(self):
        name = input("Name: ")
        age = int(input("Age: "))
        dept = input("Department: ")
        salary = int(input("Salary: "))
        self.db.cursorObject.execute(
            "INSERT INTO employees (name, age, department, salary) VALUES (%s, %s, %s, %s)",
            (name, age, dept, salary)
        )
        self.db.commit()
        print("Employee added.")

    def view_all(self):
        self.db.cursorObject.execute("SELECT * FROM employees")
        for row in self.db.cursorObject.fetchall():
            print(row)

    def search(self):
        name = input("Enter Name of Employee: ")
        self.db.cursorObject.execute("SELECT * FROM employees WHERE name=%s", (name,))
        result = self.db.cursorObject.fetchone()
        if result:
            print(result)
        else:
            print("Employee not found.")

    def update(self):
        name = input("Name of Employee: ")
        age = int(input("New age: "))
        dept = input("New department: ")
        salary = float(input("New salary: "))
        self.db.cursorObject.execute("""
            UPDATE employees SET name=%s, age=%s, department=%s, salary=%s WHERE name=%s
        """, (name, age, dept, salary, name))
        self.db.commit()
        print("Employee updated.")

    def delete(self):
        name = input("Employee name to delete: ")
        self.db.cursorObject.execute("DELETE FROM employees WHERE name=%s", (name,))
        self.db.commit()
        print("Employee deleted.")

# -- Main App --
class App:
    def __init__(self):
        self.db = DatabaseManager()
        self.user = User(self.db)
        self.employee = Employee(self.db)

    def main_menu(self):
        while True:
            print('''\n--- Employee Management Menu ---
      
1. Add Employee
2. View All Employees
3. Search Employee
4. Update Employee
5. Delete Employee
6. Logout
      ''')
            choice = input("Select: ")

            if choice == '1':
                self.employee.add()
            elif choice == '2':
                self.employee.view_all()
            elif choice == '3':
                self.employee.search()
            elif choice == '4':
                self.employee.update()
            elif choice == '5':
                self.employee.delete()
            elif choice == '6':
                break
            else:
                print("Invalid choice.")

    def run(self):
        while True:
            print('''
1. Login
2. Register
3. Exit
                  ''')
            choice = input("Choose: ")
            if choice == '1' and self.user.login():
                self.main_menu()
            elif choice == '2':
                self.user.register()
            elif choice == '3':
                self.db.close()
                break
            else:
                print("Invalid option.")

# -- Run the App --
if __name__ == "__main__":
    app = App()
    app.run()
