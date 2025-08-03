from flask import Flask, request, send_from_directory, redirect
from datetime import datetime
import requests
import os

app = Flask(__name__)

def get_ip_location(ip):
    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/")
        if response.status_code == 200:
            data = response.json()
            return f"{data.get('city')}, {data.get('region')}, {data.get('country_name')}"
    except:
        pass
    return "Inconnue"

@app.route('/rapport')
def rapport():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ua = request.headers.get('User-Agent')
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    location = get_ip_location(ip)

    log_entry = f"{time} | IP: {ip} | Location: {location} | UA: {ua}\n"
    print(log_entry)

    with open("logs.txt", "a") as f:
        f.write(log_entry)

    # Affiche une image ou PDF
    return send_from_directory("static", "rapport.png")  # ou PDF

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
