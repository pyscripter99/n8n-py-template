import json
import base64
from enum import Enum, auto
from . import list_functions
from flask import Flask, jsonify, request


app = Flask(__name__)


class _Status(Enum):
    OK = auto()
    ERROR = auto()


class _Response:
    status: _Status


class _Error(str, _Response):
    status = _Status.ERROR
    message: str

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__()


@app.route("/list")
def handle_list():
    return jsonify([func.serialize() for func in list_functions()])


@app.route("/get_arguments")
def handle_arguments():
    func = [
        func for func in list_functions() if func.name == request.args.get("function")
    ]

    if len(func) == 0:
        return jsonify(_Error("no functions with that id exist"))

    return jsonify(func[0].arguments)


@app.route("/execute", methods=["POST"])
def handle_execute():
    func = [
        func for func in list_functions() if func.name == request.args.get("function")
    ]

    if len(func) == 0:
        return jsonify.dumps(_Error("no functions with that id exist"))

    return jsonify(
        func[0].func(**json.loads(base64.b64decode(request.args.get("arguments"))))
    )


def handle() -> None:
    app.run(host="0.0.0.0", port=5566)
