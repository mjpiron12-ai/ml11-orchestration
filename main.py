import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    capacity = os.environ.get('INITIAL_CAPACITY', '500')
    term = os.environ.get('CAPACITY_TERM', 'capacity')
    return f"<h1>Morphline 11 Hub Active</h1><p>{term.capitalize()}: {capacity} units</p>"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
