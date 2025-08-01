from flask import Flask, jsonify

app = Flask(__name__)
processed_warnings = []

# healthcheck
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)