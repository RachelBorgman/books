from flask_app.config.mysqlconnection import connectToMySQL
# from flask_app.models import favorites
from flask_app.models import book

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.authors = []
        self.favorite_books = []

    @classmethod
    def save_author(cls, data):
        query = """
            INSERT INTO users (name, created_at, updated_at) VALUES (%(name)s, NOW(), NOW());
        """
        return connectToMySQL('books_schema').query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('books_schema').query_db(query)
        authors = []
        for row in results:
            authors.append(cls(row))
        return authors
    
    # @classmethod
    # def show_author(cls, data):
    #     query = """
    #             SELECT * FROM users
    #             WHERE id = %(id)s;
    #     """
    #     result = connectToMySQL('books_schema').query_db(query, data)
    #     return cls(result[0])
    
    @classmethod
    def unfavorited_authors(cls,data):
        query = """
            SELECT * FROM users WHERE users.id NOT IN ( SELECT user_id FROM favorites WHERE book_id = %(id)s);
        """
        authors = []
        results = connectToMySQL('books_schema').query_db(query, data)
        for row in results:
            authors.append(cls(row))
        return authors
    
    @classmethod
    def delete_favorite(cls, data):
        query = "DELETE FROM favorites WHERE book_id = %(book_id)s;"
        results = connectToMySQL('users_schema').query_db(query, data)
        return results

    @classmethod
    def add_favorite(cls, data):
        query = "INSERT INTO favorites (user_id, book_id) VALUES (%(user_id)s, %(book_id)s);"
        return connectToMySQL('books_schema').query_db(query, data)

    @classmethod
    def get_author_with_books(cls, data):
        query = "SELECT * FROM users LEFT JOIN favorites ON favorites.user_id = users.id LEFT JOIN books ON favorites.book_id = books.id WHERE users.id = %(id)s;"
        results = connectToMySQL('books_schema').query_db(query, data)
        author = cls(results[0])
        for row_from_db in results:
            if row_from_db in results == None:
                break
            data = {
                "id": row_from_db['books.id'],
                "title": row_from_db["title"],
                "num_of_pages": row_from_db["num_of_pages"],
                "created_at": row_from_db["books.created_at"],
                "updated_at": row_from_db["books.updated_at"]
            }
            author.favorite_books.append(book.Book(data))
        return author