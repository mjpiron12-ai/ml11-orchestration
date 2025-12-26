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
        <title>ML11 | The Opening</title>
        <style>
            :root { --bamboo: #4dbb5b; --cyan: #00f2ff; --dark: #050a05; }
            body { margin: 0; background: #000; height: 100vh; display: flex; align-items: center; justify-content: center; overflow: hidden; font-family: 'Courier New', monospace; color: white; }
            
            .plasma-core {
                width: 150px; height: 150px;
                background: radial-gradient(circle, var(--bamboo), var(--dark));
                border-radius: 50%; box-shadow: 0 0 50px var(--bamboo);
                animation: pulse var(--ps, 4s) infinite ease-in-out;
                cursor: pointer; transition: all 0.8s cubic-bezier(0.19, 1, 0.22, 1);
                z-index: 10; display: flex; align-items: center; justify-content: center;
            }

            /* The "Open Door" HUD */
            #engine-hud {
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                background: rgba(0,0,0,0.98); display: none; opacity: 0;
                flex-direction: column; align-items: center; justify-content: center;
                z-index: 20; transition: opacity 1s ease;
            }

            .hud-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; width: 80%; max-width: 1000px; }
            .sector { border: 1px solid var(--bamboo); padding: 30px; text-align: center; transition: 0.3s; }
            .sector:hover { background: rgba(77, 187, 91, 0.1); border-color: var(--cyan); }

            .welcome-msg { margin-bottom: 50px; text-align: center; animation: slideUp 1.5s ease; }
            .dash-active .plasma-core { transform: scale(30); opacity: 0; pointer-events: none; }
            .dash-active #engine-hud { display: flex; opacity: 1; }
            
            @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
            @keyframes pulse { 0%, 100% { transform: scale(0.95); } 50% { transform: scale(1); } }
        </style>
    </head>
    <body id="main-body">
        <div class="plasma-core" id="core" onclick="openDoor()"></div>
        
        <div id="engine-hud">
            <div class="welcome-msg">
                <h1 style="letter-spacing: 10px; color: var(--bamboo);">DOOR OPEN: ML11 ACTIVE</h1>
                <p style="opacity: 0.6;">Welcome to the Orchestration Hub. Select a sector to begin.</p>
            </div>
            <div class="hud-grid">
                <div class="sector" onclick="alert('Brain Sync Active')">
                    <h3 style="color: var(--cyan);">BRAIN</h3>
                    <p style="font-size: 0.7rem;">Logic Orchestration</p>
                </div>
                <div class="sector">
                    <h3 style="color: var(--cyan);">FUEL</h3>
                    <div id="hud-energy" style="font-size: 1.2rem;">---</div>
                    <p style="font-size: 0.7rem;">Live Capacity</p>
                </div>
                <div class="sector" onclick="alert('Satellite Sync Active')">
                    <h3 style="color: var(--cyan);">LINK</h3>
                    <p style="font-size: 0.7rem;">Global Reach</p>
                </div>
            </div>
            <p style="margin-top: 50px; cursor: pointer; color: var(--bamboo);" onclick="closeDoor()">[ CLOSE DOOR ]</p>
        </div>

        <script>
            function openDoor() { document.getElementById('main-body').classList.add('dash-active'); }
            function closeDoor() { document.getElementById('main-body').classList.remove('dash-active'); }
            
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
