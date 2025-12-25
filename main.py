from flask import Flask, render_template_string, jsonify
import os
import requests

app = Flask(__name__)

@app.route('/api/energy')
def get_energy():
    # Fetch real-time data to fuel the plasma state
    try:
        # Using a public API to simulate "Global Hub Energy"
        res = requests.get('https://api.coinbase.com/v2/prices/BTC-USD/spot')
        price = float(res.json()['data']['amount'])
        # Map the price to a pulse frequency (higher price = higher energy)
        pulse_speed = max(1, 10 - (price / 10000)) 
        return jsonify({"speed": f"{pulse_speed}s", "energy": price})
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
        <title>MORPHLINE 11 | PLASMA FUELED</title>
        <style>
            body { margin: 0; background: #000; height: 100vh; display: flex; align-items: center; justify-content: center; overflow: hidden; font-family: sans-serif; color: white; }
            
            .plasma-core {
                width: 180px; height: 180px;
                background: radial-gradient(circle, #ff00ff, #001a1a); /* Shift to Plasma Purple */
                border-radius: 50%;
                box-shadow: 0 0 60px #ff00ff;
                animation: pulse var(--pulse-speed, 4s) infinite ease-in-out;
                transition: all 1s ease;
            }

            #energy-metrics { position: absolute; top: 10%; letter-spacing: 4px; font-weight: bold; color: #ff00ff; }
            #status { position: absolute; bottom: 5%; opacity: 0.5; font-size: 0.7rem; }

            @keyframes pulse {
                0%, 100% { transform: scale(0.9); opacity: 0.6; }
                50% { transform: scale(1.1); opacity: 1; }
            }
        </style>
    </head>
    <body>
        <div id="energy-metrics">GLOBAL CAPACITY: <span id="val">LOADING</span></div>
        <div class="plasma-core" id="core"></div>
        <div id="status">STAGE: PLASMA | REAL-TIME DATA BINDING ACTIVE</div>

        <script>
            function updatePlasma() {
                // Fetch real-time energy metrics from our Flask API
                fetch('/api/energy')
                    .then(res => res.json())
                    .then(data => {
                        document.getElementById('val').innerText = data.energy;
                        document.getElementById('core').style.setProperty('--pulse-speed', data.speed);
                    });
            }
            // Update the plasma state every 5 seconds
            setInterval(updatePlasma, 5000);
            updatePlasma();
        </script>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
