from flask import Flask, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.executors.pool import ThreadPoolExecutor

# Redefine jinja template syntax
class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',  # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
        variable_end_string='%%',
    ))


# Create the app
app = CustomFlask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weiss.db'
db = SQLAlchemy(app)

# Add static include endpoint
@app.route('/view-static')
def view_static():
    return send_from_directory(app.root_path + '/views/', request.args.get('filename'))

# Import models
import models.solved
import models.unsolved
db.create_all()

# Attach the blueprints
from routes.main import main
app.register_blueprint(main)

# Set up scheduled jobs
from services.main import scrape_unsolved_problems, scrape_solved_problems
scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=scrape_unsolved_problems,
    trigger=IntervalTrigger(minutes=1),
    id='scrape_unsolved_problems',
    replace_existing=True
)
scheduler.add_job(
    func=scrape_solved_problems,
    trigger=IntervalTrigger(minutes=1),
    id='scrape_solved_problems',
    replace_existing=True
)
