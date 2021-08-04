from enum import unique
from flask import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:test123@postgres_database/empdatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Test String'

db = SQLAlchemy(app)

class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

@app.route('/')
def index():
    all_data = Employees.query.all()
    return render_template("index.html", employees=all_data)

    

@app.route('/insert',methods=['POST'])
def insert():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    emp = Employees(name, email, phone)
    db.session.add(emp)
    db.session.commit()
    flash("Employee added successfully")
    return redirect(url_for('index'))

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Employees.query.get(request.form.get('id'))
        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
        db.session.add(my_data)
        db.session.commit()
    flash("Employee details updated")
    return redirect(url_for('index'))

@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    my_data = Employees.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee deleted!")
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(host = '0.0.0.0', debug=True)