from flask import Flask, jsonify
from flaskext.mysql import MySQL


app = Flask(__name__)
mysql = MySQL(app)
app.config['MYSQL_DATABASE_USER'] = 'u7woqgg9uo2nf6kh'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Gt2sHFHFH4IpTCHIGcEF'
app.config['MYSQL_DATABASE_DB'] = 'buf8m8k37mwmv2mty8rh'
app.config['MYSQL_DATABASE_HOST'] = 'buf8m8k37mwmv2mty8rh-mysql.services.clever-cloud.com'


@app.route('/', methods=['POST'])
def index():
    cur = mysql.connect().cursor()

    # CREATE A TABLE
    #cur.execute(''' CREATE TABLE example(id INTEGER, name VARCHAR(20))''')

    # INSERT DATA INTO THE TABLE
    cur.execute('''INSERT INTO example VALUES (3,'JACK')''')
    mysql.connect().commit()

    # fetch data
    cur.execute('''select * from example''')
    res = cur.fetchall()
    ot = jsonify(res)
    return ot


if __name__ == '__main__':
    app.run(debug=True)
