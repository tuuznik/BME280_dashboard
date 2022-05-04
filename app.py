import json
import time
import subprocess 
from flask import Flask, Response, render_template, request, redirect, stream_with_context
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

db_name = 'data.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

db = SQLAlchemy(app)

class Measurements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    measurement_date = db.Column(db.DateTime, default=datetime.utcnow)
    temperature = db.Column(db.Float, nullable=False)
    pressure = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Measurement {self.id}>"

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html', turned_on="off")

@app.route('/start', methods=['POST', 'GET'])
def start():
    return render_template('index.html', turned_on="on")

@app.route('/stop', methods=['POST', 'GET'])
def stop():
    return render_template('index.html', turned_on="off")

@app.route('/temp-data')
def temperature_data():
    def read_data():
        while True:
            file = open("/sys/bus/i2c/devices/1-0077/temperature", 'r')
            output = file.read()
            temperature = int(output)/100
            json_data = json.dumps(
                    {'time': datetime.now().strftime('%H:%M:%S'), 'value': temperature})
                # {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': random.random() * 100})
            yield f"data:{json_data}\n\n"
            time.sleep(1)

    response = Response(stream_with_context(read_data()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response

@app.route('/pressure-data')
def pressure_data():
    def read_data():
        while True:
            file = open("/sys/bus/i2c/devices/1-0077/pressure", 'r')
            output = file.read()
            pressure = int(output)/25600
            print(pressure)
            json_data = json.dumps(
                    {'time': datetime.now().strftime('%H:%M:%S'), 'value': pressure})
                # {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': random.random() * 100})
            yield f"data:{json_data}\n\n"
            time.sleep(1)

    response = Response(stream_with_context(read_data()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response

@app.route('/humidity-data')
def humidity_data():
    def read_data():
        while True:
            file = open("/sys/bus/i2c/devices/1-0077/humidity", 'r')
            output = file.read()
            humidity = int(output)/1024
            json_data = json.dumps(
                    {'time': datetime.now().strftime('%H:%M:%S'), 'value': humidity})
                # {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': random.random() * 100})
            yield f"data:{json_data}\n\n"
            time.sleep(1)

    response = Response(stream_with_context(read_data()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response

if __name__ == "__main__":
    app.run(debug=True)