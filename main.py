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
        <title>ML11 | Emergent Engine</title>
        <style>
            :root { --bamboo: #4dbb5b; --cyan: #00f2ff; --dark: #050a05; }
            body { margin: 0; background: #000; height: 100vh; display: flex; align-items: center; justify-content: center; overflow: hidden; font-family: 'Courier New', monospace; color: white; perspective: 1000px; }
            
            .plasma-core {
                width: 170px; height: 170px; position: relative;
                background: radial-gradient(circle, var(--bamboo), var(--dark));
                border-radius: 50%; box-shadow: 0 0 60px var(--bamboo);
                animation: pulse var(--ps, 4s) infinite ease-in-out;
                cursor: pointer; z-index: 10; display: flex; align-items: center; justify-content: center;
            }

            .verb-container { position: relative; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; pointer-events: none; }

            .emergent-verb {
                position: absolute; font-size: 0.85rem; letter-spacing: 5px; font-weight: bold;
                opacity: 0; transform: translateZ(-200px) scale(0.5);
                transition: all 0.6s cubic-bezier(0.165, 0.84, 0.44, 1);
            }

            .verb-active { opacity: 1; transform: translateZ(0) scale(1); text-shadow: 0 0 15px var(--bamboo); }
            .verb-exit { opacity: 0; transform: translateZ(100px) scale(1.5); filter: blur(5px); }

            /* Subtle Referral Hub */
            .referral-hub {
                position: fixed; bottom: 20px; left: 20px; width: 180px; height: 45px;
                background: #1a1a1a; border: 1px solid #333; border-radius: 4px;
                display: flex; align-items: center; justify-content: center;
                font-size: 0.6rem; letter-spacing: 2px; color: #666; cursor: pointer; transition: 0.3s;
            }
            .referral-hub:hover { border-color: var(--bamboo); color: var(--bamboo); }

            @keyframes pulse { 0%, 100% { transform: scale(0.95); } 50% { transform: scale(1); } }
        </style>
    </head>
    <body id="main-body">
        <div class="referral-hub" onclick="copyRef()">[ SHARE CAPACITY ]</div>
        
        <div class="plasma-core" onclick="location.href='/system'">
            <div class="verb-container" id="v-container">
                <span class="emergent-verb verb-active">IGNITE</span>
            </div>
        </div>

        <script>
            const words = ["IGNITE", "ENGAGE", "ALIGN", "ORCHESTRATE", "BUILD", "EVOLVE"];
            let idx = 0;
            const container = document.getElementById("v-container");

            function cycleVerbs() {
                const current = container.querySelector(".verb-active");
                if (current) {
                    current.classList.remove("verb-active");
                    current.classList.add("verb-exit");
                    setTimeout(() => current.remove(), 600);
                }

                idx = (idx + 1) % words.length;
                const next = document.createElement("span");
                next.className = "emergent-verb";
                next.textContent = words[idx];
                container.appendChild(next);

                // Force reflow for animation
                next.offsetHeight; 
                next.classList.add("verb-active");
            }

            setInterval(cycleVerbs, 2800);

            function copyRef() {
                const link = "https://morphline11.co/rhizome/node-fs3gg";
                navigator.clipboard.writeText(link);
                alert("Rhizome Link Copied: " + link);
            }

            function updateData() {
                fetch('/api/energy').then(r => r.json()).then(d => {
                    document.querySelector('.plasma-core').style.setProperty('--ps', d.speed);
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
