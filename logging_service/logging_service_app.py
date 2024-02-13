from flask import Flask, request

app = Flask(__name__)

msg_dict = {}


@app.route('/logging_service', methods=['POST'])
def post_log():
    msg = request.json.get('msg')
    new_uuid = request.json.get('uuid')
    msg_dict[new_uuid] = msg
    print(msg)
    return "Success", 200


@app.route('/logging_service', methods=['GET'])
def get_log():
    return str(list(msg_dict.values())), 200


if __name__ == '__main__':
    app.run(port=8081)
