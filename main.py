from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-library.db'
db = SQLAlchemy(app)

# Create table
with app.app_context():
    class Book(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(250), unique=True, nullable=False)
        author = db.Column(db.String(250), nullable=False)
        rating = db.Column(db.Float, nullable=False)

    db.create_all()


@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template('index.html', books=all_books)


@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        rating = request.form['rating']

        with app.app_context():
            new_book = Book(title=title, author=author, rating=rating)
            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for('home'))

    return render_template('add.html')


@app.route('/edit', methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        with app.app_context():
            book_id = request.args.get('num')
            book_to_edit = Book.query.get(book_id)
            book_to_edit.rating = request.form['new_rating']
            db.session.commit()
            return redirect(url_for('home'))

    book_id = request.args.get('num')
    selected_book = Book.query.get(book_id)
    return render_template('edit.html', book=selected_book)


@app.route('/delete')
def delete():
    with app.app_context():
        book_id = request.args.get('num')
        book_to_delete = Book.query.get(book_id)
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
