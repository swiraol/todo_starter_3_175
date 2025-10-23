from flask import Flask, render_template, redirect, url_for, session, request

app = Flask(__name__)

app.secret_key='secret1'

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
        session['lists'] = [
            {'title': 'Lunch Groceries', 'todos': ['Buy milk']},
            {'title': 'Dinner Groceries', 'todos': []},
            {'title': title, 'todos': []}
        ]

        session.modified = True
        return redirect(url_for('get_lists'))

@app.route("/lists/new")
def add_new_list():
    return render_template('new_list.html')

if __name__ == "__main__":
    app.run(debug=True, port=5003)