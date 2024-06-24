from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'chave_super_secreta_aqui'

app.config['MYSQL_HOST'] = 'localhost'  
app.config['MYSQL_USER'] = 'root'  
app.config['MYSQL_PASSWORD'] = '2114'  
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
        session['user_type'] = 'cliente'
        session['user_id'] = cliente[0]
        return redirect(url_for('home'))
    else:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM corretores WHERE email = %s AND senha = %s", (email, senha))
        corretor = cur.fetchone()
        cur.close()
        if corretor:
            session['user_type'] = 'corretor'
            session['user_id'] = corretor[0]
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Credenciais inválidas. Por favor, tente novamente.")

@app.route('/home')
def home():
    if 'user_type' not in session:
        return redirect(url_for('login'))

    user_type = session['user_type']
    user_id = session['user_id']

    return render_template('pages/home.html', user_type=user_type, user_id=user_id)

@app.route('/pesquisar_corretores', methods=['GET', 'POST'])
def pesquisar_corretores():
    if 'user_type' not in session or session['user_type'] != 'cliente':
        return redirect(url_for('login'))

    if request.method == 'POST':
        termo_pesquisa = request.form['termo_pesquisa']
        cur = mysql.connection.cursor()
        cur.execute("SELECT nome, email, numero_registro FROM corretores WHERE nome LIKE %s OR email LIKE %s", (f'%{termo_pesquisa}%', f'%{termo_pesquisa}%'))
        corretores = cur.fetchall()
        cur.close()
        return render_template('pages/resultados_pesquisa.html', corretores=corretores)

    return render_template('pages/pesquisar_corretores.html')

@app.route('/cadastro_planos', methods=['GET', 'POST'])
def cadastro_planos():
    if 'user_type' not in session or session['user_type'] != 'corretor':
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        plano_id = request.form['plano_id']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO corretores_planos (corretor_id, plano_id) VALUES (%s, %s)", (user_id, plano_id))
        mysql.connection.commit()
        cur.close()
        flash('Plano cadastrado com sucesso!', 'success')

    cur = mysql.connection.cursor()
    cur.execute("SELECT ps.id, ps.nome_plano, ps.estado FROM planos_saude ps LEFT JOIN corretores_planos cp ON ps.id = cp.plano_id AND cp.corretor_id = %s WHERE cp.plano_id IS NULL", (user_id,))
    planos_disponiveis = cur.fetchall()
    cur.execute("SELECT ps.nome_plano, ps.estado FROM planos_saude ps INNER JOIN corretores_planos cp ON ps.id = cp.plano_id WHERE cp.corretor_id = %s", (user_id,))
    planos_cadastrados = cur.fetchall()
    cur.close()

    return render_template('pages/cadastro_planos.html', planos_disponiveis=planos_disponiveis, planos_cadastrados=planos_cadastrados)

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

    flash('Cliente cadastrado com sucesso!', 'success')
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

    flash('Corretor cadastrado com sucesso!', 'success')
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)
