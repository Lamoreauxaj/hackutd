from googlesearch import search
from urllib.request import urlopen
from bs4 import BeautifulSoup
from textblob import TextBlob
from models.unsolved import Unsolved
from models.solved import Solved
import app


def grab_sources_problem(problem, amt=25):
    resp = search(problem, tld='com', num=amt, pause=2, stop=1)
    links = []
    for link in resp:
        try:
            content = BeautifulSoup(urlopen(link).read(), 'lxml')
        except:
            pass
        if content.title is None:
            continue
        links.append({'title': str(content.title.string).strip(), 'link': link})
    return links


def calculate_solvability_and_sources(sources):
    solvability = 0
    source_titles = []
    source_links = []
    used = 0
    for source in sources:
        try:
            resp = BeautifulSoup(urlopen(source['link']).read(), 'lxml')
            text = ' '.join(str(resp.p.contents) for r in resp.p.contents)
            blob = TextBlob(text)
            solvability += blob.sentiment.polarity * (1 - blob.subjectivity)
            if blob.subjectivity < .5 and len(source_titles) < 3:
                source_titles.append(source['title'])
                source_links.append(source['link'])
            used += 1
        except:
            pass
    solvability /= used
    return source_titles, source_links, (solvability + 1) / 2


def scrape_unsolved_problems_topic(topic):
    problems_names = []
    if topic == 'mathematics':
        problems_names = [
            {'title': 'P versus NP', 'link': 'https://en.wikipedia.org/wiki/P_versus_NP_problem'},
            {'title': 'Hodge conjecture', 'link': 'https://en.wikipedia.org/wiki/Hodge_conjecture'},
            {'title': 'Riemann hypothesis', 'link': 'https://en.wikipedia.org/wiki/Riemann_hypothesis'},
            {'title': 'Yang-Mills existence and mass gap', 'link': 'https://en.wikipedia.org/wiki/Yang%E2%80%93Mills_existence_and_mass_gap'},
            {'title': 'Navier-Stokes existence and smoothness', 'link': 'https://en.wikipedia.org/wiki/Navier%E2%80%93Stokes_existence_and_smoothness'},
            {'title': 'Birch and Swinnerton-Dyer conjecture', 'link': 'https://en.wikipedia.org/wiki/Birch_and_Swinnerton-Dyer_conjecture'}
        ]
    if topic == 'computer science':
        problems_names = [
            {'title': 'P versus NP problem', 'link': 'https://en.wikipedia.org/wiki/P_versus_NP_problem'},
            {'title': 'Collatz Conjecture', 'link': 'https://en.wikipedia.org/wiki/Collatz_conjecture'},
            {'title': 'Polynomial Discrete Logarithm', 'link': 'https://en.wikipedia.org/wiki/Discrete_logarithm'}
        ]
    for problem in problems_names:
        title = problem['title']
        link = problem['link']
        sources = grab_sources_problem(title, 15)
        source_titles, source_links, solvability = calculate_solvability_and_sources(sources)
        unsolved = Unsolved(title=title, link=link, sourceTitles=source_titles, sourceLinks=source_links, solvability=solvability, topic=topic)
        q = Unsolved.query.filter_by(title=title).first()
        if q:
            app.db.session.delete(q)
            app.db.session.commit()
        app.db.session.add(unsolved)
        app.db.session.commit()


def scrape_solved_problems_topic(topic):
    problems_names = []
    if topic == 'mathematics':
        problems_names = [
            {'title': 'Poincare Conjecture', 'link': 'https://en.wikipedia.org/wiki/Poincar%C3%A9_conjecture', 'solvedBy': 'Grigori Perelman'},
            {'title': 'Fermat\'s Last Theorem', 'link': 'https://en.wikipedia.org/wiki/Fermat%27s_Last_Theorem', 'solvedBy': 'Andrew Wiles'}
        ]
    if topic == 'computer science':
        problems_names = [
        ]
    for problem in problems_names:
        title = problem['title']
        link = problem['link']
        solvedBy = problem['solvedBy']
        sources = grab_sources_problem(title, 15)
        source_titles, source_links, solvability = calculate_solvability_and_sources(sources)
        solved = Solved(title=title, link=link, sourceTitles=source_titles, sourceLinks=source_links, topic=topic, solvedBy=solvedBy)
        q = Solved.query.filter_by(title=title).first()
        if q:
            app.db.session.delete(q)
            app.db.session.commit()
        app.db.session.add(solved)
        app.db.session.commit()


def scrape_unsolved_problems():
    scrape_unsolved_problems_topic('mathematics')
    scrape_unsolved_problems_topic('computer science')


def scrape_solved_problems():
    scrape_solved_problems_topic('mathematics')
    scrape_solved_problems_topic('computer science')