from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BaseDATA.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Necesario para las notificaciones flash
db = SQLAlchemy(app)

# Modelo de Usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    date_creation = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    # Relación con la tabla de contraseñas generadas (si es necesario)
    generated_passwords = db.relationship('Passwords', backref='user', lazy=True)

# Modelo de Contraseñas generadas
class Passwords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_creation = db.Column(db.DateTime, default=datetime.now(timezone.utc))

# Crear las tablas si no existen
with app.app_context():
    db.create_all()

# Ruta para la página de login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtener los datos del formulario
        username = request.form['User']
        password = request.form['Psswrd']
        
        # Buscar el usuario en la base de datos
        user = User.query.filter_by(user=username).first()
        
        if user and check_password_hash(user.password, password):
            # Las credenciales son correctas
            flash("Login successful!", "success")
            
            # Almacenar el ID del usuario en la sesión
            session['user_id'] = user.id  # Guarda el ID del usuario en la sesión
            
            return redirect(url_for('dashboard'))  # Redirigir al dashboard
        else:
            # Las credenciales son incorrectas
            flash("Invalid username or password. Please try again.", "error")
    
    return render_template('index.html')

# Ruta para la página de dashboard
@app.route('/dashboard')
def dashboard():
    # Recuperar el ID del usuario desde la sesión
    user_id = session.get('user_id')

    if not user_id:
        # Si no hay un usuario logueado, redirigir al login
        flash("You need to log in first.", "warning")
        return redirect(url_for('login'))

    # Buscar el usuario en la base de datos utilizando el ID
    user = User.query.get(user_id)
    
    # Pasar el usuario a la plantilla para personalizar el dashboard
    return render_template('dashboard.html', user=user)

# Ruta para la página de creación de usuario
@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        # Obtener los datos del formulario
        username = request.form['User']
        password = request.form['Psswrd']
        
        # Crear un nuevo usuario
        hashed_password = generate_password_hash
