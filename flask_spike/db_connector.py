import mysql.connector


def create_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="mydatabase",
        port=3306
    )

def get_single_user(user_id):
    cnx = create_db_connection()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users where id = %s", (user_id,))
    result = cursor.fetchone()
    print(result)
    return result


def get_all_users():
    cnx = create_db_connection()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    for u in result:
        print(u)
    return result


def insert_user(user_data):
    cnx = create_db_connection()
    cursor = cnx.cursor()
    try:
        insert_query = """INSERT INTO users (name, email) VALUES (%s, %s)"""
        cursor.execute(insert_query, (user_data['name'], user_data['email']))
        cnx.commit()
        print(f'MySQL: inserted with ID={cursor.lastrowid}')
        return {'id': cursor.lastrowid, **user_data}
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
    finally:
        if cnx.is_connected():
            cursor.close()
            cnx.close()
            print("MySQL connection is closed")

if __name__ == '__main__':
    get_single_user(1)
    #get_all_users()
    # insert_user()
