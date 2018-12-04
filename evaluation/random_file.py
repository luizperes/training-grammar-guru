import sqlite3
import sys

def get_random_file(db):
    con = sqlite3.connect(db)
    cursor = con.cursor()
    cursor.execute("SELECT hash FROM repository_source ORDER BY RANDOM() LIMIT 1;")
    row = cursor.fetchall()[0]
    cursor.execute("SELECT source FROM source_file WHERE hash = \'" + row[0] + "\';")
    row = cursor.fetchall()[0]
    return str(row[0])