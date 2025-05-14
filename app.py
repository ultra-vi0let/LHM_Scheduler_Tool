from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime

app = Flask(__name__)

# Sample data
data = {
    "DJ1": {"index": 1, "performance_dates": ["2025-05-01", "2025-07-15"]},
    "DJ2": {"index": 2, "performance_dates": ["2025-05-10"]},
    "DJ3": {"index": 3, "performance_dates": []}
}

# Get priority color based on performance dates
def get_priority_color(dj_data):
    if not dj_data["performance_dates"]:
        return "blue"

    most_recent = max(dj_data["performance_dates"], key=lambda d: datetime.strptime(d, "%Y-%m-%d"))
    diff = (datetime.now() - datetime.strptime(most_recent, "%Y-%m-%d")).days

    # Red: Scheduled within ±14 days of most future date
    # Yellow: 15–45 days from future-most date
    # Green: 46–90 days from future-most date
    # Blue: Over 90 days or no data at all
    if diff <= 14:
        return "red"
    elif diff <= 45:
        return "yellow"
    elif diff <= 90:
        return "green"
    else:
        return "blue"

# Add function to Jinja globals
app.jinja_env.globals['get_priority_color'] = get_priority_color

@app.route('/')
def index():
    performances = {}
    for dj, dj_data in data.items():
        for date in dj_data["performance_dates"]:
            if date not in performances:
                performances[date] = []
            performances[date].append(dj)

    # Pass the function to the template
    return render_template('index.html', data=data, performances=performances, get_priority_color=get_priority_color)

@app.route('/add_dj', methods=['GET', 'POST'])
def add_dj():
    if request.method == 'POST':
        dj_name = request.form['dj_name']
        if dj_name in data:
            return "DJ already exists"
        index = max([dj_data['index'] for dj_data in data.values()], default=0) + 1
        data[dj_name] = {"index": index, "performance_dates": []}
        return redirect(url_for('index'))
    return render_template('add_dj.html')

@app.route('/add_performance', methods=['GET', 'POST'])
def add_performance():
    if request.method == 'POST':
        date = request.form['date']
        lineup = request.form['lineup'].split(',')
        for dj in lineup:
            if dj in data:
                data[dj]["performance_dates"].append(date)
        return redirect(url_for('index'))
    return render_template('add_performance.html', data=data)

@app.route('/edit_performance/<date>', methods=['GET', 'POST'])
def edit_performance(date):
    if request.method == 'POST':
        action = request.form['action']
        if action == 'update':
            lineup = request.form['lineup'].split(',')
            for dj in data:
                if dj in lineup:
                    if date not in data[dj]["performance_dates"]:
                        data[dj]["performance_dates"].append(date)
                else:
                    if date in data[dj]["performance_dates"]:
                        data[dj]["performance_dates"].remove(date)
        elif action == 'delete':
            for dj in data:
                if date in data[dj]["performance_dates"]:
                    data[dj]["performance_dates"].remove(date)
        return redirect(url_for('index'))
    current_lineup = [dj for dj, dj_data in data.items() if date in dj_data["performance_dates"]]
    return render_template('edit_performance.html', data=data, date=date, current_lineup=current_lineup)

@app.route('/edit_dj/<dj_name>', methods=['GET', 'POST'])
def edit_dj(dj_name):
    if request.method == 'POST':
        new_dj_name = request.form['dj_name']
        if new_dj_name != dj_name:
            if new_dj_name in data:
                return "DJ with this name already exists"
            data[new_dj_name] = data.pop(dj_name)
            dj_name = new_dj_name

        performance_dates = request.form['performance_dates'].split(', ')
        data[dj_name]["performance_dates"] = performance_dates
        return redirect(url_for('index'))

    dj_data = data[dj_name]
    return render_template('edit_dj.html', dj_name=dj_name, dj_data=dj_data)

if __name__ == '__main__':
    app.run(debug=True)
