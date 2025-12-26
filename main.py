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
        <title>ML11 | Referral Hub</title>
        <style>
            :root { --bamboo: #4dbb5b; --cyan: #00f2ff; --dark: #050a05; --grey: #1a1a1a; }
            body { margin: 0; background: #000; height: 100vh; display: flex; align-items: center; justify-content: center; overflow: hidden; font-family: 'Courier New', monospace; color: white; }
            
            /* Referral Module */
            .referral-module {
                position: fixed; bottom: 20px; left: 20px; width: 280px; min-height: 60px;
                background: var(--grey); border: 1px solid #333; border-radius: 4px;
                padding: 12px 15px; cursor: pointer; transition: 0.3s; z-index: 1000;
                display: flex; flex-direction: column; justify-content: center;
            }
            .referral-module:hover { border-color: var(--bamboo); }
            
            .primary-line { font-size: 0.95rem; color: #fff; letter-spacing: 1px; margin-bottom: 4px; }
            .secondary-line { font-size: 0.65rem; color: #888; letter-spacing: 0.5px; line-height: 1.2; }
            
            /* Success Checkmark */
            #check-icon { position: absolute; top: 10px; right: 10px; color: var(--bamboo); opacity: 0; transition: opacity 0.4s; font-size: 0.8rem; }
            #check-icon.fade { opacity: 1; }

            /* Toast Notification */
            #toast {
                position: fixed; bottom: 100px; left: 20px; padding: 12px 18px;
                background: rgba(5, 10, 5, 0.98); border: 1px solid var(--bamboo);
                font-size: 0.7rem; color: white; opacity: 0; visibility: hidden; 
                transition: 0.4s; z-index: 1100; pointer-events: none;
                display: flex; flex-direction: column; gap: 4px;
            }
            #toast.visible { opacity: 1; visibility: visible; }
            .toast-micro { font-size: 0.55rem; opacity: 0.6; }

            .plasma-core { width: 160px; height: 160px; background: radial-gradient(circle, var(--bamboo), var(--dark)); border-radius: 50%; box-shadow: 0 0 50px var(--bamboo); animation: pulse 4s infinite ease-in-out; }
            
            @media (max-width: 380px) {
                .referral-module { left: 50%; transform: translateX(-50%); width: 90%; }
                #toast { left: 50%; transform: translateX(-50%); width: 80%; text-align: center; }
            }
            @keyframes pulse { 0%, 100% { transform: scale(0.95); } 50% { transform: scale(1); } }
        </style>
    </head>
    <body>
        <div id="toast">
            <div>Referral link copied.</div>
            <div class="toast-micro">Share it — you both get +500 capacity when they activate.</div>
        </div>

        <div class="referral-module" onclick="copyReferral()">
            <div id="check-icon">✓</div>
            <div class="primary-line">Click here to refer a friend</div>
            <div class="secondary-line">Receive additional capacity — 500 units for you + 500 for them.</div>
        </div>
        
        <div class="plasma-core"></div>

        <script>
            async function copyReferral() {
                const url = "https://morphline11.co/rhizome/node-fs3gg";
                const toast = document.getElementById('toast');
                const check = document.getElementById('check-icon');

                try {
                    await navigator.clipboard.writeText(url);
                    check.classList.add('fade');
                    toast.classList.add('visible');

                    setTimeout(() => { check.classList.remove('fade'); }, 1200);
                    setTimeout(() => { toast.classList.remove('visible'); }, 2500);
                } catch (err) {
                    toast.innerHTML = "<div>COPY FAILED. TRY AGAIN.</div>";
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
