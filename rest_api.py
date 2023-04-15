from flask import Flask, jsonify,request
from flask_restful import Resource, Api
import mysql.connector

app = Flask(__name__)
# Create an API object
api = Api(app)

host = "eu-cdbr-west-03.cleardb.net"
database = "heroku_d640986ade4d1bd"
user = "b6cd2ad82aa067"
password = "6625e744"

@app.route('/get', methods=['GET'])
def get():
    connection = mysql.connector.connect(host=host,
    database=database,
    user=user,
    password=password)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM riyazus_salihin")
    columns = [column[0] for column in cursor.description]
    results = []
    rows = cursor.fetchall()
    for row in rows:
        value=dict(zip(columns, row))
        results.append(value)
    cursor.close()
    return jsonify({'data': results} )

@app.route('/search', methods=['POST'])
def search():
    search_str = request.args.get("search")
    print(search_str)
    connection = mysql.connector.connect(host=host,
    database=database,
    user=user,
    password=password)
    cursor = connection.cursor(buffered=True)
    search_text = "SELECT arabic, turkish, title from riyazus_salihin WHERE turkish LIKE \"%"+search_str+"%\""
    cursor.execute(search_text)
    connection.commit()
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    results = []
    # all in the search box will return all the tuples
    for row in rows:
        value=dict(zip(columns, row))
        results.append(value)
        print(row)
    cursor.close()
    return jsonify({'data': results} )

app.config['JSON_AS_ASCII'] = False

# Driver function
if __name__ == '__main__':
	app.run(debug = True)