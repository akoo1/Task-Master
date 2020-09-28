
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# __name__ is just referencing this file
app = Flask(__name__)
app.config['SECRET_KEY'] = 'you will never guess'

# This tells our app where the DB is located 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# To initialize the DB
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # We don't want the user to create a new task, but leave the content empty
    content = db.Column(db.String(200), nullable=False) 
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

# To initialize a DB file
# Enter the python interactive shell (type 'python3' in the terminal)
# 'from application import db'
# 'db.create_all()'

@app.route('/', methods=['POST', 'GET'])
def index():
    # If the homepage is requested by a user submitting the form
    if request.method == 'POST':
        task_content = request.form.get('content')
        if task_content == '':
            # Flash a warning message
            flash('Task field cannot be empty', 'warning')
            return redirect('/')

        # create a new Todo model to add to our DB
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    # else, get all the task objects from the DB in the order they are created, and display them 
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)



@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form.get('content')
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem deleting that task'
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
