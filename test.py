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

def search(username, password):
    sql = "SELECT * FROM User WHERE %s"
    condition = ("username = '%s' AND password = '%s'" % (username, password))
    cursor.execute(sql % condition)
    data = cursor.fetchone() or []
    return data

def insert(username, password):
    sql = "INSERT INTO User (username, password) VALUES (%s, %s)"
    value = (username, password) 
    cursor.execute(sql, value)
    conn.commit()

@app.route('/')
def test():
    cursor.execute("SELECT * from User")
    data = cursor.fetchone()
    cursor.close()

    return 'send token'

@app.route('/signup', methods = ['POST'])
def signup():
    data = request.get_json()
    if(len(search(data['username'], data['password'])) != 0): 
        return 'This user has been signup'
    
    try:
        insert(data['username'], data['password'])
    except:
        print("Error: unable to insert the data")

    return 'Successfully registered.'

@app.route('/login', methods = ['POST'])
def login():
    data = request.get_json()

    try:
        data = search(data['username'], data['password'])
    except:
        print("Error: unable to fetch data")

    if(len(data) != 0): 
        return "access token" 
    return "Cannot find this user"
    # return jsonify({"desired" :list(data)})


if __name__ == '__main__':
    app.run(debug = True)
