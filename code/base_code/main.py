import psycopg2 as pg
from flask import Flask, request, render_template

app = Flask(__name__)

# Параметры подключения к базе данных
DATABASE = {
    'user': 'postgres',
    'password': '..',
    'host': 'localhost',
    'port': '5432',
    'dbname': 'persik'
}

try:
    # Подключение к базе данных
    conn = pg.connect(**DATABASE)
    print("Connected to PostgreSQL (УСПЕШНО)")
    cur = conn.cursor()
except:
    print("Unable to connect to PostgreSQL (ОШИБКА)")

@app.route('/')
def index():
        # Получение данных из таблицы
        cur.execute("SELECT * FROM kostochka.otpravitel")
        rows = cur.fetchall()

        return render_template('index.html', data=rows)
@app.route('/add', methods=['POST', 'GET'])
def add():

    if request.method == 'GET':
        return render_template('add.html')
    # Добавление новой строки
    if request.method == 'POST':
        sender_id = request.form['sender_id']
        sender_name = request.form['sender_name']
        inn_sender = request.form['inn_sender']
        bank_sender = request.form['bank_sender']
        address_sender = request.form['address_sender']


    cur.execute("INSERT INTO customers (sender_id, sender_name, inn_sender, bank_sender, address_sender) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (sender_id, sender_name, inn_sender, bank_sender, address_sender))
    conn.commit()
    return render_template('add.html')

@app.route('/req1', methods=['GET'])
def req1():
    if request.method == 'GET':
        cur.execute("SELECT shipment, SUM(declare_value) AS total_declare_value, unit FROM kostochka.gryz GROUP BY shipment, unit;")
        rows = cur.fetchall()
        return render_template('Request1.html', data=rows)

@app.route('/req2', methods=['GET'])
def req2():
    if request.method == 'GET':
        cur.execute("SELECT pg.reg_number_id, s.name, s.skipper, pg.custom_value_id, pg.custom_clearance FROM kostochka.partia_gryza pg JOIN kostochka.sydno s ON pg.reg_number_id = s.reg_number_id WHERE pg.custom_clearance = true;;")
        rows = cur.fetchall()
        return render_template('Request2.html', data=rows)

@app.route('/req3', methods=['GET'])
def req3():
    if request.method == 'GET':
        cur.execute("SELECT s.reg_number_id, s.name, s.skipper, COUNT(pg.reg_number_id) AS num_of_shipments FROM  kostochka.sydno s LEFT JOIN kostochka.partia_gryza pg ON s.reg_number_id = pg.reg_number_id GROUP BY  s.reg_number_id, s.name, s.skipper ORDER BY s.reg_number_id ASC;")
        rows = cur.fetchall()
        return render_template('Request3.html', data=rows)

@app.route('/req4', methods=['GET'])
def req4():
    if request.method == 'GET':
        cur.execute("SELECT m.route_id, s.name AS ship_name, m.origin, m.destination, EXTRACT(DAY FROM (m.arrive_date - m.departure_date)) AS duration_days, ROUND(EXTRACT(EPOCH FROM (m.arrive_date - m.departure_date))/3600)::integer AS hours_in_transit FROM kostochka.marshryt m JOIN kostochka.sydno s ON m.reg_number_id = s.reg_number_id ORDER BY (m.arrive_date - m.departure_date) DESC LIMIT 10;")
        rows = cur.fetchall()
        return render_template('Request4.html', data=rows)
    
if __name__ == '__main__':
    app.run(debug=True)

