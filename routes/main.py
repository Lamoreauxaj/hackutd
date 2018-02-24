from flask import Blueprint, render_template, request, jsonify, Response
from textblob import TextBlob

main = Blueprint('main', __name__, template_folder='../views')


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/api/unsolved-problems', methods=['POST'])
def unsolved_problems():
    if 'topic' not in request.form.keys():
        return Response('data must contain key topic', 400)
    return "hello, world"
    # return jsonify(request.get_json(force=True))