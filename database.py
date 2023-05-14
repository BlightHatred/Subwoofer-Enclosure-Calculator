#!/usr/bin/python3
import sqlite3

conn = sqlite3.connect('subwoofer_drivers.db')
cursor = conn.cursor()

create_statement = '''CREATE TABLE IF NOT EXISTS speakers(
            name VARCHAR, 
            qts VARCHAR,
            vas VARCHAR, 
            fs INT,
            sd VARCHAR,
            xmax VARCHAR
            );'''

cursor.execute(create_statement)


def db_add(name, vas, qts, fs, sd, xmax):
    add_statement = f'''INSERT INTO speakers 
                        VALUES{name, 
                               vas, 
                               qts,
                               fs, 
                               sd, 
                               xmax, 
                               }'''
    cursor.execute(add_statement)
    conn.commit()

def db_get():
    get_statement = f'''SELECT *
                        FROM speakers'''
    cursor.execute(get_statement)
    return cursor.fetchall()

def db_remove(name):
    remove_statement = f'''DELETE FROM speakers
                           WHERE name = '{name}';'''
    cursor.execute(remove_statement)
    conn.commit()




