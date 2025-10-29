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
    if any(title == lst['title'] for lst in session['lists']):
        flash('The title must be unique.', 'error')
        return redirect(url_for('add_todo_list'))
    
    if 1 <= len(title) <= 100:
        session['lists'].append({
            'id': str(uuid4()),
            'title': title,
            'todos': [],
        })
        session.modified = True

        flash('List was successfully added', 'success')

        return redirect(url_for('get_lists'))
    
    flash('The title must be between 1 and 100 characters.', 'error')
    return redirect(url_for('add_todo_list'))

@app.route("/lists/new")
def add_todo_list():
    return render_template('new_list.html')

if __name__ == "__main__":
    app.run(debug=True, port=5003)

