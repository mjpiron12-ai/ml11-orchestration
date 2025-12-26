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
        <title>ML11 | The Possibility Window</title>
        <style>
            :root { --bamboo: #4dbb5b; --cyan: #00f2ff; --dark: #050a05; }
            body { margin: 0; background: #000; height: 100vh; display: flex; flex-direction: column; overflow: hidden; font-family: 'Courier New', monospace; color: white; }
            
            /* The Glowing Ignition Point */
            .plasma-core {
                width: 160px; height: 160px; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
                background: radial-gradient(circle, var(--bamboo), var(--dark));
                border-radius: 50%; box-shadow: 0 0 50px var(--bamboo);
                animation: pulse var(--ps, 4s) infinite ease-in-out;
                cursor: pointer; transition: all 1s ease; z-index: 100;
                display: flex; align-items: center; justify-content: center;
            }
            .ignite-word { font-size: 0.8rem; letter-spacing: 0.15em; transition: opacity 0.6s; }
            .fade-out { opacity: 0; }

            /* Hero Content: The Window */
            #world-canvas { flex-grow: 1; display: none; opacity: 0; flex-direction: column; align-items: center; justify-content: center; transition: opacity 2s ease; text-align: center; }
            
            /* The Interactive Bottom Dock (Power User Layer) */
            .bottom-dock {
                height: 180px; display: none; justify-content: center; align-items: flex-end; 
                gap: 20px; padding-bottom: 40px; opacity: 0; transition: opacity 2s ease;
            }
            .dock-box {
                border: 1px solid var(--bamboo); padding: 20px; width: 220px; 
                opacity: 0.2; transform: scale(0.9); cursor: pointer;
                transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                background: rgba(0,0,0,0.9);
            }
            .dock-box:hover { opacity: 1; transform: scale(1.1) translateY(-15px); border-color: var(--cyan); box-shadow: 0 0 30px var(--bamboo); }
            .box-title { font-size: 0.7rem; letter-spacing: 4px; color: var(--bamboo); margin-bottom: 8px; }
            .box-val { font-size: 1.2rem; color: var(--cyan); }

            .world-active .plasma-core { transform: translate(-50%, -50%) scale(0); opacity: 0; pointer-events: none; }
            .world-active #world-canvas, .world-active .bottom-dock { display: flex; opacity: 1; }
            
            @keyframes pulse { 0%, 100% { transform: translate(-50%, -50%) scale(0.95); } 50% { transform: translate(-50%, -50%) scale(1); } }
        </style>
    </head>
    <body id="main-body">
        <div class="plasma-core" id="trigger" onclick="enterWorld()">
            <span id="word" class="ignite-word">IGNITE</span>
        </div>
        
        <div id="world-canvas">
            <h1 style="letter-spacing: 20px; color: var(--bamboo); margin: 0;">POSSIBILITY VISUALIZED</h1>
            <p style="opacity: 0.7; margin-top: 20px; max-width: 600px;">We’re organizing your intent into a workable system flow. Nothing is committed yet.</p>
            
            <div style="margin-top: 40px; border: 1px solid var(--cyan); padding: 15px 40px; font-size: 0.9rem; cursor: pointer; color: var(--cyan);" onclick="alert('Proceeding to Question Protocol...')">
                [ CONTINUE ]
            </div>
            <div style="margin-top: 15px; font-size: 0.65rem; opacity: 0.3; letter-spacing: 1px;">No credit card required. You’ll see options before anything is final.</div>
        </div>

        <div class="bottom-dock">
            <div class="dock-box">
                <div class="box-title">ORCHESTRATION</div>
                <div class="box-val">ACTIVE</div>
                <p style="font-size: 0.6rem; opacity: 0.5; margin-top: 10px;">Structuring the logic path.</p>
            </div>
            <div class="dock-box">
                <div class="box-title">SATELLITE</div>
                <div class="box-val">SYNCED</div>
                <p style="font-size: 0.6rem; opacity: 0.5; margin-top: 10px;">Connecting required nodes.</p>
            </div>
            <div class="dock-box">
                <div class="box-title">CAPACITY</div>
                <div id="hud-energy" class="box-val">---</div>
                <p style="font-size: 0.6rem; opacity: 0.5; margin-top: 10px;">Usage: Free Range.</p>
            </div>
        </div>

        <script>
            const words = ["IGNITE", "ENGAGE", "ALIGN", "ORCHESTRATE", "BUILD", "EVOLVE"];
            let idx = 0;
            const wordEl = document.getElementById("word");
            const trigger = document.getElementById("trigger");

            trigger.addEventListener("mouseenter", () => {
                this.loop = setInterval(() => {
                    wordEl.classList.add("fade-out");
                    setTimeout(() => {
                        idx = (idx + 1) % words.length;
                        wordEl.textContent = words[idx];
                        wordEl.classList.remove("fade-out");
                    }, 600);
                }, 2800);
            });
            trigger.addEventListener("mouseleave", () => {
                clearInterval(this.loop);
                wordEl.textContent = "IGNITE";
            });

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
