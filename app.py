from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'crud_demo_db'

mysql = MySQL(app)

# Routes
@app.route('/', methods=['GET'])
def home():
    return jsonify("connection successfully")

@app.route('/create-db', methods=['POST'])
def create_db():
    data = request.get_json()
    db_name = data["dbname"]
    cur = mysql.connection.cursor()
    cur.execute(f"create database {db_name}")
    
    mysql.connection.commit()
    print(cur)
    cur.close()
    return jsonify({'message': 'User created successfully'})

@app.route('/users', methods=['GET'])
def get_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    return jsonify(users)


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    if user:
        return jsonify(user)
    else:
        return jsonify({'message': 'User not found'})

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data['name']
    email = data['email']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'User created successfully'})

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    name = data['name']
    email = data['email']

    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (name, email, user_id))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'User updated successfully'})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'User deleted successfully'})

# Run the application
if __name__ == '__main__':
    app.run()
