"""
Render free plan uchun keep-alive server
Bot o'chib qolmasligi uchun HTTP server ham ishlatiladi
"""
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "GOJO-USERBOT ishlayapti!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()
