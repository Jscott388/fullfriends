from flask import Flask, request, redirect, render_template
from mysqlconnection import MySQLConnector


app = Flask(__name__)
mysql = MySQLConnector(app, 'fullfriends')


queries = {
    'create': "INSERT INTO friends (first_name, last_name, email, created_at, updated_at) VALUES (:first_name, :last_name, :email, NOW(), NOW());",
    'index': "SELECT * FROM friends",
    'delete': "DELETE FROM friends WHERE id = :id",
    'getuser': "SELECT * FROM friends WHERE id = :id",
    'update': "UPDATE friends SET first_name= :first_name, last_name= :last_name, email= :email, updated_at = NOW() WHERE id = :id"
}


@app.route('/', methods=['GET'])
def index():
    query = queries['index']
    data = {}
    friends = mysql.query_db(query, data)
    return render_template('index.html', friends=friends)


@app.route('/friends', methods=['POST'])
def create():

    query = queries['create']
    data = {
            'first_name' : request.form['first_name'],
            'last_name' : request.form['last_name'],
            'email' : request.form['email']
    }
    mysql.query_db(query, data)

    return redirect('/')

@app.route('/friends/<id>', methods=['POST'])
def update(id):
    query = queries['update']
    data = {
            'id': id,
            'first_name' : request.form['first_name'],
            'last_name' : request.form['last_name'],
            'email' : request.form['email']

    }
    mysql.query_db(query, data)
    return redirect('/')

@app.route('/friends/<id>/edit', methods=['GET'])
def edit(id):
    query = queries['getuser']
    data = {'id': id}
    friend = mysql.query_db(query, data)[0]
    return render_template('/edit.html', friend=friend)


@app.route('/friends/<id>/delete', methods=['POST'])
def destory(id):
    query = queries['delete']
    data = {'id': id}
    mysql.query_db(query, data)
    return redirect('/')
app.run(debug=True)
