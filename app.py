from uuid import uuid4

from flask import (
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

@app.route('/lists', methods=['GET', 'POST'])
def get_lists():
    
    current_method = request.method

    if current_method == 'GET':
        return render_template('lists.html', lists=session['lists'])
    else:
        title = request.form.get('list_title')
        session['lists'].append({
            'uuid': str(uuid4()),
            'title': title,
            'todos': [],
        })

        session.modified = True
        return redirect(url_for('get_lists'))

@app.route("/lists/new")
def add_new_list():
    return render_template('new_list.html')

if __name__ == "__main__":
    app.run(debug=True, port=5003)