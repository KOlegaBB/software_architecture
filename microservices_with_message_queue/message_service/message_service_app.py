import hazelcast
from flask import Flask
import threading

app = Flask(__name__)

client = hazelcast.HazelcastClient(
    cluster_name="hw4_klym",
    cluster_members=["127.18.0.2:5704"]
)

messages = []
msg_queue = client.get_queue("message_queue").blocking()


def consume():
    while True:
        msg = msg_queue.take()
        print(msg)
        messages.append(msg)


threading.Thread(target=consume, daemon=True).start()


@app.route('/message_service', methods=['GET'])
def get_message():
    return messages, 200


if __name__ == '__main__':
    app.run(port=8085)
