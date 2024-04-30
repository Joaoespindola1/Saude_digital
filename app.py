from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'  
app.config['MYSQL_USER'] = 'root'  
app.config['MYSQL_PASSWORD'] = '24534152'  
app.config['MYSQL_DB'] = 'saude_digital'  

mysql = MySQL(app)

@app.route('/')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def fazer_login():
    email = request.form['email']
    senha = request.form['senha']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM clientes WHERE email = %s AND senha = %s", (email, senha))
    cliente = cur.fetchone()
    cur.close()

    if cliente:
        return redirect(url_for('home'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM corretores WHERE email = %s AND senha = %s", (email, senha))
        corretor = cur.fetchone()
        cur.close()
        if corretor:
            return redirect(url_for('home'))
        else:
            return "Credenciais inválidas. Por favor, tente novamente."


@app.route('/home')
def home():
    return render_template('pages/home.html')



@app.route('/cadastro_clientes')
def cadastro_clientes():
    return render_template('pages/cad_clientes.html')

@app.route('/salvar_cliente', methods=['POST'])
def salvar_cliente():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    cpf = request.form['cpf']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO clientes (nome, email, senha, cpf) VALUES (%s, %s, %s, %s)", (nome, email, senha, cpf))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('login'))


@app.route('/cadastro_corretores')
def cadastro_corretores():
    return render_template('pages/cad_corretores.html')

@app.route('/salvar_corretor', methods=['POST'])
def salvar_corretor():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    cpf = request.form['cpf']
    numero_registro = request.form['numero_registro']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO corretores (nome, email, senha, cpf, numero_registro) VALUES (%s, %s, %s, %s, %s)", (nome, email, senha, cpf, numero_registro))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
