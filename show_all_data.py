import sqlite3

# Connect to the database
conn = sqlite3.connect('instance/library.db')
cursor = conn.cursor()

# Check all tables more thoroughly
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cursor.fetchall()]

print("All tables:", tables)
print()

# Show all data from all tables
for table in tables:
    print(f"\n{'='*50}")
    print(f"Table: {table}")
    print('='*50)
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    
    # Get column names
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [col[1] for col in cursor.fetchall()]
    print("Columns:", ", ".join(columns))
    print(f"Total rows: {len(rows)}")
    
    if rows:
        print("\nData:")
        for i, row in enumerate(rows, 1):
            print(f"  Row {i}: {row}")
    else:
        print("  (empty)")

conn.close()
