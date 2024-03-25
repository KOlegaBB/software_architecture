from flask import Flask

app = Flask(__name__)


@app.route('/message_service', methods=['GET'])
def get_message():
    response = "not implemented yet"
    return response, 200


if __name__ == '__main__':
    app.run(port=8082)
