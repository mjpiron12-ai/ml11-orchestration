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

            .hud-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; width: 90%; max-width: 1100px; margin-top: 30px; }
            .sector { border: 1px solid var(--bamboo); padding: 30px; text-align: center; }
            .hud-title { color: var(--bamboo); font-size: 0.9rem; letter-spacing: 5px; margin-bottom: 15px; border-bottom: 1px solid var(--bamboo); padding-bottom: 10px; }
            .hud-val { font-size: 1.5rem; color: var(--cyan); margin-bottom: 10px; }
            .microcopy { font-size: 0.7rem; opacity: 0.5; line-height: 1.4; }

            .reassurance { margin-bottom: 20px; font-size: 1rem; color: white; opacity: 0.9; letter-spacing: 1px; text-align: center; max-width: 600px; }

            .continue-btn {
                margin-top: 50px; padding: 15px 80px; border: 1px solid var(--cyan);
                color: var(--cyan); cursor: pointer; letter-spacing: 5px;
                transition: 0.3s; background: transparent; font-family: inherit;
            }
            .continue-btn:hover { background: var(--cyan); color: black; box-shadow: 0 0 30px var(--cyan); }
            
            .trust-line { margin-top: 15px; font-size: 0.65rem; opacity: 0.3; letter-spacing: 1px; }

            .dash-active .plasma-core { transform: scale(30); opacity: 0; pointer-events: none; }
            .dash-active #engine-hud { display: flex; opacity: 1; }
            
            @keyframes pulse { 0%, 100% { transform: scale(0.95); } 50% { transform: scale(1); } }
        </style>
    </head>
    <body id="main-body">
        <div class="plasma-core" id="core" onclick="openDoor()"></div>
        
        <div id="engine-hud">
            <div class="reassurance">We’ll ask a few quick questions to understand your goal — nothing is committed yet.</div>
            
            <div class="hud-grid">
                <div class="sector">
                    <div class="hud-title">ORCHESTRATION</div>
                    <div class="hud-val">ACTIVE</div>
                    <div class="microcopy">Structuring your idea so the next steps are clear.</div>
                </div>
                
                <div class="sector">
                    <div class="hud-title">SATELLITE</div>
                    <div class="hud-val">SYNCED</div>
                    <div class="microcopy">Preparing the tools needed to support your goal.</div>
                </div>

                <div class="sector">
                    <div class="hud-title">CAPACITY</div>
                    <div class="hud-val" id="hud-energy">---</div>
                    <div class="microcopy">Shared system capacity. Your usage is well within the free range.</div>
                </div>
            </div>

            <button class="continue-btn" onclick="nextStage()">[ CONTINUE ]</button>
            <div class="trust-line">No credit card required. You’ll see options before anything is final.</div>
            
            <div style="margin-top: 40px; font-size: 0.6rem; opacity: 0.2; cursor: pointer;" onclick="closeDoor()">Return to core</div>
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
