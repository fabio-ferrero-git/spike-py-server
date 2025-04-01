from flask import Flask, request, Response, stream_with_context
from flask import jsonify
from waitress import serve
from functools import wraps

import db_connector

app = Flask(__name__)

#
# Non interessante
#
def handle_cors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.method == 'OPTIONS':
            return Response(status=204, headers={
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS, GET, POST',
                'Access-Control-Allow-Headers': 'Content-Type'
            })
        return f(*args, **kwargs)
    return wrapper


@app.route('/test-get-user', methods=['GET', 'OPTIONS'], strict_slashes=False)
def test_get_user():
    user_id = request.args.get('user_id')
    print(user_id)
    u = db_connector.get_single_user(user_id)
    return jsonify(u)


@app.route('/test-get-all-users', methods=['GET', 'OPTIONS'], strict_slashes=False)
def test_get_all_users():
    u = db_connector.get_all_users()
    return jsonify(u)


@app.route('/add-user', methods=['POST', 'OPTIONS'], strict_slashes=False)
@handle_cors
def add_user():
    try:
        data = request.get_json(force=True)
        user_data = data.get("user")
        user = db_connector.insert_user(user_data)
        return jsonify(user)
    except Exception as e:
        print(e)
        return jsonify({'error': 'Internal server error'}), 500


if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=3050)
