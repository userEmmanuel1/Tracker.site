from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.datastructures import ImmutableMultiDict


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
        tracking_stocks= data.get('stocks', '')
        email_sms_value = data.get('email/sms', '')

        print("Stocks:", tracking_stocks) 
        print("Email/SMS:", email_sms_value)

    return render_template('index.html')

user_data = ImmutableMultiDict([('stocks', ''), ('email/sms', '')])
for key, value in user_data.items():
    print(f"{key}: {value}")

if __name__ == "__main__":
    app.run(debug=True)
data = request.form
tracking_stocks= data.get('stocks', '')
email_sms_value = data.get('email/sms', '')

print("Stocks:", tracking_stocks) 
print("Email/SMS:", email_sms_value)













################# TRACKING AND ALERTING ################# 



import requests
import time
import smtplib
import ssl


# Email sender
smtp_port = 587
smtp_server = "smtp.gmail.com"

# To and from emails
email_from = "ecueva003@gmail.com"
email_to = email_sms_value

pw = "ihvv iluz gmrc vcqh"

simple_email_context = ssl.create_default_context()

# Stock tracker


ticker = tracking_stocks
msg1 = f"Check the stock {ticker}, probably SELL"
api_key = "71959a3173904d4cb215fe33857b2665"


def get_stock_price(ticker_symbol, api):
    url = f"https://api.twelvedata.com/price?symbol={ticker}&apikey={api}"
    url2 = f"https://api.twelvedata.com/quote?symbol={ticker}&apikey={api}"
    response = requests.get(url).json()
    price = response['price'][:-3]
    print("$" + price + " per share for " + ticker_symbol)
    return price


def send_notification(message):
    try:
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls(context=simple_email_context)
        TIE_server.login(email_from, pw)

        print(f"Sending email to {email_to}")
        TIE_server.sendmail(email_from, email_to, message)
        print(f"Sent email to {email_to}")
 
        resp = requests.post('https://textbelt.com/text', {
            'phone': '+13237173041',
            'heading': 'STFU',
            'message': message,
            'key': 'cd2595248c0ac46913b132b3ff6f335fa996cd95BAfjSt35FbB3Nnp0X7oxtIJlE',
        })
        print(resp.json())

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        TIE_server.quit()


# Basic information about the stock
price = get_stock_price(ticker, api_key)
low_price = high_price = open_price = close_price = float(price)

sell_price1 = open_price + close_price
sell_price2 = open_price - close_price

while sell_price1 or sell_price2 == True:
    if sell_price1 or sell_price2 == True:
        send_notification(msg1)
    else:
        print("Don't touch the stock")
    time.sleep(20)  # Adjust the sleep time based on your needs


print('ticker')