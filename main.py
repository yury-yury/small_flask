from flask import Flask, request
from redis import Redis


app = Flask(__name__)

app.url_map.strict_slashes = False
app.app_context().push()

redis = Redis(host="redis", port=6379)


@app.route(
    "/",
    methods=[
        "POST",
    ],
)
def func():
    data = request.get_json()
    key = data.get("key")
    value = data.get("value")
    if key and value:
        redis.set(key, value)
        return {data["key"]: data["value"]}, 200
    else:
        return {
            "message": "The requested parameter values 'key' and 'value' must be defined in the body of the request."
        }, 400


@app.route(
    "/<key>",
    methods=[
        "GET",
        "PUT",
    ],
)
def func_(key: str):
    if request.method == "PUT":
        data = request.get_json()
        value = redis.get(key)
        if value:
            redis[key] = data["value"]
            return {key: data["value"]}, 200
    elif request.method == "GET":
        value_bytes = redis.get(key)
        if value_bytes:
            value = value_bytes.decode()
            return {key: value}, 200
        else:
            return {
                "message": f"The database does not have data with the requested key {key}."
            }, 400


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8080)
