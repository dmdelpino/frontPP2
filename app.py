# app.py
from flask import Flask, render_template, request, redirect, url_for
from models import db, Incidente
from config import Config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()  # Crea las tablas de la base de datos

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ingreso', methods=['GET', 'POST'])
def ingreso():
    if request.method == 'POST':
        # Recoger datos del formulario
        fecha = request.form['fecha']
        tipo_incidente = request.form['tipo_incidente']
        subtipo_incidente = request.form['subtipo_incidente']
        uso_arma = bool(request.form.get('uso_arma'))
        uso_moto = bool(request.form.get('uso_moto'))
        direccion = request.form['direccion']
        numero = request.form['numero']
        barrio = request.form['barrio']
        
        # Crear un nuevo incidente
        nuevo_incidente = Incidente(
            fecha=datetime.strptime(fecha, '%Y-%m-%d'),
            tipo_incidente=tipo_incidente,
            subtipo_incidente=subtipo_incidente,
            uso_arma=uso_arma,
            uso_moto=uso_moto,
            direccion=direccion,
            numero=numero,
            barrio=barrio
        )
        db.session.add(nuevo_incidente)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('ingreso_datos.html')

@app.route('/consulta', methods=['GET', 'POST'])
def consulta():
    if request.method == 'POST':
        # Obtener los filtros desde el formulario
        filtros = {
            'fecha': request.form.get('fecha'),
            'tipo_incidente': request.form.get('tipo_incidente'),
            'subtipo_incidente': request.form.get('subtipo_incidente'),
            'uso_arma': request.form.get('uso_arma') == 'on',
            'uso_moto': request.form.get('uso_moto') == 'on',
            'barrio': request.form.get('barrio'),
            'comuna': request.form.get('comuna')
        }
        # Redirige a los resultados con los filtros
        return redirect(url_for('resultados', **filtros))

    return render_template('consulta_datos.html')

@app.route('/resultados')
def resultados():
    # Obtener los filtros desde la URL
    query = Incidente.query

    # Filtrar con cada campo si existe en la URL
    if request.args.get('fecha'):
        query = query.filter_by(fecha=datetime.strptime(request.args.get('fecha'), '%Y-%m-%d'))
    if request.args.get('tipo_incidente'):
        query = query.filter_by(tipo_incidente=request.args.get('tipo_incidente'))
    if request.args.get('subtipo_incidente'):
        query = query.filter_by(subtipo_incidente=request.args.get('subtipo_incidente'))
    if request.args.get('uso_arma') == 'True':
        query = query.filter_by(uso_arma=True)
    if request.args.get('uso_moto') == 'True':
        query = query.filter_by(uso_moto=True)
    if request.args.get('barrio'):
        query = query.filter_by(barrio=request.args.get('barrio'))
    if request.args.get('comuna'):
        query = query.filter_by(comuna=request.args.get('comuna'))
    
    resultados = query.all()
    return render_template('resultados.html', resultados=resultados)
