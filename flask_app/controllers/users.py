from flask import Flask, render_template, request, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.book import Book

@app.route("/")
def index():
    return redirect('/authors')

@app.route("/authors")
def authors():
    authors = User.get_all()
    print(authors)
    return render_template("authors.html", all_authors=authors)

from flask_app.models.user import User
@app.route('/created_author', methods=["POST"])
def created():
    data = {
        "name": request.form["name"]
    }
    new_user_id=User.save_author(data)
    return redirect('/authors')


from flask_app.models.user import User
@app.route("/show_author/<int:id>")
def get_author_with_books(id):
    data = {
        'id': id
    }
    return render_template("show_author.html", user = User.get_author_with_books(data), unfavorited_books=Book.unfavorited_books(data))

@app.route('/merge/book', methods=['POST'])
def merge_book():
    data = {
        'user_id': request.form['user_id'],
        'book_id': request.form['book_id'],
    }
    User.add_favorite(data)
    new_user_id = request.form["user_id"]
    return redirect("/books")

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