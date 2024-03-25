from flask import Flask, request
import requests
import uuid

app = Flask(__name__)

logging_service_url = "http://localhost:8081"
messages_service_url = "http://localhost:8082"


@app.route('/facade_service', methods=['POST'])
def post_facade():
    msg = request.json
    new_uuid = uuid.uuid4()
    requests.post(f"{logging_service_url}/logging_service",
                  json={'uuid': str(new_uuid), 'msg': msg})
    return "Success", 200


@app.route('/facade_service', methods=['GET'])
def get_message():
    response_log = requests.get(f"{logging_service_url}/logging_service")
    response_message = requests.get(f"{messages_service_url}/message_service")
    return response_log.text + ": " + response_message.text, 200


if __name__ == '__main__':
    app.run(port=8080)
