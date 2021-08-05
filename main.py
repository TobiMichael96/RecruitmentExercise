import sqlite3
from flask import Flask, request

app = Flask(__name__)

DATABASE_PATH = "persons.sqlite"


@app.route('/person', methods=['PUT', 'POST'])
def add_user():
    req = request.json

    if 'name' not in req and 'age' not in req:
        return {"success": "false"}, 400
    elif 'name' not in req:
        return {"success": "false"}, 400
    elif 'age' not in req:
        return {"success": "false"}, 400
    elif 'name' in req and 'age' in req:
        name = req['name']
        age = req['age']

    if not isinstance(age, int):
        return {"success": "false"}, 400

    with sqlite3.connect("person.sqlite") as con:
        cursor = con.cursor()
        cursor.execute("INSERT INTO persons VALUES(?, ?);", (name, age))
        con.commit()
    return {
        "success": "true",
        "name": name
    }


@app.route('/person/<name>')
def get_user(name):
    with sqlite3.connect(DATABASE_PATH) as con:
        cursor = con.cursor()
        cursor.execute('SELECT * FROM persons WHERE name=?', (name,))
        row = cursor.fetchone()

    if row is None:
        return {"success": "false"}, 404

    return {
        "name": row[0],
        "age": row[1]
    }


@app.route('/person')
def get_users():
    with sqlite3.connect(DATABASE_PATH) as con:
        cursor = con.cursor()
        cursor.execute('SELECT * FROM persons')
        rows = cursor.fetchall()
        names = list(map(lambda x: x[0], cursor.description))

    pers_list = {}
    for row in rows:
        pers = {
            names[0]: row[0],
            names[1]: row[1]
        }
        pers_list[len(pers_list)] = pers

    return {"persons": pers_list}


@app.route('/person/<name>')
def delete_user(name):
    with sqlite3.connect(DATABASE_PATH) as con:
        cursor = con.cursor()
        rowcount = cursor.execute('DELETE FROM persons WHERE name=?', (name,)).rowcount
        con.commit()

    if rowcount == 0:
        return {"success": "false"}, 404

    return {
        "success": "true",
        "name": name,
        "deletedPersons": rowcount
    }


if __name__ == '__main__':
    # Create a SQL connection to our SQLite database
    conn = sqlite3.connect(DATABASE_PATH)

    cur = conn.cursor()
    cur.execute('CREATE TABLE persons (name VARCHAR(255), age INTEGER);')
    cur.close()
    conn.commit()
    conn.close()
    app.run(port=5000, host='0.0.0.0')
