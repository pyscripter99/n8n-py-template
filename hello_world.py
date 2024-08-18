from n8n_py import (
    expose_function,
    String,
    Number,
    Boolean,
    Options,
)
from datetime import datetime
from enum import Enum


@expose_function(
    "Add One",
    "Adds one to any number",
    {
        "num": Number(
            friendly_name="Number",
            description="Number to add one to",
            required=True,
            default=5,
        )
    },
)
def addOne(num: int) -> dict:
    return {"result": num + 1}


@expose_function(
    "Add Two Numbers",
    "Adds two numbers",
    {
        "num1": Number(
            friendly_name="Number 1",
            description="First Number",
            required=True,
            default=5,
        ),
        "num2": Number(
            friendly_name="Number 2",
            description="Second Number",
            required=True,
            default=10,
        ),
    },
)
def addTwoNums(num1: int, num2: int) -> dict:
    return {"result": num1 + num2}


class type(str, Enum):
    HI = "HI"
    HELP = "HELP"


@expose_function(
    "Test All",
    "Tests the world!",
    {
        "num": Number(friendly_name="Number", description="", required=True, default=0),
        "string": String(
            friendly_name="String", description="", required=True, default=""
        ),
        "boolean": Boolean(
            friendly_name="Boolean", description="", required=True, default=False
        ),
        "type_": Options(
            friendly_name="Type",
            description="",
            required=True,
            enum=type,
            default=type.HI,
        ),
    },
)
def test(num: int, string: str, boolean: bool, type_: type):
    return {
        "result": "OK",
        "fields": {
            "num": num,
            "string": string,
            "boolean": boolean,
            "type": type_,
        },
    }
