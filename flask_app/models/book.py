from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
# book.of_authors.append( user.User(data) )

class Book:
    def __init__( self , db_data ):
        self.id = db_data['id']
        self.title = db_data['title']
        self.num_of_pages = db_data['num_of_pages']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.authors_who_favorited = []
        # self.book_id = db_data['book_id']

    @classmethod
    def get_all_books(cls):
        query = "SELECT * FROM books;"
        results = connectToMySQL('books_schema').query_db(query)
        books = []
        for row in results:
            books.append(cls(row))
        return books
    
    @classmethod
    def get_one_book(cls, data):
        query = """
                SELECT * FROM books
                WHERE id = %(id)s;
        """
        result = connectToMySQL('books_schema').query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def get_favorite_book(cls, data):
        query = """
                SELECT * FROM books LEFT JOIN favorites ON books.id = favorites.book_id LEFT JOIN users ON users.id = favorites.user_id
                WHERE books.id = %(id)s;
        """
        results = connectToMySQL('books_schema').query_db(query, data)
        book = cls(results[0])
        for row in results:
            if row['users.id'] == None:
                break
            data = {
                "id": row['users.id'],
                "name": row['name'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            book.authors_who_favorited.append(user.User(data))
        return book
    
    @classmethod
    def unfavorited_books(cls,data):
        query = """
            SELECT * FROM books WHERE books.id NOT IN (SELECT book_id FROM favorites WHERE user_id = %(id)s);
        """
        results = connectToMySQL('books_schema').query_db(query,data)
        books = []
        for row in results:
            books.append(cls(row))
        return books
    
    # @classmethod
    # def get_book_with_authors(cls, data):
    #     query = """
    #             SELECT * FROM books LEFT JOIN favorites on books.id = favorites.book_id LEFT JOIN users ON users.id = favorites.user_id WHERE books.id users.%(id)s
    #     """
    #     results = connectToMySQL('books_schema').query_db(query, data)
    #     book = cls(results[0])
    #     for row_from_db in results:
    #         data = {
    #             "id": row_from_db["user.id"],
    #             "name": row_from_db["name"],
    #             "created_at": row_from_db["burgers.created_at"],
    #             "updated_at": row_from_db["burgers.updated_at"]
    #         }
    #         book.authors_who_favorited(user.User(data))
    #     return book

    @classmethod
    def save_book(cls, data):
        query = "INSERT INTO books (title, num_of_pages, created_at, updated_at ) VALUES (%(title)s, %(num_of_pages)s, NOW(), NOW());"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('books_schema').query_db(query, data)