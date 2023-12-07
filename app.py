

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.datastructures import ImmutableMultiDict
from multiprocessing import Process
import time
from my_tracker import run_stock_tracker 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Stocks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(30), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form
        tracking_stocks = data.get('stocks', '')
        email_sms_value = data.get('email/sms', '')

        print("Stocks:", tracking_stocks)
        print("Email/SMS:", email_sms_value)

        # Run the stock tracker in a separate process
        stock_tracker_process = Process(target=run_stock_tracker, args=(tracking_stocks, email_sms_value))
        stock_tracker_process.start()

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
