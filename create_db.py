import sqlite3

# Connect to (or create) a local database file
conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

# Create a table and add some sample data
cursor.execute('''CREATE TABLE IF NOT EXISTS products 
                  (id INTEGER PRIMARY KEY, name TEXT, price REAL, stock INTEGER)''')

cursor.execute("INSERT INTO products (name, price, stock) VALUES ('Laptop', 1200.00, 10)")
cursor.execute("INSERT INTO products (name, price, stock) VALUES ('Mouse', 25.50, 50)")

conn.commit()
conn.close()
print("Local database 'inventory.db' created with sample data.")