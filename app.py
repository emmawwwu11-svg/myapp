import pymysql
import os
from flask import Flask, jsonify

app = Flask(__name__)

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'admin')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
DB_NAME = os.environ.get('DB_NAME', 'myapp')

@app.route('/')
def home():
    return jsonify({
        'status': 'ok',
        'message': 'App is running on ECS!',
        'database': DB_HOST
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

@app.route('/db')
def db_test():
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        with conn.cursor() as cursor:
            cursor.execute('SELECT VERSION()')
            version = cursor.fetchone()
        conn.close()
        return jsonify({
            'status': 'connected',
            'mysql_version': version[0]
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
