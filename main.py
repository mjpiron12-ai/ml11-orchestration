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

@app.route('/rhizome/<node_id>')
def referral_landing(node_id):
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ML11 | Unit Allocated</title>
        <style>
            :root { --bamboo: #4dbb5b; --dark: #050a05; }
            body { margin: 0; background: #000; height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; overflow: hidden; font-family: 'Courier New', monospace; color: white; }
            .plasma-core {
                width: 160px; height: 160px;
                background: radial-gradient(circle, var(--bamboo), var(--dark));
                border-radius: 50%; box-shadow: 0 0 50px var(--bamboo);
                animation: pulse 4s infinite ease-in-out; cursor: pointer;
                display: flex; align-items: center; justify-content: center;
            }
            .msg { margin-top: 40px; text-align: center; max-width: 400px; line-height: 1.6; }
            @keyframes pulse { 0%, 100% { transform: scale(0.95); } 50% { transform: scale(1); } }
        </style>
    </head>
    <body>
        <div class="plasma-core" onclick="location.href='/'">
            <span style="font-size: 0.7rem; letter-spacing: 2px;">IGNITE</span>
        </div>
        <div class="msg">
            <h2 style="color: var(--bamboo); letter-spacing: 5px;">UNIT ALLOCATED</h2>
            <p style="font-size: 0.8rem; opacity: 0.6;">A peer has shared their system capacity with you. Click the core to initialize your node.</p>
        </div>
    </body>
    </html>
    """)

@app.route('/')
def index():
    # ... (Keep existing index logic with the grey referral box)
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
            .referral-hub {
                position: fixed; bottom: 20px; left: 20px; width: 180px; height: 45px;
                background: var(--mid-grey); border: 1px solid #444; border-radius: 4px;
                display: flex; align-items: center; justify-content: center;
                font-size: 0.65rem; letter-spacing: 2px; color: #888;
                cursor: pointer; z-index: 1000; transition: 0.3s;
            }
            .referral-hub:hover { background: #333; color: var(--bamboo); border-color: var(--bamboo); }
            .plasma-core {
                width: 150px; height: 150px; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
                background: radial-gradient(circle, var(--bamboo), #050a05);
                border-radius: 50%; box-shadow: 0 0 50px var(--bamboo);
                animation: pulse 4s infinite ease-in-out; cursor: pointer;
            }
            #world-canvas { flex-grow: 1; display: none; opacity: 0; flex-direction: column; align-items: center; justify-content: center; transition: 2s; }
            .world-active .plasma-core { display: none; }
            .world-active #world-canvas { display: flex; opacity: 1; }
            @keyframes pulse { 0%, 100% { transform: translate(-50%, -50%) scale(0.95); } 50% { transform: translate(-50%, -50%) scale(1); } }
        </style>
    </head>
    <body id="main-body">
        <div class="referral-hub" onclick="copyReferral()">[ SHARE CAPACITY ]</div>
        <div class="plasma-core" onclick="enterWorld()"></div>
        <div id="world-canvas">
            <h1 style="letter-spacing: 15px; color: var(--bamboo);">SYSTEM VIEW</h1>
            <div style="border: 1px solid #333; padding: 15px 30px; color: #444; cursor: not-allowed; margin-top: 30px;">[ DOWNLOAD WORK ]</div>
        </div>
        <script>
            function enterWorld() { document.getElementById('main-body').classList.add('world-active'); }
            function copyReferral() {
                const link = "https://morphline11.co/rhizome/node-" + Math.random().toString(36).substr(2, 5);
                navigator.clipboard.writeText(link);
                alert("Rhizome Link Copied: " + link);
            }
        </script>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
