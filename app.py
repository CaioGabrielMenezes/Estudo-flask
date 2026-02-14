from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave-padrao')
db = SQLAlchemy(app)

#Definindo modelo de banco de dados
class Tasks (db.Model):
    id = db.Column(db.Integer, primary_key= True)
    description = db.Column(db.String(100), unique=True, nullable=False)

#cRud
@app.route('/')
def index():
    tasks = Tasks.query.all()
    return render_template('index.html', tasks=tasks)

#Crud
@app.route('/create', methods=["POST"])
def create_task():
    description = request.form['description']

    #Validando arquivos duplicados
    existind_task = Tasks.query.filter_by(description=description).first()
    if existind_task:
        return 'Error: Tarefa já existe', 400
    

    new_task = Tasks(description = description)
    db.session.add(new_task)
    db.session.commit()
    return redirect('/')

#cruD
@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):   
    task = Tasks.query.get(task_id)

    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect('/')

#crUd
@app.route('/update/<int:task_id>',methods=['POST'])
def update_task(task_id):
    task = Tasks.query.get(task_id) #instância do db

    if task: #se existir captura as informações do formulário html de description
        task.description = request.form['description']
        db.session.commit() #commit no banco
    return redirect('/') #redireciona para a rota principal



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5153)