from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Expense model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Expense {self.description} - {self.amount}>"

# Initialize the database
@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    expenses = Expense.query.all()
    
    # Get categories and their total amounts
    categories = db.session.query(Expense.category, db.func.sum(Expense.amount).label('total'))\
                           .group_by(Expense.category).all()
    
    return render_template('index.html', expenses=expenses, categories=categories)

@app.route('/add', methods=['POST'])
def add_expense():
    description = request.form['description']
    amount = float(request.form['amount'])
    category = request.form['category']
    
    new_expense = Expense(description=description, amount=amount, category=category)
    db.session.add(new_expense)
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['GET'])
def delete_expense(id):
    expense = Expense.query.get(id)
    if expense:
        db.session.delete(expense)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
