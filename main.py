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
        <title>MORPHLINE 11 | Firing Mode</title>
        <style>
            body { margin: 0; background: #000; height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; overflow: hidden; font-family: sans-serif; }
            
            /* The Firing Engine Core */
            .unit-core {
                width: 160px; height: 160px;
                background: radial-gradient(circle, #00f2ff, #001a1a);
                border-radius: 50%;
                box-shadow: 0 0 40px #00f2ff;
                animation: idle-pulse 4s infinite ease-in-out;
                cursor: pointer; position: relative; z-index: 10;
            }
            .unit-core:active { transform: scale(0.8); transition: 0.1s; }

            /* App Opportunity Modal */
            #app-trigger {
                display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                background: rgba(0,0,0,0.9); z-index: 100; color: white;
                flex-direction: column; align-items: center; justify-content: center;
            }
            .cta-button {
                background: #00f2ff; color: black; padding: 20px 40px; 
                border-radius: 50px; text-decoration: none; font-weight: bold;
                margin-top: 20px; text-transform: uppercase; letter-spacing: 2px;
            }

            @keyframes idle-pulse {
                0%, 100% { transform: scale(1); box-shadow: 0 0 40px #00f2ff; }
                50% { transform: scale(1.1); box-shadow: 0 0 80px #00f2ff; }
            }
        </style>
    </head>
    <body>
        <div class="unit-core" onclick="ignite()"></div>
        <div id="app-trigger">
            <h1 style="letter-spacing: 8px;">CAPACITY UNLOCKED</h1>
            <p>Transitioning to ML11 Mobile Environment...</p>
            <a href="#" class="cta-button">Open ML11 App</a>
            <p style="margin-top: 30px; opacity: 0.5; cursor: pointer;" onclick="closeModal()">Back to Hub</p>
        </div>

        <script>
            function ignite() { document.getElementById('app-trigger').style.display = 'flex'; }
            function closeModal() { document.getElementById('app-trigger').style.display = 'none'; }
        </script>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
