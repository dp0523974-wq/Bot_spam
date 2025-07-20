# app.py
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Criar banco de dados (uma vez)
def init_db():
    conn = sqlite3.connect('denuncias.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS denuncias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_denunciante TEXT,
            usuario_denunciado TEXT,
            motivo TEXT,
            mensagem TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Rota para enviar denúncia
@app.route('/denunciar', methods=['POST'])
def denunciar():
    data = request.get_json()
    conn = sqlite3.connect('denuncias.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO denuncias (usuario_denunciante, usuario_denunciado, motivo, mensagem)
        VALUES (?, ?, ?, ?)
    ''', (data['denunciante'], data['denunciado'], data['motivo'], data['mensagem']))
    conn.commit()
    conn.close()
    return jsonify({"mensagem": "Denúncia registrada com sucesso."})

# Rota para listar denúncias (ex: para moderação)
@app.route('/denuncias', methods=['GET'])
def listar_denuncias():
    conn = sqlite3.connect('denuncias.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM denuncias')
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)
