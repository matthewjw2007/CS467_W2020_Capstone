from flask import Flask
import constants    # constants.py
import login        # login.py
import pantry       # pantry.py
import recipes      # recipes.py
import register     # register.py
import users        # users.py

app = Flask(__name__)

# Register the blueprints for different routes
app.register_blueprint(login.bp)    # /login
app.register_blueprint(pantry.bp)   # /pantry
app.register_blueprint(recipes.bp)  # /recipes
app.register_blueprint(register.bp) # /register
app.register_blueprint(users.bp)    # /users


# Enables running the app locally.
# Access through http://127.0.0.1:8080 or http://localhost:8080
if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8080', debug=True)  # debug=True allows for debugging info to be printed in the browser
