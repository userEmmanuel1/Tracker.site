

import requests
import time
import smtplib
import ssl
from multiprocessing import Process

def run_stock_tracker(tracking_stocks, email_sms_value):
    # Email sender configuration
    smtp_port = 587
    smtp_server = "smtp.gmail.com"
    email_from = "ecueva003@gmail.com"
    email_to = email_sms_value
    pw = ""
    simple_email_context = ssl.create_default_context()

    # Stock tracker configuration
    ticker = tracking_stocks
    msg1 = f"Check the stock {ticker}, probably SELL"
    api_key = ""

    # Function to get stock price
    def get_stock_price(ticker_symbol, api):
        url = f"https://api.twelvedata.com/price?symbol={ticker}&apikey={api}"
        url2 = f"https://api.twelvedata.com/quote?symbol={ticker}&apikey={api}"
        response = requests.get(url).json()
        price = response['price'][:-3]
        print("$" + price + " per share for " + ticker_symbol)
        return price

    # Function to send notification
    def send_notification(message):
        try:
            TIE_server = smtplib.SMTP(smtp_server, smtp_port)
            TIE_server.starttls(context=simple_email_context)
            TIE_server.login(email_from, pw)

            print(f"Sending email to {email_to}")
            TIE_server.sendmail(email_from, email_to, message)
            print(f"Sent email to {email_to}")

            resp = requests.post('https://textbelt.com/text', {
                'phone': '+',
                'heading': 'STFU',
                'message': message,
                'key': '',
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

    # Stock tracker loop
    while sell_price1 or sell_price2:
        # Get the current stock price
        current_price = float(get_stock_price(ticker, api_key))

        # Check if the current price is below a certain threshold for notification
        if current_price < sell_price1:
            send_notification(msg1)
            print("Notification sent.")
        
        # Update sell_price1 and sell_price2 with the current price (adjust as needed)
        sell_price1 = current_price * 0.95  # Example: Notify when the price drops by 5%
        sell_price2 = current_price * 0.90  # Example: Notify when the price drops by 10%

        time.sleep(20)  # Adjust the sleep time based on your needs

    print('Stock tracker finished.')
