from flask import Blueprint, render_template, request, jsonify, Response
from textblob import TextBlob
from models.unsolved import Unsolved
from models.solved import Solved
from operator import itemgetter

main = Blueprint('main', __name__, template_folder='../views')


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/api/get-topics', methods=['POST', 'GET'])
def get_topics():
    return jsonify(['mathematics', 'computer science']), 200


@main.route('/api/get-unsolved-problems', methods=['POST', 'GET'])
def get_unsolved_problems():
    problems = {}
    problems['mathematics'] = []
    problems['computer science'] = []
    query = Unsolved.query.all()
    for q in query:
        problem = {
            'title': q.title,
            'link': q.link,
            'solvability': q.solvability,
            'sources': []
        }
        i = 0
        for s in q.sourceTitles:
            problem['sources'].append({'title': s, 'link': q.sourceLinks[i]})
            i += 1
        problems[q.topic].append(problem)
    for topic in problems.keys():
        row = problems[topic]
        problems[topic] = sorted(row, key=itemgetter('solvability'))
    return jsonify(problems), 200


@main.route('/api/get-solved-problems', methods=['POST'])
def get_solved_problems():
    problems = {}
    problems['mathematics'] = []
    problems['computer science'] = []
    query = Solved.query.all()
    for q in query:
        problem = {
            'title': q.title,
            'link': q.link,
            'solvedBy': q.solvedBy,
            'sources': []
        }
        i = 0
        for s in q.sourceTitles:
            problem['sources'].append({'title': s, 'link': q.sourceLinks[i]})
            i += 1
        problems[q.topic].append(problem)
    return jsonify(problems), 200