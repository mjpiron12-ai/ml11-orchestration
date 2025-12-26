from flask import Flask, render_template_string, jsonify
import os
import requests

app = Flask(__name__)

@app.route('/api/energy')
def get_energy():
    try:
        res = requests.get('https://api.coinbase.com/v2/prices/BTC-USD/spot', timeout=2)
        price = float(res.json()['data']['amount'])
        pulse_speed = max(0.5, 8 - (price / 15000)) 
        return jsonify({"speed": f"{pulse_speed}s", "energy": f"{price:,.2f}"})
    except:
        return jsonify({"speed": "4s", "energy": "Stabilizing..."})

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ML11 | The Threshold</title>
        <style>
            :root { --bamboo: #4dbb5b; --cyan: #00f2ff; --dark: #050a05; }
            body { margin: 0; background: #000; height: 100vh; display: flex; align-items: center; justify-content: center; overflow: hidden; font-family: 'Courier New', monospace; color: white; }
            
            .plasma-core {
                width: 150px; height: 150px;
                background: radial-gradient(circle, var(--bamboo), var(--dark));
                border-radius: 50%; box-shadow: 0 0 50px var(--bamboo);
                animation: pulse var(--ps, 4s) infinite ease-in-out;
                cursor: pointer; transition: all 0.8s cubic-bezier(0.19, 1, 0.22, 1);
                z-index: 10;
            }

            #engine-hud {
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                background: rgba(0,0,0,0.98); display: none; opacity: 0;
                flex-direction: column; align-items: center; justify-content: center;
                z-index: 20; transition: opacity 1s ease;
            }

            .welcome-msg { text-align: center; margin-bottom: 40px; }
            .guidance { color: var(--bamboo); opacity: 0.7; font-size: 0.9rem; margin-top: 10px; }

            .hud-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; width: 80%; max-width: 800px; }
            .sector { border: 1px solid var(--bamboo); padding: 25px; text-align: center; }
            .label { font-size: 0.7rem; opacity: 0.6; letter-spacing: 2px; margin-bottom: 10px; }

            .continue-btn {
                margin-top: 50px; padding: 15px 60px; border: 1px solid var(--cyan);
                color: var(--cyan); cursor: pointer; letter-spacing: 5px;
                transition: 0.3s; background: transparent; animation: buttonPulse 2s infinite;
            }
            .continue-btn:hover { background: var(--cyan); color: black; box-shadow: 0 0 30px var(--cyan); }
            
            .hint { margin-top: 15px; font-size: 0.7rem; opacity: 0.4; }

            .dash-active .plasma-core { transform: scale(30); opacity: 0; pointer-events: none; }
            .dash-active #engine-hud { display: flex; opacity: 1; }
            
            @keyframes buttonPulse { 0%, 100% { box-shadow: 0 0 5px var(--cyan); } 50% { box-shadow: 0 0 20px var(--cyan); } }
            @keyframes pulse { 0%, 100% { transform: scale(0.95); } 50% { transform: scale(1); } }
        </style>
    </head>
    <body id="main-body">
        <div class="plasma-core" id="core" onclick="openDoor()"></div>
        
        <div id="engine-hud">
            <div class="welcome-msg">
                <h1 style="letter-spacing: 15px; color: var(--bamboo); margin: 0;">VEHICLE ENGAGED</h1>
                <div class="guidance">Let’s get a bit more clarity so we can help you properly.</div>
            </div>
            
            <div class="hud-grid">
                <div class="sector">
                    <div class="label">THRUST STATUS</div>
                    <div style="color: var(--cyan); font-size: 1.5rem;">ACTIVE</div>
                </div>
                <div class="sector">
                    <div class="label">SYSTEM CAPACITY IN USE</div>
                    <div id="hud-energy" style="color: var(--cyan); font-size: 1.5rem;">---</div>
                </div>
            </div>

            <button class="continue-btn" onclick="nextStage()">[ CONTINUE ]</button>
            <div class="hint">We’ll ask a few questions to understand what you’re trying to build.</div>
            
            <div style="margin-top: 40px; font-size: 0.6rem; opacity: 0.2; cursor: pointer;" onclick="closeDoor()">DISENGAGE</div>
        </div>

        <script>
            function openDoor() { document.getElementById('main-body').classList.add('dash-active'); }
            function closeDoor() { document.getElementById('main-body').classList.remove('dash-active'); }
            function nextStage() { alert("Transitioning to Question Protocol..."); }
            
            function updateData() {
                fetch('/api/energy').then(r => r.json()).then(d => {
                    document.getElementById('hud-energy').innerText = d.energy;
                    document.getElementById('core').style.setProperty('--ps', d.speed);
                });
            }
            setInterval(updateData, 5000);
            updateData();
        </script>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
