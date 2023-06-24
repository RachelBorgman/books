from flask import Flask, render_template, request, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.book import Book

# @app.route("/tryout")
# def books_tryout():
#     books = Book.get_all_books()
#     print(books)
#     return render_template("books.html", all_books=books)

@app.route("/books")
def books():
    books = Book.get_all_books()
    print(books)
    return render_template("books.html", all_books=books)

@app.route('/created_book', methods=["POST"])
def created_book():
    data = {
        "title": request.form["title"],
        "num_of_pages": request.form["num_of_pages"]
    }
    Book.save_book(data)
    return redirect('/books')

@app.route("/show_book/<int:id>")
def get_favorite_book(id):
    data = {
        'id': id
    }
    return render_template("show_book.html", book = Book.get_favorite_book(data), unfavorited_authors=User.unfavorited_authors(data))

@app.route('/merge/author', methods=['POST'])
def merge_author():
    data = {
        'user_id': request.form['user_id'],
        'book_id': request.form['book_id']
    }
    # User.save(data)
    User.add_favorite(data)
    return redirect(f"/show_book/{request.form['book_id']}")

# @app.route('/update', methods=['POST'])
# def update():
#     User.update(request.form)
#     new_user_id = request.form["id"]
#     return redirect(f'/read_one/{new_user_id}')

# @app.route('/delete/<int:id>')
# def delete(id):
#     data = {
#         'id': id
#     }
#     User.delete(data)
#     return redirect('/')