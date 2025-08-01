from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
processed_warnings = []
WEBHOOK_URL = "https://webhook.site/faca2b88-f1e9-4533-8361-f6558730ec63"

# healthcheck
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/notify', methods=['POST'])
def handle_notification():
    # parsen der JSON
    data = request.get_json()

    # überprüfen ob JSON leer
    if not data:
        return jsonify({"error": "Something is wrong with the JSON payload"}), 400

    # überprüfen ob JSON alle Felder enthält
    required_fields = ["Type", "Name", "Description"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: '{field}'"}), 400

    # Filtern auf Type
    notification_type = data["Type"]

    if notification_type == "Warning":

        # Daten für Messenger vorbereiten
        messenger_payload = {
            "type": data["Type"],
            "name": data["Name"],
            "description": data["Description"]
        }

        try:
            response_from_messenger = requests.post(WEBHOOK_URL, json=messenger_payload, timeout=5)
            response_from_messenger.raise_for_status()

            # Logs in Terminal
            print(f"Forwarding WARNING to Messenger")
            print(f"Payload: {messenger_payload}")
            print(f"Messenger response status: {response_from_messenger.status_code}")
            print(f"---------------------------------------" + "\n")

            # Speichern von Warnung
            processed_warnings.append(data)
            return jsonify({"message": "WARNING notification forwarded to messenger"}), 200

        # expection falls das Senden an Messenger nicht geht
        except requests.exceptions.RequestException as e:
            print(f"ERROR sending to messenger: {e}")
            return jsonify({"error": f"Failed to forward WARNING: {e}"}), 500

    elif notification_type == "Info":
        print(f"IGNORING INFO")
        print(f"Type: {data['Type']}")
        print(f"Name: {data['Name']}")
        print(f"Description: {data['Description']}")
        print(f"---------------------" + "\n")
        return jsonify({"message": "Info notification received but not forwarded"}), 200

    else:
        print(f"IGNORING UNKNOWN TYPE: {notification_type}")
        print(f"Name: {data['Name']}")
        print(f"Description: {data['Description']}")
        print(f"-----------------------------------" + "\n")

        return jsonify({"message": f"Notification of type '{notification_type}' received but not forwarded"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)