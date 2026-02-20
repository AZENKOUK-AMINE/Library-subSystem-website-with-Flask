import sqlite3

# Connect to the database
conn = sqlite3.connect('instance/library.db')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cursor.fetchall()]
print("Tables in database:", tables)
print()

# For each table, show its structure
for table in tables:
    print(f"\n=== Table: {table} ===")
    cursor.execute(f"PRAGMA table_info({table})")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
    
    # Show row count
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"  Total rows: {count}")
    
    # If it's feedback table, show some data
    if 'feedback' in table.lower():
        print(f"\n  Sample data from {table}:")
        cursor.execute(f"SELECT * FROM {table} LIMIT 3")
        rows = cursor.fetchall()
        for row in rows:
            print(f"    {row}")

conn.close()
