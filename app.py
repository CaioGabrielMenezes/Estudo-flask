from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'minha-super-chave-secreta-para-testes-12345678990')
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
        flash('Error: Tarefa já existe!', 'error')
        print("FLASH ENVIADO: Erro - Tarefa duplicada")
        return redirect('/')
    

    new_task = Tasks(description = description)
    db.session.add(new_task)
    db.session.commit()
    flash('Tarefa adicionada com sucesso!', 'success')
    return redirect('/')

#cruD
@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):   
    task = Tasks.query.get(task_id)

    if task:
        db.session.delete(task)
        db.session.commit()
        flash('Tarefa removida', 'success')
    else:
        flash('Tarefa não encontrada', 'error')
    return redirect('/')

#crUd
@app.route('/update/<int:task_id>',methods=['POST'])
def update_task(task_id):
    task = Tasks.query.get(task_id) #instância do db

    if task:
        new_description = request.form['description'] #se existir captura as informações do formulário html de description
        existing_task = Tasks.query.filter_by(description=new_description).first()
        if existing_task and existing_task.id != task_id:
            flash('Erro! Ja existe essa tarefa', 'error')
            return redirect('/') #redireciona para a rota principal
        task.description = new_description
        db.session.commit()
        flash('Tarefa atualizada!', 'success')
    else:
        flash('Tarefa não Encontrada!', 'error')
    return redirect('/')

@app.route('/teste-flash')
def teste_flash():
    flash('Mensagem de teste! Se você vê isso, o flash funciona!', 'success')
    return redirect('/')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5153)