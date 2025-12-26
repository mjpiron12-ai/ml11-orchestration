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
        <title>ML11 | v0.01 Threshold</title>
        <style>
            :root { --bamboo: #4dbb5b; --cyan: #00f2ff; --dark: #050a05; --mid-grey: #1a1a1a; }
            body { margin: 0; background: #000; height: 100vh; display: flex; align-items: center; justify-content: center; overflow: hidden; font-family: 'Courier New', monospace; color: white; perspective: 1000px; }
            
            /* Persistent Referral Hub */
            .referral-hub {
                position: fixed; bottom: 20px; left: 20px; width: 180px; height: 45px;
                background: var(--mid-grey); border: 1px solid #333; border-radius: 4px;
                display: flex; align-items: center; justify-content: center;
                font-size: 0.65rem; letter-spacing: 2px; color: #666; cursor: pointer; transition: 0.3s; z-index: 1000;
            }
            .referral-hub:hover { border-color: var(--bamboo); color: var(--bamboo); }
            
            /* Toast */
            #toast { position: fixed; bottom: 80px; left: 20px; padding: 10px 15px; background: rgba(5,10,5,0.9); border: 1px solid var(--bamboo); font-size: 0.6rem; opacity: 0; transition: 0.4s; z-index: 1100; pointer-events: none; }
            #toast.visible { opacity: 1; }

            /* HUD & Question Protocol */
            #engine-hud { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #000; display: none; opacity: 0; flex-direction: column; align-items: center; justify-content: center; z-index: 500; transition: 1s; }
            #question-stage { display: none; text-align: center; max-width: 600px; }
            
            .world-active #engine-hud { display: flex; opacity: 1; }
            .question-active #hud-grid, .question-active .reassurance { display: none; }
            .question-active #question-stage { display: block; }

            .plasma-core { width: 150px; height: 150px; background: radial-gradient(circle, var(--bamboo), var(--dark)); border-radius: 50%; box-shadow: 0 0 50px var(--bamboo); cursor: pointer; display: flex; align-items: center; justify-content: center; z-index: 10; }
            .emergent-verb { position: absolute; font-size: 0.8rem; letter-spacing: 5px; opacity: 0; transform: translateZ(-100px); transition: 0.6s; }
            .verb-active { opacity: 1; transform: translateZ(0); }

            .btn { margin-top: 40px; padding: 15px 40px; border: 1px solid var(--cyan); color: var(--cyan); background: transparent; cursor: pointer; font-family: inherit; letter-spacing: 3px; }
            .btn:hover { background: var(--cyan); color: black; }
        </style>
    </head>
    <body id="main-body">
        <div id="toast">LINK COPIED. +500 CAPACITY ON ACTIVATION.</div>
        <div class="referral-hub" id="ref-btn" onclick="copyRef()">[ SHARE CAPACITY ]</div>
        
        <div class="plasma-core" id="core" onclick="enterWorld()">
            <span id="verb" class="emergent-verb verb-active">IGNITE</span>
        </div>

        <div id="engine-hud">
            <div id="hud-content" style="text-align:center;">
                <div class="reassurance">Preparing the tools needed to support your goal.</div>
                <button class="btn" onclick="startQuestions()">[ CONTINUE ]</button>
            </div>

            <div id="question-stage">
                <h2 style="color: var(--bamboo); letter-spacing: 8px;">PROTOCOL 01</h2>
                <p style="opacity: 0.7;">What is your primary orchestration goal?</p>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 30px;">
                    <div class="btn" style="padding:20px;" onclick="alert('Demo Path Initializing...')">I WANT A DEMO</div>
                    <div class="btn" style="padding:20px;" onclick="alert('Live Node Initializing...')">I WANT TO BUILD LIVE</div>
                </div>
            </div>
        </div>

        <script>
            const words = ["IGNITE", "ENGAGE", "ALIGN", "ORCHESTRATE", "BUILD", "EVOLVE"];
            let idx = 0;
            setInterval(() => {
                idx = (idx + 1) % words.length;
                document.getElementById('verb').textContent = words[idx];
            }, 2800);

            function enterWorld() { document.getElementById('main-body').classList.add('world-active'); }
            function startQuestions() { document.getElementById('main-body').classList.add('question-active'); }
            
            function copyRef() {
                navigator.clipboard.writeText("https://morphline11.co/rhizome/node-fs3gg").then(() => {
                    const b = document.getElementById('ref-btn');
                    const t = document.getElementById('toast');
                    b.innerText = "[ COPIED ]";
                    t.classList.add('visible');
                    setTimeout(() => { b.innerText = "[ SHARE CAPACITY ]"; t.classList.remove('visible'); }, 2000);
                });
            }
        </script>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
