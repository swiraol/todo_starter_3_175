from uuid import uuid4

from flask import (
    flash,
    Flask, 
    redirect,
    render_template,  
    request,
    session, 
    url_for,
)
from todos.utils import error_for_list_title

app = Flask(__name__)

app.secret_key='secret1'

@app.before_request
def initialize_session():
    if 'lists' not in session:
        session['lists'] = []

@app.route("/")
def index():
    return redirect(url_for('get_lists'))

@app.route('/lists')
def get_lists():

    return render_template('lists.html', lists=session['lists'])

@app.route('/lists', methods=["POST"])
def create_list():
    title = request.form.get('list_title').strip()
    error = error_for_list_title(title, session['lists'])
    if error:
        flash(error, 'error')
        session['new_list_title'] = title
        return redirect(url_for('add_todo_list'))

    session['lists'].append({
        'id': str(uuid4()),
        'title': title,
        'todos': [],
    })
    session.modified = True

    flash('List was successfully added', 'success')

    return redirect(url_for('get_lists'))

@app.route("/lists/new")
def add_todo_list():
    title = session.get('new_list_title', "")
    return render_template('new_list.html', title=title)

if __name__ == "__main__":
    app.run(debug=True, port=5003)

