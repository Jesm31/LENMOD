from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'user': 'root',           
    'password': 'root1234', 
    'host': 'localhost',      
    'port': 3306,              
    'database': 'testdb'       
}

@app.route('/')
def index():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Obtener todos los usuarios
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('index.html', users=users)
    
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return "Error al conectar a MySQL", 500

@app.route('/insert', methods=['POST'])
def insert():
    name = request.form.get('name')
    email = request.form.get('email')

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (name, email))
        conn.commit()

        cursor.close()
        conn.close()
        
        return redirect(url_for('index'))
    
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return "Error al conectar a MySQL", 500

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')

            cursor.execute('UPDATE users SET name = %s, email = %s WHERE id = %s', (name, email, id))
            conn.commit()
            cursor.close()
            conn.close()

            return redirect(url_for('index'))
        else:
            cursor.execute('SELECT * FROM users WHERE id = %s', (id,))
            user = cursor.fetchone()

            cursor.close()
            conn.close()

            return render_template('edit.html', user=user)
    
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return "Error al conectar a MySQL", 500

@app.route('/delete/<int:id>')
def delete(id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM users WHERE id = %s', (id,))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for('index'))
    
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return "Error al conectar a MySQL", 500

if __name__ == '__main__':
    app.run(debug=True)
