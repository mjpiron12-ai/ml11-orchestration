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
        <title>ML11 | The Breathing Engine</title>
        <style>
            :root { --bamboo: #4dbb5b; --cyan: #00f2ff; --dark: #050a05; }
            body { margin: 0; background: #000; height: 100vh; display: flex; flex-direction: column; overflow: hidden; font-family: 'Courier New', monospace; color: white; }
            
            /* The Glowing Core */
            .plasma-core {
                width: 160px; height: 160px; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
                background: radial-gradient(circle, var(--bamboo), var(--dark));
                border-radius: 50%; box-shadow: 0 0 50px var(--bamboo);
                animation: pulse var(--ps, 4s) infinite ease-in-out;
                cursor: pointer; transition: all 1s ease; z-index: 10;
                display: flex; align-items: center; justify-content: center;
            }

            /* Word Loop Styling */
            .ignite-word {
                font-size: 0.8rem; letter-spacing: 0.15em; font-weight: bold;
                transition: opacity 0.6s ease-in-out, text-shadow 0.6s ease-in-out;
            }
            .fade-out { opacity: 0; }
            .fade-in { opacity: 1; text-shadow: 0 0 12px var(--bamboo); }

            #world-canvas { flex-grow: 1; display: none; opacity: 0; flex-direction: column; align-items: center; justify-content: center; transition: opacity 2s ease; }
            .bottom-dock { height: 150px; display: none; justify-content: center; align-items: flex-end; gap: 20px; padding-bottom: 30px; opacity: 0; transition: opacity 2s ease; }
            .dock-box { border: 1px solid var(--bamboo); padding: 15px; width: 200px; text-align: center; opacity: 0.3; transition: 0.4s; cursor: pointer; background: rgba(0,0,0,0.8); }
            .dock-box:hover { opacity: 1; transform: scale(1.1) translateY(-10px); border-color: var(--cyan); box-shadow: 0 0 20px var(--bamboo); }

            .world-active .plasma-core { transform: translate(-50%, -50%) scale(0); opacity: 0; pointer-events: none; }
            .world-active #world-canvas, .world-active .bottom-dock { display: flex; opacity: 1; }
            
            @keyframes pulse { 0%, 100% { transform: translate(-50%, -50%) scale(0.95); } 50% { transform: translate(-50%, -50%) scale(1); } }
        </style>
    </head>
    <body id="main-body">
        <div class="plasma-core" id="ignite-trigger" onclick="enterWorld()">
            <span id="ignite-word" class="ignite-word">IGNITE</span>
        </div>
        
        <div id="world-canvas">
            <h1 style="letter-spacing: 20px; color: var(--bamboo);">WORLD VISUALIZED</h1>
            <div style="margin-top: 30px; border: 1px solid var(--cyan); padding: 10px 20px; font-size: 0.8rem; cursor: pointer;">
                [ EXPAND NETWORK ]
            </div>
        </div>

        <div class="bottom-dock">
            <div class="dock-box"><div style="font-size:0.7rem; color:var(--bamboo);">ORCHESTRATION</div><div>ACTIVE</div></div>
            <div class="dock-box"><div style="font-size:0.7rem; color:var(--bamboo);">SATELLITE</div><div>SYNCED</div></div>
            <div class="dock-box"><div style="font-size:0.7rem; color:var(--bamboo);">CAPACITY</div><div id="hud-energy">---</div></div>
        </div>

        <script>
            const words = ["IGNITE", "ENGAGE", "ALIGN", "ORCHESTRATE", "BUILD", "EVOLVE"];
            let idx = 0;
            let interval = null;
            const wordEl = document.getElementById("ignite-word");
            const trigger = document.getElementById("ignite-trigger");

            function startLoop() {
                if (interval) return;
                interval = setInterval(() => {
                    wordEl.classList.add("fade-out");
                    setTimeout(() => {
                        idx = (idx + 1) % words.length;
                        wordEl.textContent = words[idx];
                        wordEl.classList.remove("fade-out");
                        wordEl.classList.add("fade-in");
                    }, 600);
                }, 2800);
            }

            function stopLoop() {
                clearInterval(interval);
                interval = null;
                idx = 0;
                wordEl.textContent = "IGNITE";
                wordEl.classList.remove("fade-out", "fade-in");
            }

            trigger.addEventListener("mouseenter", startLoop);
            trigger.addEventListener("mouseleave", stopLoop);

            function enterWorld() { document.getElementById('main-body').classList.add('world-active'); }
            
            function updateData() {
                fetch('/api/energy').then(r => r.json()).then(d => {
                    document.getElementById('hud-energy').innerText = d.energy;
                    trigger.style.setProperty('--ps', d.speed);
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
