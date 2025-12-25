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
        <title>MorphLine 11 | Bamboo Core</title>
        <style>
            :root { --bamboo: #4dbb5b; --cyan: #00f2ff; }
            body { margin: 0; background: #000; height: 100vh; display: flex; align-items: center; justify-content: center; overflow: hidden; font-family: 'Courier New', monospace; color: white; }
            
            /* Bamboo Unit Core */
            .plasma-core {
                width: 150px; height: 150px;
                background: radial-gradient(circle, var(--bamboo), #0a1a0a);
                border-radius: 50%;
                box-shadow: 0 0 50px var(--bamboo);
                animation: pulse var(--ps, 4s) infinite ease-in-out;
                cursor: pointer; transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                z-index: 10; display: flex; align-items: center; justify-content: center;
            }

            /* Hover Signal */
            .plasma-core:hover { transform: scale(1.2); box-shadow: 0 0 80px var(--bamboo); }
            .plasma-core::after { content: 'ENGAGE'; font-size: 0.7rem; letter-spacing: 2px; opacity: 0; transition: opacity 0.3s; }
            .plasma-core:hover::after { opacity: 1; }

            #vehicle-dash {
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                background: #000; display: none; opacity: 0; flex-direction: column; 
                align-items: center; justify-content: center; z-index: 20;
                transition: opacity 1s ease;
            }
            .dash-active .plasma-core { transform: scale(30); opacity: 0; pointer-events: none; }
            .dash-active #vehicle-dash { display: flex; opacity: 1; }
            
            .grid-overlay { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; padding: 20px; border: 1px solid var(--bamboo); }
            .stat-box { border: 1px solid var(--cyan); padding: 15px; text-align: center; }
            .stat-val { font-size: 1.5rem; color: var(--cyan); }
            @keyframes pulse { 0%, 100% { transform: scale(0.9); opacity: 0.7; } 50% { transform: scale(1); opacity: 1; } }
        </style>
    </head>
    <body id="main-body">
        <div class="plasma-core" id="core" onclick="engageVehicle()"></div>
        
        <div id="vehicle-dash">
            <h1 style="letter-spacing: 15px; color: var(--bamboo);">VEHICLE ENGAGED</h1>
            <div class="grid-overlay">
                <div class="stat-box"><div>THRUST</div><div class="stat-val">ACTIVE</div></div>
                <div class="stat-box"><div>GLOBAL ENERGY</div><div class="stat-val" id="dash-energy">---</div></div>
            </div>
            <p style="margin-top: 40px; cursor: pointer; color: var(--cyan);" onclick="disengage()">[ DISENGAGE ]</p>
        </div>

        <script>
            function engageVehicle() { document.getElementById('main-body').classList.add('dash-active'); }
            function disengage() { document.getElementById('main-body').classList.remove('dash-active'); }
            
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
