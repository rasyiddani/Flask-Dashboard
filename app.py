from flask import Flask, request, jsonify, render_template
from datetime import datetime
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"


# Fungsi untuk membaca data dari data.json
def read_data():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as file:
        return json.load(file)


# Fungsi untuk menyimpan data ke data.json
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


# Halaman utama
@app.route("/")
def index():
    data = read_data()
    return render_template("index.html", data=data)

@app.route("/kirim")
def kirim():
    return render_template("kirim.html")


# Route POST untuk menerima data sensor
@app.route("/api/suhu", methods=["POST"])
def post_suhu():
    body = request.get_json()

    suhu = body.get("suhu")

    if suhu is None:
        return jsonify({
            "status": "error",
            "message": "Data suhu wajib diisi"
        }), 400

    new_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "suhu": suhu
    }

    data = read_data()
    data.append(new_data)
    save_data(data)

    return jsonify({
        "status": "success",
        "message": "Data suhu berhasil disimpan",
        "data": new_data
    })


@app.route("/api/suhu", methods=["GET"])
def get_suhu():
    data = read_data()
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)