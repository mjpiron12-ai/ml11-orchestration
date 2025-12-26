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
        <title>MorphLine 11 | Engine HUD</title>
        <style>
            :root { --bamboo: #4dbb5b; --cyan: #00f2ff; --dark: #050a05; }
            body { margin: 0; background: #000; height: 100vh; display: flex; align-items: center; justify-content: center; overflow: hidden; font-family: 'Courier New', monospace; color: white; }
            
            .plasma-core {
                width: 150px; height: 150px;
                background: radial-gradient(circle, var(--bamboo), var(--dark));
                border-radius: 50%; box-shadow: 0 0 50px var(--bamboo);
                animation: pulse var(--ps, 4s) infinite ease-in-out;
                cursor: pointer; transition: all 0.6s cubic-bezier(0.19, 1, 0.22, 1);
                z-index: 10; display: flex; align-items: center; justify-content: center;
            }
            .plasma-core:hover { transform: scale(1.1); box-shadow: 0 0 80px var(--bamboo); }
            .plasma-core:hover::after { content: 'IGNITE'; font-size: 0.8rem; letter-spacing: 4px; color: white; }

            /* The Modular HUD */
            #engine-hud {
                position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                background: rgba(0,0,0,0.95); display: none; opacity: 0;
                grid-template-columns: repeat(3, 1fr); gap: 20px; padding: 50px;
                box-sizing: border-box; z-index: 20; transition: opacity 0.5s;
            }
            .hud-sector { border: 1px solid var(--bamboo); padding: 30px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
            .hud-title { color: var(--bamboo); font-size: 1rem; letter-spacing: 5px; margin-bottom: 20px; border-bottom: 1px solid var(--bamboo); width: 100%; }
            .hud-val { font-size: 1.8rem; color: var(--cyan); }

            .dash-active .plasma-core { transform: scale(0.2); position: fixed; top: 20px; left: 20px; }
            .dash-active #engine-hud { display: grid; opacity: 1; }
            
            @keyframes pulse { 0%, 100% { transform: scale(0.95); opacity: 0.8; } 50% { transform: scale(1); opacity: 1; } }
        </style>
    </head>
    <body id="main-body">
        <div class="plasma-core" id="core" onclick="engageHUD()"></div>
        
        <div id="engine-hud">
            <div class="hud-sector">
                <div class="hud-title">ORCHESTRATION</div>
                <div class="hud-val">ACTIVE</div>
                <p style="font-size: 0.7rem; opacity: 0.5;">Logic flow optimized for 300M+ users.</p>
            </div>
            <div class="hud-sector">
                <div class="hud-title">CAPACITY</div>
                <div class="hud-val" id="hud-energy">---</div>
                <p style="font-size: 0.7rem; opacity: 0.5;">Live global energy throughput.</p>
            </div>
            <div class="hud-sector">
                <div class="hud-title">SATELLITE</div>
                <div class="hud-val">SYNCING</div>
                <p style="font-size: 0.7rem; opacity: 0.5;">Establishing real-time connection nodes.</p>
            </div>
            <p style="grid-column: span 3; color: var(--bamboo); cursor: pointer; margin-top: 20px;" onclick="disengage()">[ RETURN TO CORE ]</p>
        </div>

        <script>
            function engageHUD() { document.getElementById('main-body').classList.add('dash-active'); }
            function disengage() { document.getElementById('main-body').classList.remove('dash-active'); }
            
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
