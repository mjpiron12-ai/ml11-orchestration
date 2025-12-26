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
        <title>ML11 | The Hub</title>
        <style>
            :root { --bamboo: #4dbb5b; --cyan: #00f2ff; --mid-grey: #2a2a2a; }
            body { margin: 0; background: #000; height: 100vh; display: flex; flex-direction: column; overflow: hidden; font-family: 'Courier New', monospace; color: white; }
            
            /* Persistent Referral Box (Bottom Left) */
            .referral-hub {
                position: fixed; bottom: 20px; left: 20px; width: 180px; height: 45px;
                background: var(--mid-grey); border: 1px solid #444; border-radius: 4px;
                display: flex; align-items: center; justify-content: center;
                font-size: 0.65rem; letter-spacing: 2px; color: #888;
                cursor: pointer; z-index: 1000; transition: all 0.3s ease;
            }
            .referral-hub:hover { background: #333; color: var(--bamboo); border-color: var(--bamboo); }
            .referral-hub:active { transform: scale(0.95); }

            /* Ignition Core */
            .plasma-core {
                width: 150px; height: 150px; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
                background: radial-gradient(circle, var(--bamboo), #050a05);
                border-radius: 50%; box-shadow: 0 0 50px var(--bamboo);
                animation: pulse var(--ps, 4s) infinite ease-in-out;
                cursor: pointer; z-index: 10;
            }

            /* Main World View */
            #world-canvas { flex-grow: 1; display: none; opacity: 0; flex-direction: column; align-items: center; justify-content: center; transition: opacity 2s ease; }
            
            /* Capacity Display */
            .cap-indicator { margin-top: 20px; font-size: 0.7rem; color: var(--cyan); }
            .download-lock { margin-top: 30px; padding: 15px 30px; border: 1px solid #333; color: #444; cursor: not-allowed; }

            .world-active .plasma-core { display: none; }
            .world-active #world-canvas { display: flex; opacity: 1; }
            
            @keyframes pulse { 0%, 100% { transform: translate(-50%, -50%) scale(0.95); } 50% { transform: translate(-50%, -50%) scale(1); } }
            @keyframes pulse-grey { 0%, 100% { box-shadow: 0 0 5px var(--mid-grey); } 50% { box-shadow: 0 0 20px var(--bamboo); } }
            .pulse-request { animation: pulse-grey 1s infinite; color: var(--bamboo) !important; border-color: var(--bamboo) !important; }
        </style>
    </head>
    <body id="main-body">
        <div class="referral-hub" id="ref-box" onclick="copyReferral()">
            [ SHARE CAPACITY ]
        </div>

        <div class="plasma-core" id="core" onclick="enterWorld()"></div>
        
        <div id="world-canvas">
            <h1 style="letter-spacing: 15px; color: var(--bamboo);">SYSTEM VIEW</h1>
            <div class="cap-indicator">ORCHESTRATION LOAD: 92% (LIMIT REACHED)</div>
            
            <div class="download-lock" onclick="triggerReferralPulse()">
                [ DOWNLOAD WORK ]
            </div>
            <p style="font-size: 0.6rem; opacity: 0.4; margin-top: 10px;">Expand capacity via referral hub to unlock download.</p>
        </div>

        <script>
            function enterWorld() { document.getElementById('main-body').classList.add('world-active'); }
            
            function triggerReferralPulse() {
                const refBox = document.getElementById('ref-box');
                refBox.classList.add('pulse-request');
                setTimeout(() => refBox.classList.remove('pulse-request'), 3000);
            }

            function copyReferral() {
                const link = "https://morphline11.co/rhizome/private-node-" + Math.random().toString(36).substr(2, 5);
                navigator.clipboard.writeText(link);
                alert("Rhizome Link Copied: " + link + "\\nShare to expand your unit's capacity.");
            }
            
            function updateData() {
                fetch('/api/energy').then(r => r.json()).then(d => {
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
