import logging
import requests
import os
import pandas
import datetime
from matplotlib import pyplot
from flask import Flask, send_from_directory, request, jsonify, render_template
import argparse

app = Flask(__name__, static_folder='static')
app.logger.setLevel(logging.ERROR)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
port = [8000]

#visualize messages
MESSAGES = []
#visualize pandas
PDFIGS = []


@app.route("/")
def index():
    htm = render_template('index.html', pdfigs=PDFIGS, messages=MESSAGES)
    print(htm)
    print(PDFIGS)
    print(MESSAGES)
    return htm
    #return send_from_directory("static", "index.html")


@app.route("/__temp__/<string:fname>")
def temp(fname):
    return send_from_directory('__temp__', fname)


@app.route("/chain_visualizer")
def chain_visualizer():
    return send_from_directory("static", "chain_visualizer.html")


@app.route("/replay")
def replay():
    return send_from_directory("static", "replay.html")


@app.route("/get_messages")
def get_messages():
    return jsonify(MESSAGES)


@app.route("/send_message", methods=["POST"])
def send_message():
    data = request.get_json()
    role = data.get("role")
    text = data.get("text")

    avatarUrl = find_avatar_url(role)

    message = {"role": role, "text": text, "avatarUrl": avatarUrl}
    MESSAGES.append(message)
    return jsonify(message)


@app.route("/append_pdfig", methods=["POST"])
def append_pdfig():
    data = request.get_json()
    appd = data.get("fname")
    PDFIGS.append(appd)
    retm = {"now": PDFIGS}
    return jsonify(retm)


def find_avatar_url(role):
    role = role.replace(" ", "%20")
    avatar_filename = f"avatars/{role}.png"
    avatar_url = f"/static/{avatar_filename}"
    return avatar_url


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='argparse')
    parser.add_argument('--port', type=int, default=8000, help="port")
    args = parser.parse_args()
    port.append(args.port)
    print(f"Please visit http://127.0.0.1:{port[-1]}/ for the front-end display page. \nIn the event of a port conflict, please modify the port argument (e.g., python3 app.py --port 8012).")
    app.run(host='0.0.0.0', debug=False, port=port[-1])
