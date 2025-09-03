from flask_sqlalchemy import SQLAlchemy
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    ruolo = db.Column(db.String(20), nullable=False)
    macchina = db.Column(db.String(50), nullable=True)

class Lavorazione(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    macchina = db.Column(db.String(50))
    descrizione = db.Column(db.String(200))
    cliente = db.Column(db.String(100))
    ordine = db.Column(db.String(100))
    codice = db.Column(db.String(100))
    data_consegna = db.Column(db.String(100))
    notifica = db.Column(db.Boolean, default=False)
