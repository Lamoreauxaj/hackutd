from flask import Flask, send_from_directory, request
from routes.main import main

# Redefine jinja template syntax
class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',  # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
        variable_end_string='%%',
    ))

# Create the app
app = CustomFlask(__name__)

# Add static include endpoint
@app.route('/view-static')
def view_static():
    return send_from_directory(app.root_path + '/views/', request.args.get('filename'))

# Attach the blueprints
app.register_blueprint(main)
