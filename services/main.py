from googlesearch.googlesearch import GoogleSearch

def get_unsolved_problems(topic):
    if topic == 'mathematics':
        return [{'title': 'P versus NP', 'link': 'https://en.wikipedia.org/wiki/P_versus_NP_problem'},
                {'title': 'Hodge conjecture', 'link': 'https://en.wikipedia.org/wiki/Hodge_conjecture'}]
    else:
        return None


def calculate_solvability(problem):
    pass


def grab_articles(problem):
    resp = GoogleSearch().search(problem)
    for result in resp:
        print(result.title, result.getText())


if __name__ == '__main__':
    print(grab_articles('P versus NP'))