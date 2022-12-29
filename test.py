from flask import Flask, request, jsonify
from flaskext.mysql import MySQL
from dotenv import load_dotenv
from  werkzeug.security import generate_password_hash, check_password_hash
import os

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

def search(username):
    sql = "SELECT * FROM User WHERE %s"
    condition = ("username = '%s' LIMIT 1" % (username))
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

    return 'send token'

@app.route('/signup', methods = ['POST'])
def signup():
    data = request.get_json()
    user = search(data['username'])
    # Not have user yet
    if(len(user) == 0):
        password = generate_password_hash(data['password'])
        insert(data['username'], password)
        return 'Successfully registered.'
    username = user[0]
    if(data['username'] == username): 
        return 'The user has already registered.' 
    return 'Cannot register'

@app.route('/login', methods = ['POST'])
def login():
    data = request.get_json()
    user = search(data['username'])
    if(len(user) == 0):
        return "Cannot find this user"
    username = user[0]
    password = user[1]
    if(data['username'] == username and check_password_hash(password, data['password'])): 
        return "access token" 
    return 'Cannot login'
    # return jsonify({"desired" :list(data)})

if __name__ == '__main__':
    app.run(debug = True)
