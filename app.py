from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return redirect(url_for('get_lists'))

@app.route('/lists', methods=['GET', 'POST'])
def get_lists():
    lists = [
        {'title': 'Lunch Groceries', 'todos': []},
        {'title': 'Dinner Groceries', 'todos': []},
    ]
    return render_template('lists.html', lists=lists)

@app.route("/lists/new")
def add_new_list():
    return render_template('new_list.html')

if __name__ == "__main__":
    app.run(debug=True, port=5003)