from flask import Flask, render_template_string, session
import os
import secrets

app = Flask(__name__)
# Generate a random secret key for secure silent detection
app.secret_key = secrets.token_hex(16)

@app.route('/')
def index():
    # Detect if this user is a returning visitor
    is_returning = session.get('initialized', False)
    
    # Mark the session as active for future visits
    session['initialized'] = True
    
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MORPHLINE 11 | All-Electric</title>
        <style>
            body { margin: 0; background: #000; height: 100vh; display: flex; align-items: center; justify-content: center; overflow: hidden; font-family: sans-serif; color: white; }
            
            .unit-core {
                width: 160px; height: 160px;
                background: radial-gradient(circle, {{ 'cyan' if returning else '#00f2ff' }}, #001a1a);
                border-radius: 50%;
                box-shadow: 0 0 {{ '100px cyan' if returning else '40px #00f2ff' }};
                animation: idle-pulse 4s infinite ease-in-out;
                cursor: pointer;
            }

            #status-bar { position: absolute; bottom: 5%; letter-spacing: 3px; font-size: 0.8rem; opacity: 0.6; }

            @keyframes idle-pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.1); }
            }
        </style>
    </head>
    <body>
        <div class="unit-core" onclick="ignite()"></div>
        <div id="status-bar">
            SYSTEM: {{ 'RECOGNIZED' if returning else 'INITIALIZING' }} | STAGE: ALL-ELECTRIC
        </div>

        <script>
            function ignite() { 
                alert("Transitioning to Plasma Fueled State...");
            }
            
            // Fast-Key affirmative listeners still active
            document.addEventListener('keydown', (e) => {
                if (['/', ';', "'"].includes(e.key)) ignite();
            });
        </script>
    </body>
    </html>
    """, returning=is_returning)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
