from flask import Flask, jsonify, request
import re

app = Flask(__name__)

last_reversed_string = None

# A global error handler to catch unexpected exceptions.
@app.errorhandler(Exception)
def handle_unexpected_error(e):
    app.logger.error('An unexpected error occurred: %s', e)
    return jsonify({"error": "An internal server error occurred."}), 500

@app.route("/reverse", methods=["GET"])
def reverse_string():
    global last_reversed_string
    input_str = request.args.get("in")

    if input_str is None:
        return jsonify({"error": "Missing 'in' query parameter"}), 400

    if not input_str:
        return jsonify({"error": "Input string cannot be empty"}), 400

    words = re.findall(r'\S+', input_str)
    reversed_words = reversed(words)
    result_str = " ".join(reversed_words)

    last_reversed_string = result_str
    return jsonify({"result": result_str})

@app.route("/restore", methods=["GET"])
def restore_string():
    global last_reversed_string
    if last_reversed_string is None:
        return jsonify({"error": "No previous result available"}), 404
    else:
        return jsonify({"result": last_reversed_string}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)