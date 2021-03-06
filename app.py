import json
import io
import csv
import time
import subprocess
import sqlite3 as sql
from flask import Flask, Response, render_template, request, redirect, stream_with_context
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

db_name = 'data.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

db = SQLAlchemy(app)

class TempMeasurements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    measurement_date = db.Column(db.DateTime, default=datetime.utcnow)
    temperature = db.Column(db.Float, nullable=False)

class PressureMeasurements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    measurement_date = db.Column(db.DateTime, default=datetime.utcnow)
    pressure = db.Column(db.Float, nullable=False)
    
class HumidityMeasurements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    measurement_date = db.Column(db.DateTime, default=datetime.utcnow)
    humidity = db.Column(db.Float, nullable=False)


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html', turned_on="off")

@app.route('/start', methods=['POST', 'GET'])
def start():
    return render_template('index.html', turned_on="on")

@app.route('/stop', methods=['POST', 'GET'])
def stop():
    return render_template('index.html', turned_on="off")

def add_data(table, data_column_name, meas_data):  
  try:
    con = sql.connect('data.db')
    c =  con.cursor()
    sql_cmd = f"INSERT INTO {table} (measurement_date, {data_column_name}) VALUES (datetime('now','localtime'), {meas_data})"
    c.execute(sql_cmd)
    con.commit() 
  except:
    print("An error has occured")


def read_data(file_name, table, data_column_name, coef):
    while True:
        file = open(f"/sys/bus/i2c/devices/1-0077/{file_name}", 'r')
        output = file.read()
        data = int(output)/coef
        json_data = json.dumps(
                {'time': datetime.now().strftime('%H:%M:%S'), 'value': data})
        add_data(table, data_column_name, data)
        yield f"data:{json_data}\n\n"
        time.sleep(1)


@app.route('/temp-data')
def temperature_data():
    response = Response(stream_with_context(read_data("temperature", "temp_measurements", "temperature", 100)), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response

@app.route('/pressure-data')
def pressure_data():
    response = Response(stream_with_context(read_data("pressure", "pressure_measurements", "pressure", 25600)), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response

@app.route('/humidity-data')
def humidity_data():
    response = Response(stream_with_context(read_data("humidity", "humidity_measurements", "humidity", 1024)), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response

def delete_data_from_table(table_name: str):
    conn = None
    cursor = None
    try:
        con = sql.connect('data.db')
        c =  con.cursor()
        sql_cmd = f"DELETE FROM {table_name};"
        c.execute(sql_cmd)
        con.commit() 
    except:
        print("An error has occured")

@app.route('/remove-data')
def remove_data():
    delete_data_from_table('temp_measurements')
    delete_data_from_table('humidity_measurements')
    delete_data_from_table('pressure_measurements')
    return render_template('index.html', turned_on="off")

@app.route('/download/')
def download_report():
    conn = None
    cursor = None
    try:
        con = sql.connect('data.db')
        c =  con.cursor()
        sql_cmd = "SELECT humidity_measurements.id, humidity_measurements.measurement_date, humidity_measurements.humidity, " \
                  "pressure_measurements.pressure, temp_measurements.temperature FROM humidity_measurements " \
                  "JOIN pressure_measurements ON pressure_measurements.id = humidity_measurements.id " \
                  "JOIN temp_measurements ON temp_measurements.id = pressure_measurements.id;"
        c.execute(sql_cmd)
        result = c.fetchall()

        output = io.StringIO()
        writer = csv.writer(output)

        line = ['ID, date, humidity, pressure, temperature']
        writer.writerow(line)

        for row in result:
            print(row)
            line = [str(row[0]) + ',' + row[1] + ',' + str(row[2]) + ',' + str(row[3]) + ',' + str(row[4])]
            writer.writerow(line)

        output.seek(0)
            
        return Response(output, mimetype="text/csv", headers={"Content-Disposition":"attachment;filename=data.csv"})
    except Exception as e:
        print(e)

if __name__ == "__main__":
    app.run(debug=True)