from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, this is a simple HTTP API server!'

@app.route('/webhook', methods=['POST'])
def line_webhook():
    data = request.get_json()
    print("Received LINE Webhook：")
    print(data)
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
