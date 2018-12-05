import os
import sys
import sqlite3

FOLDER = 'source'

def get_random_file(db, n):
    con = sqlite3.connect(db)
    cursor = con.cursor()
    for i in range(int(n)):
        file = open(FOLDER + "/" + str(i) + '.js', "w") 
        cursor.execute("SELECT hash FROM repository_source ORDER BY RANDOM() LIMIT 1;")
        row = cursor.fetchall()[0]
        cursor.execute("SELECT source FROM source_file WHERE hash = \'" + row[0] + "\';")
        row = cursor.fetchall()[0]
        file.write(row[0])
        print('copied file ' + str(i))
        file.close()

if __name__ == '__main__':
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)
    get_random_file(sys.argv[1], sys.argv[2])