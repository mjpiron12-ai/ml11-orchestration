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
        <title>ML11 | The World Visualized</title>
        <style>
            :root { --bamboo: #4dbb5b; --cyan: #00f2ff; --dark: #050a05; }
            body { margin: 0; background: #000; height: 100vh; display: flex; flex-direction: column; overflow: hidden; font-family: 'Courier New', monospace; color: white; }
            
            /* Stage 1: The Core Threshold */
            .plasma-core {
                width: 150px; height: 150px; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
                background: radial-gradient(circle, var(--bamboo), var(--dark));
                border-radius: 50%; box-shadow: 0 0 50px var(--bamboo);
                animation: pulse var(--ps, 4s) infinite ease-in-out;
                cursor: pointer; transition: all 1s ease; z-index: 10;
            }

            /* The Visualized World Space */
            #world-canvas {
                flex-grow: 1; display: none; opacity: 0; flex-direction: column; 
                align-items: center; justify-content: center; transition: opacity 2s ease;
            }

            /* The Interactive Bottom Dock */
            .bottom-dock {
                height: 150px; display: none; justify-content: center; align-items: flex-end; 
                gap: 20px; padding-bottom: 30px; opacity: 0; transition: opacity 2s ease;
            }

            .dock-box {
                border: 1px solid var(--bamboo); padding: 15px; width: 200px; 
                text-align: center; opacity: 0.3; transform: scale(0.9);
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                cursor: pointer; background: rgba(0,0,0,0.8);
            }
            .dock-box:hover { opacity: 1; transform: scale(1.1) translateY(-10px); border-color: var(--cyan); box-shadow: 0 0 20px var(--bamboo); }

            .box-title { font-size: 0.7rem; letter-spacing: 3px; color: var(--bamboo); margin-bottom: 5px; }
            .box-val { font-size: 1.1rem; color: var(--cyan); }

            /* Activation States */
            .world-active .plasma-core { transform: translate(-50%, -50%) scale(0); opacity: 0; pointer-events: none; }
            .world-active #world-canvas, .world-active .bottom-dock { display: flex; opacity: 1; }
            
            @keyframes pulse { 0%, 100% { transform: translate(-50%, -50%) scale(0.95); } 50% { transform: translate(-50%, -50%) scale(1); } }
        </style>
    </head>
    <body id="main-body">
        <div class="plasma-core" id="core" onclick="enterWorld()"></div>
        
        <div id="world-canvas">
            <h1 style="letter-spacing: 20px; color: var(--bamboo);">THE WORLD VISUALIZED</h1>
            <p style="opacity: 0.6; max-width: 600px; text-align: center;">Experience the ML11 logic firing across global nodes. You are currently piloting a Unit of Capacity.</p>
            
            <div style="margin-top: 30px; border: 1px solid var(--cyan); padding: 10px 20px; font-size: 0.8rem; cursor: pointer;">
                [ EXPAND NETWORK / TELL A FRIEND ]
            </div>
        </div>

        <div class="bottom-dock">
            <div class="dock-box" onclick="location.href='/orchestration'">
                <div class="box-title">ORCHESTRATION</div>
                <div class="box-val">ACTIVE</div>
            </div>
            <div class="dock-box" onclick="location.href='/satellite'">
                <div class="box-title">SATELLITE</div>
                <div class="box-val">SYNCED</div>
            </div>
            <div class="dock-box" onclick="location.href='/capacity'">
                <div class="box-title">CAPACITY</div>
                <div id="hud-energy" class="box-val">---</div>
            </div>
        </div>

        <script>
            function enterWorld() { document.getElementById('main-body').classList.add('world-active'); }
            
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
