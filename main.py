from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my-books-collection.db"
Bootstrap5(app)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=False)
    author: Mapped[str] = mapped_column(unique=False)
    rating: Mapped[str] = mapped_column(unique=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    result = db.session.execute(db.select(Book).order_by(Book.id))
    all_books = result.scalars()
    return render_template("index.html", library=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Book(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"]
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        book_id = request.form["id"]
        book_to_update = db.get_or_404(Book, book_id)
        book_to_update.title = request.form["title"]
        book_to_update.author = request.form["author"]
        book_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = db.get_or_404(Book, book_id)
    return render_template("edit.html", book=book_selected)


@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        book_id = request.form["id"]
        book_to_delete = db.get_or_404(Book, book_id)
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = db.get_or_404(Book, book_id)
    return render_template("delete.html", book=book_selected)


if __name__ == "__main__":
    app.run(debug=True)
