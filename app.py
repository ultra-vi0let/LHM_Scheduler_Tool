from flask import Flask, render_template, jsonify
import json
from datetime import datetime

app = Flask(__name__)

# Load DJ data from JSON
def load_data():
    with open('data/dj_data.json') as f:
        return json.load(f)

# Helper function to calculate priority color
def calculate_priority(dj_data):
    today = datetime.today()
    performance_dates = dj_data.get('performance_dates', [])
    if not performance_dates:
        return 'blue'  # No performances yet
    # Sort the performance dates and find the most recent future date
    future_dates = [datetime.strptime(date, '%Y-%m-%d') for date in performance_dates if datetime.strptime(date, '%Y-%m-%d') > today]
    if not future_dates:
        return 'blue'  # No future performances
    future_most = max(future_dates)
    delta = (future_most - today).days
    if delta <= 14:
        return 'red'
    elif 15 <= delta <= 45:
        return 'yellow'
    elif 46 <= delta <= 90:
        return 'green'
    else:
        return 'blue'

@app.route('/')
def index():
    dj_data = load_data()

    # Prepare DJ roster with priority color
    dj_roster = []
    for dj, data in dj_data.items():
        dj_roster.append({
            'name': dj,
            'most_recent': max(data['performance_dates']),
            'priority_color': calculate_priority(data)
        })

    # Prepare performance schedule (simple example)
    performance_schedule = []
    for date in set(date for dj in dj_data.values() for date in dj['performance_dates']):
        performing_djs = [dj for dj, data in dj_data.items() if date in data['performance_dates']]
        performance_schedule.append({'date': date, 'djs': performing_djs})

    return render_template('index.html', performance_schedule=performance_schedule, dj_roster=dj_roster)

if __name__ == '__main__':
    app.run(debug=True)
