from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

todos = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date = request.form['date']
        todo = request.form['todo']
        if date in todos:
            todos[date].append(todo)
        else:
            todos[date] = [todo]
        return redirect(url_for('index'))
    return render_template('index.html', todos=todos)

if __name__ == '__main__':
    app.run(debug=True)
