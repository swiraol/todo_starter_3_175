from uuid import uuid4
from functools import wraps

from flask import (
    flash,
    Flask, 
    redirect,
    render_template,  
    request,
    session, 
    url_for,
)
from todos.utils import complete_all_todos, error_for_list_title, delete_todo_by_id, error_for_todo_title, find_list_by_id, find_todo_by_id, is_list_completed, is_todo_completed, sort_items, todos_remaining
from werkzeug.exceptions import NotFound

app = Flask(__name__)

app.secret_key='secret1'

def require_list(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        list_id = kwargs.get('list_id')
        lst = find_list_by_id(list_id, session['lists'])
        if not lst: 
            raise NotFound(description="List not found")
        return f(lst=lst, *args, **kwargs)
    
    return decorated_function

def require_todo(f):
    @wraps(f)
    @require_list
    def decorated_function(lst, *args, **kwargs):
        todo_id = kwargs.get('todo_id')
        todo = find_todo_by_id(todo_id, lst['todos'])
        if not todo:
            raise NotFound(description="Todo not found")
        return f(lst=lst, todo=todo, *args, **kwargs)
    return decorated_function

@app.before_request
def initialize_session():
    if 'lists' not in session:
        session['lists'] = []

@app.route("/")
def index():
    return redirect(url_for('get_lists'))

@app.route('/lists')
def get_lists():
    lists = sort_items(session['lists'], is_list_completed)
    return render_template('lists.html', lists=lists, todos_remaining=todos_remaining, is_list_completed=is_list_completed)

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
@require_list
def show_list(lst, list_id):
    lst['todos'] = sort_items(lst['todos'], is_todo_completed)
    return render_template('list.html', lst=lst, is_list_completed=is_list_completed)

@app.route("/lists/<list_id>", methods=["POST"])
@require_list
def update_list(lst, list_id):    
    title_from_form = request.form['list_title'].strip()
    error = error_for_list_title(title_from_form, session['lists'])
    if error:
        flash(error, "error")
        return render_template("edit_list.html", lst=lst, title=title_from_form)
    
    lst['title'] = title_from_form
    flash("List title has been updated.", "success")
    session.modified = True
    return redirect(url_for('show_list', list_id=list_id))

@app.route("/lists/<list_id>/delete", methods=["POST"])
@require_list
def delete_list(lst, list_id):    
    session['lists'] = [lst for lst in session['lists'] if list_id != lst['id']]
    flash("The list has been deleted", "success")
    session.modified = True
    return redirect(url_for('get_lists'))

@app.route("/lists/<list_id>/todos", methods=["POST"])
@require_list
def add_todo(list_id):
    todo_title = request.form.get('todo').strip()
    
    error = error_for_todo_title(todo_title)
    if error:
        flash(error, "error")
        return render_template("list.html", lst=lst)
    
    lst['todos'].append({
        'title': todo_title,
        'id': str(uuid4()),
        'completed': False
    })
    session.modified = True
    flash("The todo was successfully added.", "success")
    return redirect(url_for("show_list", list_id=list_id))

@app.route('/lists/<list_id>/todos/<todo_id>/toggle', methods=["POST"])
@require_todo
def update_todo_status(lst, todo, list_id, todo_id):
        todo['completed'] = (request.form['completed'] == 'True')
        session.modified = True
        flash("The todo is completed", "success")
        return redirect(url_for('show_list', list_id=list_id))
    
@app.route("/lists/<list_id>/todos/<todo_id>/delete", methods=["POST"])
@require_todo
def delete_todo(lst, todo, list_id, todo_id):
    delete_todo_by_id(todo_id, lst)
    session.modified = True
    flash("Todo was successfully removed", "success")
    return redirect(url_for("show_list", list_id=list_id))

@app.route("/lists/<list_id>/complete_all", methods=["POST"])
@require_todo
def mark_all_todos(lst, list_id):    
    complete_all_todos(lst['todos'])
    session.modified = True
    flash("All todos are completed.", "success")
    return redirect(url_for("show_list", list_id=list_id))

@app.route("/lists/<list_id>/edit")
@require_list 
def edit_list(lst, list_id):
    return render_template("edit_list.html", lst=lst)
    
if __name__ == "__main__":
    app.run(debug=True, port=5003)

