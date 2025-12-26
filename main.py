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
        <title>ML11 | v0.01.1</title>
        <style>
            :root { --bamboo: #4dbb5b; --cyan: #00f2ff; --dark: #050a05; --grey: #1a1a1a; }
            body { margin: 0; background: #000; height: 100vh; display: flex; align-items: center; justify-content: center; overflow: hidden; font-family: 'Courier New', monospace; color: white; }
            
            /* The Core */
            .plasma-core { 
                width: 160px; height: 160px; 
                background: radial-gradient(circle, var(--bamboo), var(--dark)); 
                border-radius: 50%; box-shadow: 0 0 50px var(--bamboo); 
                cursor: pointer; display: flex; align-items: center; justify-content: center; 
                z-index: 10; animation: pulse 4s infinite ease-in-out;
            }
            .verb { font-size: 0.8rem; letter-spacing: 5px; text-shadow: 0 0 10px var(--bamboo); transition: 0.6s; }

            /* Bottom-Left Instrument Dock */
            .referral-hub {
                position: fixed; bottom: 20px; left: 20px; width: 200px; height: 45px;
                background: var(--grey); border: 1px solid #333; border-radius: 4px;
                display: flex; align-items: center; justify-content: center;
                font-size: 0.65rem; letter-spacing: 2px; color: #666; cursor: pointer; transition: 0.3s; z-index: 100;
            }
            .referral-hub:hover { border-color: var(--bamboo); color: var(--bamboo); }
            .referral-hub.copied-state { color: var(--cyan); border-color: var(--cyan); }

            /* The Toast Notification */
            #toast {
                position: fixed; bottom: 75px; left: 20px; padding: 10px 15px;
                background: rgba(5, 10, 5, 0.95); border: 1px solid var(--bamboo);
                font-size: 0.6rem; letter-spacing: 1px; color: white;
                opacity: 0; visibility: hidden; transition: opacity 0.4s, visibility 0.4s;
                z-index: 90; pointer-events: none;
            }
            #toast.visible { opacity: 1; visibility: visible; }

            @keyframes pulse { 0%, 100% { transform: scale(0.95); } 50% { transform: scale(1); } }
        </style>
    </head>
    <body>
        <div id="toast">LINK COPIED. +500 CAPACITY WHEN THEY ACTIVATE.</div>
        <div class="referral-hub" id="ref-btn" onclick="copyReferral()">[ SHARE CAPACITY ]</div>
        
        <div class="plasma-core">
            <span id="verb-text" class="verb">IGNITE</span>
        </div>

        <script>
            const words = ["IGNITE", "ENGAGE", "ALIGN", "ORCHESTRATE", "BUILD", "EVOLVE"];
            let idx = 0;
            setInterval(() => {
                idx = (idx + 1) % words.length;
                document.getElementById('verb-text').textContent = words[idx];
            }, 2800);

            async function copyReferral() {
                const url = "https://morphline11.co/rhizome/node-fs3gg";
                const btn = document.getElementById('ref-btn');
                const toast = document.getElementById('toast');

                try {
                    await navigator.clipboard.writeText(url);
                    btn.innerText = "[ COPIED ]";
                    btn.classList.add('copied-state');
                    toast.classList.add('visible');

                    setTimeout(() => {
                        btn.innerText = "[ SHARE CAPACITY ]";
                        btn.classList.remove('copied-state');
                    }, 1200);

                    setTimeout(() => { toast.classList.remove('visible'); }, 2500);
                } catch (err) {
                    toast.innerText = "COPY FAILED. TRY AGAIN.";
                    toast.style.borderColor = "#ff4444";
                    toast.classList.add('visible');
                    setTimeout(() => toast.classList.remove('visible'), 2500);
                }
            }
        </script>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
