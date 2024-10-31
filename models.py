# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Incidente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    tipo_incidente = db.Column(db.String(50), nullable=False)
    subtipo_incidente = db.Column(db.String(50), nullable=False)
    uso_arma = db.Column(db.Boolean, nullable=False)
    uso_moto = db.Column(db.Boolean, nullable=False)
    direccion = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.String(10), nullable=False)
    barrio = db.Column(db.String(50), nullable=True)
    comuna = db.Column(db.String(50), nullable=True)
