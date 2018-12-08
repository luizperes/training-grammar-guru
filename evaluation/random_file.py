import os
import sys
import shutil
import sqlite3
import detect

FOLDER = 'source'

def get_random_file(db, n):
    con = sqlite3.connect(db)
    cursor = con.cursor()
    for i in range(int(n)):
        while True:
            cursor.execute("SELECT hash FROM repository_source ORDER BY RANDOM() LIMIT 1;")
            row = cursor.fetchall()[0]
            cursor.execute("SELECT source FROM source_file WHERE hash = \'" + row[0] + "\';")
            row = cursor.fetchall()[0]
            try:
                with detect.synthetic_file(row[0].decode('UTF-8')) as f:
                    tokens = detect.tokenize_file(f)
                file = open(FOLDER + "/" + str(i) + '.js', "w") 
                file.write(detect.tokens_to_source_code(tokens))
                print('copied file ' + str(i))
                file.close()
                break
            except:
                pass

if __name__ == '__main__':
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)
    else:
        shutil.rmtree(FOLDER)
        os.makedirs(FOLDER)
    get_random_file(sys.argv[1], sys.argv[2])
