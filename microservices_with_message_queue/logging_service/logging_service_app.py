import hazelcast
from flask import Flask, request

app = Flask(__name__)

client = hazelcast.HazelcastClient(
    cluster_name="hw4_klym",
    cluster_members=["127.18.0.2:5703"]
)
log_map = client.get_map("log").blocking()


@app.route('/logging_service', methods=['POST'])
def post_log():
    msg = request.json.get('msg')
    new_uuid = request.json.get('uuid')
    log_map.put(new_uuid, msg)
    print(msg)
    return "Success", 200


@app.route('/logging_service', methods=['GET'])
def get_log():
    return str(list(log_map.values())), 200


if __name__ == '__main__':
    app.run(port=8083)
