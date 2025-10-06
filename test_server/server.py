from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
led_status = False

@app.route('/')
def index():
    return render_template('index.html', led_status=led_status)

@app.route('/led-status', methods=['GET'])
def get_led_status():
    return jsonify({'status': led_status})

@app.route('/led-status', methods=['POST'])
def set_led_status():
    global led_status
    data = request.get_json()
    led_status = data.get('status', False)
    return jsonify({'message': 'LED status updated', 'status': led_status})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
