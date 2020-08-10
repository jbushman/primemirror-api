import json
from flask import request

def post_healthcheck():
    data = request.get_json()
    try:
        with open("/tmp/pmapi-healthcheck.json", "w") as file:
            file.write(json.dumps(data))
        response = {
            "status": "success",
            "message": "New healthcheck successfully created.",
            "data": data
        }
        return response, 201
    except Exception as e:
        response = {
            "status": "fail",
            "message": "POST healthcheck failed.",
            "exception": str(e)
        }
        return response, 409


def get_healthcheck():
    response = {
        "status": "success",
        "message": "system is healthy"
    }
    return response, 200
