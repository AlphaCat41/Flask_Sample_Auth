from flask import Flask, request, jsonify
from flaskext.mysql import MySQL
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_DATABASE_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_DATABASE_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_DATABASE_DB')
app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_DATABASE_HOST')

mysql.init_app(app)
conn = mysql.connect()
cursor =conn.cursor()

@app.route('/')
def test():
    cursor.execute("SELECT * from User")
    data = cursor.fetchone()
    cursor.close()

    return 'send token'

@app.route('/signup', methods = ['POST'])
def signup():
    data = request.get_json()
    sql = "INSERT INTO User (username, password) VALUES (%s, %s)"
    value = (data['username'], data['password']) 
    cursor.execute(sql, value)
    conn.commit()
    try:
        cursor.execute(sql, value)
        conn.commit()
    except:
        print("Error: unable to insert the data")

    return 'Successfully registered.'

@app.route('/login', methods = ['POST'])
def login():
    data = request.get_json()
    sql = "SELECT * FROM User WHERE %s"
    condition = ("username = '%s' AND password = '%s'" % (data['username'], data['password']))

    print(sql % condition)
    try:
        cursor.execute(sql % condition)
        data = cursor.fetchone() or []
    except:
        print("Error: unable to fetch data")

    if(len(data) != 0): return "access token" 
    else: return "Cannot find this user"
    # return jsonify({"desired" :list(data)})


if __name__ == '__main__':
    app.run(debug = True)
