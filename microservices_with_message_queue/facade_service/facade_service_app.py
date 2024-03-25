import random
import hazelcast
from flask import Flask, request
import requests
import uuid

app = Flask(__name__)

logging_service_urls = ["http://localhost:8081", "http://localhost:8082",
                        "http://localhost:8083"]
messages_service_urls = ["http://localhost:8084", "http://localhost:8085"]

client = hazelcast.HazelcastClient(
    cluster_name="hw4_klym",
    cluster_members=["127.18.0.2:5704"]
)

messages = []
msg_queue = client.get_queue("message_queue").blocking()


@app.route('/facade_service', methods=['POST'])
def post_facade():
    msg = request.json
    new_uuid = uuid.uuid4()
    logging_service_url = random.choice(logging_service_urls)
    response = requests.post(f"{logging_service_url}/logging_service",
                             json={'uuid': str(new_uuid), 'msg': msg})
    msg_queue.offer(msg)
    if response.status_code != 200:
        return "Error", response.status_code
    return "Success", 200


@app.route('/facade_service', methods=['GET'])
def get_message():
    logging_service_url = random.choice(logging_service_urls)
    messages_service_url = random.choice(messages_service_urls)
    try:
        response_log = requests.get(f"{logging_service_url}/logging_service")
        response_message = requests.get(
            f"{messages_service_url}/message_service")
    except requests.exceptions.ConnectionError:
        return "Error", 500
    return response_log.text + ": " + response_message.text, 200


if __name__ == '__main__':
    app.run(port=8080)
