import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# =====================================================================
# DILARANG MENGUBAH ATAU MENG-HARDCODE BAGIAN INI!
# =====================================================================
# Sistem akan otomatis membaca Environment Variables dari Azure ACI.
# Jika kalian menulis nama langsung di sini, nilai otomatis dipotong.
nama_owner = os.environ.get('NAMA_PRAKTIKAN', 'Misterius')
nim_owner = os.environ.get('NIM_PRAKTIKAN', '00000000')

# =====================================================================
# BAGIAN INI BEBAS KALIAN MODIFIKASI SESUAI TEMA YANG KALIAN PILIH
# Tema: Koleksi Album Indie Rock
# =====================================================================
katalog_data = {
    "judul_katalog": f"Indie Rock Vault \u2014 {nama_owner}",
    "pemilik": nama_owner,
    "nim": nim_owner,
    "deskripsi": "Koleksi album indie rock legendaris pilihan kurator",
    "items": [
        {"album": "AM", "artis": "Arctic Monkeys", "tahun": 2013, "genre": "Indie Rock"},
        {"album": "Whatever People Say I Am, That's What I'm Not", "artis": "Arctic Monkeys", "tahun": 2006, "genre": "Post-Punk Revival"},
        {"album": "Is This It", "artis": "The Strokes", "tahun": 2001, "genre": "Garage Rock Revival"},
        {"album": "Room on Fire", "artis": "The Strokes", "tahun": 2003, "genre": "Indie Rock"},
        {"album": "Tranquility Base Hotel & Casino", "artis": "Arctic Monkeys", "tahun": 2018, "genre": "Space Pop"},
        {"album": "Favourite Worst Nightmare", "artis": "Arctic Monkeys", "tahun": 2007, "genre": "Indie Rock"},
        {"album": "The New Abnormal", "artis": "The Strokes", "tahun": 2020, "genre": "New Wave"}
    ]
}

@app.route('/api/info', methods=['GET'])
def get_info():
    return jsonify(katalog_data)

@app.route('/api/add-item', methods=['POST'])
def add_item():
    data = request.json
    album = data.get('album') if data else None
    if album:
        new_item = {
            "album": album,
            "artis": data.get('artis', 'Unknown Artist'),
            "tahun": data.get('tahun', '-'),
            "genre": data.get('genre', 'Indie Rock')
        }
        katalog_data["items"].append(new_item)
        return jsonify({"message": "Album berhasil ditambahkan!", "items": katalog_data["items"]}), 201
    return jsonify({"error": "Data tidak valid"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
