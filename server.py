from flask_app.controllers import users, books
from flask_app import app

if __name__=="__main__":
    app.run(debug=True, host="localhost", port=5004)