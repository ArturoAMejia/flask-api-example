from flask import Flask, render_template, jsonify
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Hello world'})

    