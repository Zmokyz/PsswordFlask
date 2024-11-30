from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

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
            return redirect(url_for('dashboard'))  # Redirigir a una página de éxito
        else:
            # Las credenciales son incorrectas
            flash("Invalid username or password. Please try again.", "error")
    
    return render_template('index.html')

# Ruta para la página de dashboard o página privada después del login
@app.route('/dashboard')
def dashboard():
    return "Welcome to the dashboard!"

# Ruta para la página de creación de usuario
@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        # Obtener los datos del formulario
        username = request.form['User']
        password = request.form['Psswrd']
        
        # Crear un nuevo usuario
        hashed_password = generate_password_hash(password)
        new_user = User(user=username, password=hashed_password)
        
        # Guardar el usuario en la base de datos
        db.session.add(new_user)
        db.session.commit()
        
        flash("User created successfully! You can now log in.", "success")
        return redirect(url_for('login'))  # Redirigir al login
    
    return render_template('CreateUser.html')  # Página para crear usuario

if __name__ == '__main__':
    app.run(debug=True)
