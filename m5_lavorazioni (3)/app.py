from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models.models import User, Lavorazione

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        ruolo = request.form['ruolo']
        user = User.query.filter_by(username=username, ruolo=ruolo).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['ruolo'] = user.ruolo
            return redirect(url_for('dashboard_operatore' if user.ruolo == 'operatore' else 'dashboard_ufficio'))
        return render_template('login.html', error='Credenziali errate')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        macchina = request.form['macchina']
        user = User(username=username, password=password, ruolo='operatore', macchina=macchina)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard_operatore')
def dashboard_operatore():
    if 'user_id' not in session or session['ruolo'] != 'operatore':
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    lavorazioni = Lavorazione.query.filter_by(macchina=user.macchina).all()
    return render_template('dashboard_operatore.html', lavorazioni=lavorazioni, user=user)

@app.route('/dashboard_ufficio')
def dashboard_ufficio():
    if 'user_id' not in session or session['ruolo'] != 'ufficio':
        return redirect(url_for('login'))
    filtro = request.args.get('macchina')
    lavorazioni = Lavorazione.query.filter_by(macchina=filtro).all() if filtro else Lavorazione.query.all()
    return render_template('dashboard_ufficio.html', lavorazioni=lavorazioni)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/modifica/<int:id>', methods=['POST'])
def modifica(id):
    if 'user_id' not in session or session['ruolo'] != 'operatore':
        return redirect(url_for('login'))
    lavorazione = Lavorazione.query.get(id)
    lavorazione.cliente = request.form['cliente']
    lavorazione.ordine = request.form['ordine']
    lavorazione.codice = request.form['codice']
    lavorazione.data_consegna = request.form['data_consegna']
    db.session.commit()
    return redirect(url_for('dashboard_operatore'))

@app.route('/richiedi_data/<int:id>', methods=['POST'])
def richiedi_data(id):
    if 'user_id' not in session or session['ruolo'] != 'ufficio':
        return redirect(url_for('login'))
    lavorazione = Lavorazione.query.get(id)
    lavorazione.notifica = True
    db.session.commit()
    return redirect(url_for('dashboard_ufficio'))

if __name__ == '__main__':
    app.run(debug=True)
