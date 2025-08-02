from flask import Flask, render_template, request
from scraper.scraper import fetch_case_data
import mysql.connector
from datetime import datetime

app = Flask(__name__)


DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',  
    'database': 'court_data'
}
print('Connected!')

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def log_query(case_type, case_number, year, raw_html):
    conn = get_connection()
    cursor = conn.cursor()

    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS queries (
            id INT AUTO_INCREMENT PRIMARY KEY,
            case_type VARCHAR(20),
            case_number VARCHAR(20),
            year VARCHAR(10),
            timestamp DATETIME,
            raw_html LONGTEXT
        )
    ''')

    
    cursor.execute('''
        INSERT INTO queries (case_type, case_number, year, timestamp, raw_html)
        VALUES (%s, %s, %s, %s, %s)
    ''', (case_type, case_number, year, datetime.now(), raw_html))

    conn.commit()
    cursor.close()
    conn.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        case_type = request.form.get('case_type')
        case_number = request.form.get('case_number')
        year = request.form.get('year')

        try:
            result, raw_html = fetch_case_data(case_type, case_number, year)
            log_query(case_type, case_number, year, raw_html)
            print("[DEBUG] Result:", result)
            print("[DEBUG] Raw HTML length:", len(raw_html) if raw_html else "No HTML")

            return render_template('result.html', result=result)
        except Exception as e:
            return render_template('result.html', error=str(e))

    return render_template('index.html')


if __name__ == '__main__':
    app.run()
