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
        
        <title>MorphLine 11 | Official Global Hub</title>
        <meta name="description" content="Official headquarters of ML11. Access the Plasma-fueled vehicle, global units of capacity, and real-time energy orchestration.">
        <link rel="canonical" href="https://morphline11.co/" />
        
        <style>
            :root { --plasma: #ff00ff; --cyan: #00f2ff; }
            body { margin: 0; background: #000; height: 100vh; display: flex; align-items: center; justify-content: center; overflow: hidden; font-family: 'Courier New', monospace; color: white; }
            .plasma-core {
                width: 150px; height: 150px;
                background: radial-gradient(circle, var(--plasma), #110011);
                border-radius: 50%;
                box-shadow: 0 0 50px var(--plasma);
                animation: pulse var(--ps, 4s) infinite ease-in-out;
                cursor: pointer; transition: all 0.8s cubic-bezier(0.85, 0, 0.15, 1);
                z-index: 10;
            }
            #vehicle-dash {
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                background: linear-gradient(180deg, #000 0%, #110011 100%);
                display: none; opacity: 0; flex-direction: column; 
                align-items: center; justify-content: center; z-index: 20;
                transition: opacity 1s ease;
            }
            .dash-active .plasma-core { transform: scale(20); opacity: 0; }
            .dash-active #vehicle-dash { display: flex; opacity: 1; }
            .grid-overlay { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; padding: 40px; border: 1px solid var(--plasma); }
            .stat-box { border: 1px solid var(--cyan); padding: 20px; text-align: center; }
            .stat-val { font-size: 2rem; color: var(--cyan); text-shadow: 0 0 10px var(--cyan); }
            @keyframes pulse { 0%, 100% { transform: scale(0.9); opacity: 0.6; } 50% { transform: scale(1.1); opacity: 1; } }
        </style>
    </head>
    <body id="main-body">
        <div class="plasma-core" id="core" onclick="engageVehicle()"></div>
        <div id="vehicle-dash">
            <h1 style="letter-spacing: 15px; color: var(--plasma);">VEHICLE ENGAGED</h1>
            <div class="grid-overlay">
                <div class="stat-box"><div>THRUST</div><div class="stat-val">ACTIVE</div></div>
                <div class="stat-box"><div>ENERGY</div><div class="stat-val" id="dash-energy">---</div></div>
                <div class="stat-box"><div>STAGE</div><div class="stat-val">PLASMA</div></div>
                <div class="stat-box"><div>CAPACITY</div><div class="stat-val">MAX</div></div>
            </div>
            <p style="margin-top: 40px; cursor: pointer; color: var(--cyan);" onclick="disengage()">[ DISENGAGE ]</p>
        </div>
        <script>
            function engageVehicle() { document.getElementById('main-body').classList.add('dash-active'); }
            function disengage() { document.getElementById('main-body').classList.remove('dash-active'); }
            document.addEventListener('keydown', (e) => {
                if (['/', ';', "'"].includes(e.key)) engageVehicle();
                if (e.key === 'Escape') disengage();
            });
            function updateData() {
                fetch('/api/energy').then(r => r.json()).then(d => {
                    document.getElementById('dash-energy').innerText = d.energy;
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
