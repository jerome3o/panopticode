import json
import sqlite3

# Configure DB connection
db_file = 'data/diary.db'
data_file = 'diary.json'

conn = sqlite3.connect(db_file)
c = conn.cursor()

# Open the JSON file
with open(data_file) as f:
    data = json.load(f)

# Insert each object into the DB  
for i, obj in enumerate(data):
    c.execute('INSERT INTO reports (id, data) VALUES (?, ?)', (i + 2000, json.dumps(obj)))

conn.commit()
conn.close()

