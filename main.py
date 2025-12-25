from flask import Flask, render_template_string
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MORPHLINE 11 | Global Hub</title>
        <style>
            body { margin: 0; background: #000; height: 100vh; display: flex; align-items: center; justify-content: center; overflow: hidden; font-family: 'Inter', sans-serif; }
            .unit-core {
                width: 150px; height: 150px;
                background: radial-gradient(circle, #00f2ff, #000b1a);
                border-radius: 50%;
                box-shadow: 0 0 50px #00f2ff;
                animation: pulse 3s infinite ease-in-out;
                cursor: pointer; transition: transform 0.3s;
            }
            .unit-core:hover { transform: scale(1.1); }
            @keyframes pulse {
                0% { transform: scale(0.9); opacity: 0.6; box-shadow: 0 0 20px #00f2ff; }
                50% { transform: scale(1); opacity: 1; box-shadow: 0 0 70px #00f2ff; }
                100% { transform: scale(0.9); opacity: 0.6; box-shadow: 0 0 20px #00f2ff; }
            }
            .label { color: #fff; position: absolute; bottom: 10%; letter-spacing: 5px; font-weight: 200; opacity: 0.5; }
        </style>
    </head>
    <body>
        <div class="unit-core"></div>
        <div class="label">MORPHLINE 11 | UNIT OF CAPACITY ACTIVE</div>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
