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
        <title>MORPHLINE 11 | Hyper-Input</title>
        <style>
            body { margin: 0; background: #000; height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; overflow: hidden; font-family: sans-serif; color: white; }
            
            /* The Hyper-Input Visual Core */
            .unit-core {
                width: 160px; height: 160px;
                background: radial-gradient(circle, #00f2ff, #001a1a);
                border-radius: 50%;
                box-shadow: 0 0 40px #00f2ff;
                animation: idle-pulse 4s infinite ease-in-out;
                cursor: pointer; position: relative; z-index: 10;
            }

            /* Modal Transition */
            #app-trigger {
                display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                background: rgba(0,0,0,0.95); z-index: 100;
                flex-direction: column; align-items: center; justify-content: center;
            }
            .plasma-text { color: #00f2ff; letter-spacing: 10px; text-transform: uppercase; font-weight: 100; }

            @keyframes idle-pulse {
                0%, 100% { transform: scale(1); box-shadow: 0 0 40px #00f2ff; }
                50% { transform: scale(1.1); box-shadow: 0 0 80px #00f2ff; }
            }
        </style>
    </head>
    <body>
        <div class="unit-core" id="core" onclick="ignite()"></div>
        <div id="app-trigger">
            <h1 class="plasma-text">Cylinders Firing</h1>
            <p>Affirmative received. Transitioning to All-Electric Stage...</p>
            <div style="margin-top: 20px; opacity: 0.5; cursor: pointer;" onclick="closeModal()">[ ESC to reset ]</div>
        </div>

        <script>
            // Fast-Key Listener logic
            document.addEventListener('keydown', function(event) {
                const fastKeys = ['/', ';', "'"];
                if (fastKeys.includes(event.key)) {
                    ignite();
                }
                if (event.key === 'Escape') {
                    closeModal();
                }
            });

            function ignite() { 
                document.getElementById('app-trigger').style.display = 'flex';
                document.getElementById('core').style.boxShadow = '0 0 150px #00f2ff';
            }
            function closeModal() { 
                document.getElementById('app-trigger').style.display = 'none';
                document.getElementById('core').style.boxShadow = '0 0 40px #00f2ff';
            }
        </script>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
