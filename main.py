from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from flask_sqlalchemy import SQLAlchemy


class BookForm(FlaskForm):
    name = StringField('Book Name')
    author = StringField('Book Author')
    rating = IntegerField('Rating')
    submit = SubmitField('Add Book')


app = Flask(__name__)
app.secret_key = "any-string-you-want-just-keep-it-secret"

##CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books-collection.db"
#Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CREATE TABLE
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    #This will allow each book object to be identified by it's Title
    def __repr__(self):
        return f'<Book {self.title}>'


db.create_all()


@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template('index.html', books=all_books)


@app.route("/add", methods=["GET","POST"])
def add():
    book_form = BookForm()

    if request.method == "POST":
        new_book = Book(title=book_form.name.data, author=book_form.author.data, rating=book_form.rating.data)
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('add.html', form=book_form)


@app.route('/edit', methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        #UPDATE RATING
        book_id = request.form['id']
        book_to_update = Book.query.get(book_id)
        book_to_update.rating = request.form['new_rating']
        db.session.commit()
        return redirect(url_for('home'))

    book_id = request.args.get('id')
    selected_book = Book.query.get(book_id)
    return render_template('edit.html', book=selected_book)

if __name__ == "__main__":
    app.run(debug=True)

