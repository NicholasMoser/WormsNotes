'''
Python script to track changes made to Worms 3D Kerfuffle
Run with:
    python db.py create {dir}
    python db.py check {dir}
'''
import os
import sys
import sqlite3
import mmh3

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 3:
        print('Missing command')
        sys.exit(1)
    cmd = sys.argv[1]
    conn = sqlite3.connect('files.db')
    if cmd == 'create':
        if len(sys.argv) < 3:
            print('Missing param')
            sys.exit(1)
        create(conn, sys.argv[2])
    elif cmd == 'check':
        if len(sys.argv) < 3:
            print('Missing param')
            sys.exit(1)
        check(conn, sys.argv[2])
    conn.commit()
    conn.close()

def create(conn, directory):
    ''' Create and populate the database. '''
    create_table(conn)
    populate_table(conn, directory)

def check(conn, directory):
    ''' Check for new, modified, and missing files. '''
    check_new_and_modified(conn, directory)
    check_missing(conn)

def create_table(conn):
    ''' Create a new file table. '''
    cur = conn.cursor()
    cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='file' ''')
    if cur.fetchone()[0]==1:
        return
    sql = '''
      CREATE TABLE file (
      	file_path TEXT,
      	hash TEXT NOT NULL,
        PRIMARY KEY (file_path)
      );
    '''
    cur.execute(sql)

def hash_file(file_path):
    ''' Hash a file. '''
    with open(file_path, mode="rb") as f:
        contents = f.read()
    return mmh3.hash(contents)

def update_file(conn, file_path, hash):
    ''' Update a hash for a file in the database. '''
    cur = conn.cursor()
    insert = 'update file set hash = ? where file_path = ?'
    cur.execute(insert, (hash, file_path))

def insert_file(conn, file_path, hash):
    ''' Insert a file and hash into the database. '''
    cur = conn.cursor()
    insert = """insert or ignore into file(file_path, hash) values (?, ?);"""
    cur.execute(insert, (file_path, hash))

def retrieve_hash(conn, file_path):
    ''' Retrieve a particular file hash. '''
    cur = conn.cursor()
    select = 'select hash from file where file_path = ?'
    cur.execute(select, (file_path,))
    value = cur.fetchall()
    return int(value[0][0]) if value else None

def retrieve_all_file_paths(conn):
    ''' Retrieve all file paths. '''
    cur = conn.cursor()
    select = 'select file_path from file'
    cur.execute(select)
    return cur.fetchall()

def populate_table(conn, path):
    ''' Populate the file table. '''
    for root, _, files in os.walk(path):
        print(root)
        conn.commit()
        for file in files:
            try:
                file_path = os.path.join(root, file)
                hash = hash_file(file_path)
                insert_file(conn, file_path, hash)
            except Exception as e:
                print(file_path)
                print(e)

def check_new_and_modified(conn, directory):
    ''' Check for new and modified files. '''
    for root, _, files in os.walk(directory):
        conn.commit()
        for file in files:
            try:
                file_path = os.path.join(root, file)
                new_hash = hash_file(file_path)
                old_hash = retrieve_hash(conn, file_path)
                if old_hash == None:
                    print(f'New file: {file_path}')
                elif new_hash != old_hash:
                    print(f'Different file found: {file_path}')
            except Exception as e:
                print(f'Error with {file_path}')
                print(e)

def check_missing(conn):
    ''' Check for missing files. '''
    for file_path in retrieve_all_file_paths(conn):
        if not os.path.isfile(file_path[0]):
            print(f'Missing: {file_path[0]}')

if __name__ == '__main__':
    main()
