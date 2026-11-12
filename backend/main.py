from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "project": "Orkloo",
        "status": "online"
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
