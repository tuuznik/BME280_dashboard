import random
import json
import time
from flask import Flask, Response, render_template, request, redirect, stream_with_context
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
random.seed()

#TODO: add database to the project
# class Measurements(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     measurement_date = db.Column(db.DateTime, default=datetime.utcnow)
#     temperature = db.Column(db.Integer, nullable=False)
#     pressure = db.Column(db.Integer, nullable=False)
#     humidity = db.Column(db.Integer, nullable=False)


#     def __repr__(self):
#         return f"<Measurement {self.id}>"

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/chart-data')
def chart_data():
    def generate_random_data():
        while True:
            json_data = json.dumps(
                    {'time': datetime.now().strftime('%H:%M:%S'), 'value': random.random() * 100})
                # {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': random.random() * 100})
            yield f"data:{json_data}\n\n"
            time.sleep(1)

    response = Response(stream_with_context(generate_random_data()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response

if __name__ == "__main__":
    app.run(debug=True)