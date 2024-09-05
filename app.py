from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'user': 'root',            # Nombre de usuario de MySQL
    'password': 'root1234',  # Reemplaza con tu contraseña de MySQL
    'host': 'localhost',       # Dirección del servidor MySQL
    'port': 3306,              # Puerto del servidor MySQL
    'database': 'testdb'       # Nombre de la base de datos que creaste
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/insert', methods=['POST'])
def insert():
    name = request.form.get('name')
    email = request.form.get('email')

    try:
        # Conexión a la base de datos
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Insertar datos en la tabla
        cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (name, email))
        conn.commit()

        # Cerrar la conexión
        cursor.close()
        conn.close()
        
        return redirect(url_for('index'))
    
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return "Error al conectar a MySQL", 500

if __name__ == '__main__':
    app.run(debug=True)
