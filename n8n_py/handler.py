import json
import sys
import base64
from enum import Enum, auto, EnumType
from . import list_functions
from dataclasses import is_dataclass, asdict, dataclass
from datetime import datetime


class _CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if is_dataclass(obj):
            return asdict(obj)
        if hasattr(obj, "__json__"):
            return obj.__json__()
        if isinstance(obj, EnumType):
            return obj._member_names_
        return super().default(obj)


@dataclass
class _ArgumentsRequest:
    function_name: str


@dataclass
class _ExecuteRequest:
    function_name: str
    data: dict[str, any]


class _OperationMode(Enum):
    LIST = auto()
    ARGUMENTS = auto()
    EXECUTE = auto()


class _Command(Enum):
    GET_ARGUMENTS = auto()
    EXECUTE = auto()


class _OperationCommand:
    command: _Command
    data: dict

    def __init__(self, command: str, data: dict) -> None:
        self.command = _Command[command]
        self.data = data


class _Status(Enum):
    OK = auto()
    ERROR = auto()


class _Response:
    status: _Status


class _Error(_Response):
    status = _Status.ERROR
    message: str

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__()

    def __json__(self) -> dict:
        dct = self.__dict__
        dct["status"] = self.status.name
        return dct


def handle() -> None:
    MODE = _OperationMode.LIST
    data: _ArgumentsRequest | None = None

    if len(sys.argv) == 2:
        command = _OperationCommand(**json.loads(base64.b64decode(sys.argv[1])))

        if command.command == _Command.GET_ARGUMENTS:
            MODE = _OperationMode.ARGUMENTS
            data = _ArgumentsRequest(**command.data)
        if command.command == _Command.EXECUTE:
            MODE = _OperationMode.EXECUTE
            data = _ExecuteRequest(**command.data)

    if MODE == _OperationMode.LIST:
        print(
            json.dumps(
                [func.serialize() for func in list_functions()], cls=_CustomEncoder
            )
        )
    elif MODE == _OperationMode.ARGUMENTS:
        data: _ArgumentsRequest = data

        func = [func for func in list_functions() if func.name == data.function_name]

        if len(func) == 0:
            print(
                json.dumps(
                    _Error("no functions with that id exist"), cls=_CustomEncoder
                )
            )
            exit(1)

        print(json.dumps(func[0].arguments, cls=_CustomEncoder))
    elif MODE == _OperationMode.EXECUTE:
        data: _ExecuteRequest = data

        func = [func for func in list_functions() if func.name == data.function_name]

        if len(func) == 0:
            print(
                json.dumps(
                    _Error("no functions with that id exist"), cls=_CustomEncoder
                )
            )
            exit(1)

        print(json.dumps(func[0].func(**data.data), cls=_CustomEncoder))
