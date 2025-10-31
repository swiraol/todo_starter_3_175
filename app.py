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
from werkzeug.exceptions import NotFound

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
    print("lists: ", session['lists'])
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

@app.route("/lists/<list_id>")
def show_list(list_id):
    lst = next((lst for lst in session['lists'] if list_id == lst['id']), None)
    if not lst:
        raise NotFound(description="List not found")
    return render_template('list.html', lst=lst)

if __name__ == "__main__":
    app.run(debug=True, port=5003)

