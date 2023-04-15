from flask import Flask, jsonify,request
from flask_restful import Resource, Api
import mysql.connector

app = Flask(__name__)
# Create an API object
api = Api(app)


@app.route('/get', methods=['GET'])
def get():
    connection = mysql.connector.connect(host='localhost',
    database='riyaz',
    user='root',
    password='123wasd321W')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM riyaz.riyazus_salihin")
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
    connection = mysql.connector.connect(host='localhost',
    database='riyaz',
    user='root',
    password='123wasd321W')
    cursor = connection.cursor(buffered=True)
    search_text = "SELECT arabic, turkish, title from riyaz.riyazus_salihin WHERE turkish LIKE \"%"+search_str+"%\""
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