#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Tables:
# ----------------------
# Table meta | language | mined
# ----------------------
# Table repository | name | link | hash | date | License
# ----------------------
# Table source-file | hash | code
# ----------------------
# ....
# ----------------------

# The number of repos download was 8400

import sqlite3
import sys

if __name__ == "__main__":
    dbname = sys.argv[1]
    con = sqlite3.connect(dbname)
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("----------------------")
    for tbl in tables:
        print("Table " + tbl[0] + " |")
        cursor.execute("SELECT * FROM "+tbl[0]+";")
        for description in cursor.description:
            print(" " + description[0] + " |")
        print ("----------------------")