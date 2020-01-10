from app import app

# Enables running the app locally.
# Access through http://127.0.0.1:8080 or http://localhost:8080
if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8080', debug=True)  # debug=True allows for debugging info to be printed in the browser
