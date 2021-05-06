from mysql.connector import MySQLConnection, Error
from dbconfig import read_db_config
from time import time

table_name = 'imonmarsbot'

#переписать весь код на dictionary=True

# CHECK - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_user(uid):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query = f'SELECT *  ' \
            f'FROM {table_name} ' \
            f'WHERE uid = "{uid}" ' \
            f'LIMIT 1'
    try:
        cursor.execute(query)
        rows = cursor.fetchone()
        print(f'[DataBase] --> {rows} (check_user)')
        return rows
    except Error as e:
        print(f'[DataBase] ERR: {e} (check_user)')
        pass
    finally:
        cursor.close()
        conn.close()

# ADD - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def add_user(uid, username):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query = f"INSERT INTO {table_name} (uid, username) " \
            f"VALUES ('{uid}', '{username}')"
    try:
        cursor.execute(query)
        conn.commit()
        print(f'[DataBase] --> (add_user)')
    except Error as e:
        print(f'[DataBase] ERR: {e} (add_user)')
        pass
    finally:
        cursor.close()
        conn.close()

# UPDATE - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def update_language(uid, lang):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query = f'UPDATE {table_name} ' \
            f'SET lang = "{lang}" ' \
            f'WHERE uid = "{uid}" ' \
            f'LIMIT 1'
    try:
        cursor.execute(query)
        conn.commit()
        print(f'[DataBase] --> (update_language)')
    except Error as e:
        print(f'[DataBase] ERR: {e} (update_language)')
        pass
    finally:
        cursor.close()
        conn.close()

def update_attractions(uid, attractions):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query = f'UPDATE {table_name} ' \
            f'SET attractions = "{attractions}" ' \
            f'WHERE uid = "{uid}" ' \
            f'LIMIT 1'
    try:
        cursor.execute(query)
        conn.commit()
        print(f'[DataBase] --> (update_attractions)')
    except Error as e:
        print(f'[DataBase] ERR: {e} (update_attractions)')
        pass
    finally:
        cursor.close()
        conn.close()

# GET - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_language(uid):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query = f'SELECT lang ' \
            f'FROM {table_name} ' \
            f'WHERE uid = {uid} ' \
            f'LIMIT 1'
    try:
        cursor.execute(query)
        rows = cursor.fetchone()
        print(f'[DataBase] --> {rows} (get_language)')
        return rows
    except Error as e:
        print(f'[DataBase] ERR: {e} (get_language)')
    finally:
        cursor.close()
        conn.close()

def get_attractions(uid):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()

    query = f'SELECT attractions ' \
            f'FROM {table_name} ' \
            f'WHERE uid = {uid} ' \
            f'LIMIT 1'
    try:
        cursor.execute(query)
        rows = cursor.fetchone()
        print(f'[DataBase] --> {rows} (get_language)')
        return rows
    except Error as e:
        print(f'[DataBase] ERR: {e} (get_language)')
    finally:
        cursor.close()
        conn.close()

# ADD INFO ABOUT USER GEO

def add_info_about_geo(uid, gradus_x, gradus_y):
    dbconfig = read_db_config()
    conn = MySQLConnection(**dbconfig)
    cursor = conn.cursor()
    info_about_geo = f'{int(time())} {gradus_x} {gradus_y}'

    query = f'UPDATE {table_name} ' \
            f'SET geo_info = CONCAT(geo_info, "{info_about_geo}") ' \
            f'WHERE uid = {uid} ' \
            f'LIMIT 1'
    try:
        cursor.execute(query)
        conn.commit()
        print(f'[DataBase] --> (add_info_about_geo)')
    except Error as e:
        print(f'[DataBase] ERR: {e} (add_info_about_geo)')
        pass
    finally:
        cursor.close()
        conn.close()