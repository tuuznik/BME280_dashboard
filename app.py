from flask import Flask,  render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)