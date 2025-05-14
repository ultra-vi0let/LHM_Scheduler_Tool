# from flask import Flask, render_template, request, redirect, url_for
# import json
# from datetime import datetime
#
# app = Flask(__name__)
#
# # Sample data
# data = {
#     "DJ1": {"index": 1, "performance_dates": ["2025-05-01", "2025-07-15"]},
#     "DJ2": {"index": 2, "performance_dates": ["2025-05-10"]},
#     "DJ3": {"index": 3, "performance_dates": []}
# }
#
# # Get priority color based on performance dates
# def get_priority_color(dj_data):
#     if not dj_data["performance_dates"]:
#         return "blue"
#
#     most_recent = max(dj_data["performance_dates"], key=lambda d: datetime.strptime(d, "%Y-%m-%d"))
#     diff = (datetime.now() - datetime.strptime(most_recent, "%Y-%m-%d")).days
#
#     # Red: Scheduled within ±14 days of most future date
#     # Yellow: 15–45 days from future-most date
#     # Green: 46–90 days from future-most date
#     # Blue: Over 90 days or no data at all
#     if diff <= 14:
#         return "red"
#     elif diff <= 45:
#         return "yellow"
#     elif diff <= 90:
#         return "green"
#     else:
#         return "blue"
#
# # Add function to Jinja globals
# app.jinja_env.globals['get_priority_color'] = get_priority_color
#
# @app.route('/')
# def index():
#     performances = {}
#     for dj, dj_data in data.items():
#         for date in dj_data["performance_dates"]:
#             if date not in performances:
#                 performances[date] = []
#             performances[date].append(dj)
#
#     # Pass the function to the template
#     return render_template('index.html', data=data, performances=performances, get_priority_color=get_priority_color)
#
# @app.route('/add_dj', methods=['GET', 'POST'])
# def add_dj():
#     if request.method == 'POST':
#         dj_name = request.form['dj_name']
#         if dj_name in data:
#             return "DJ already exists"
#         index = max([dj_data['index'] for dj_data in data.values()], default=0) + 1
#         data[dj_name] = {"index": index, "performance_dates": []}
#         return redirect(url_for('index'))
#     return render_template('add_dj.html')
#
# @app.route('/add_performance', methods=['GET', 'POST'])
# def add_performance():
#     if request.method == 'POST':
#         date = request.form['date']
#         lineup = request.form['lineup'].split(',')
#         for dj in lineup:
#             if dj in data:
#                 data[dj]["performance_dates"].append(date)
#         return redirect(url_for('index'))
#     return render_template('add_performance.html', data=data)
#
# @app.route('/edit_performance/<date>', methods=['GET', 'POST'])
# def edit_performance(date):
#     if request.method == 'POST':
#         action = request.form['action']
#         if action == 'update':
#             lineup = request.form['lineup'].split(',')
#             for dj in data:
#                 if dj in lineup:
#                     if date not in data[dj]["performance_dates"]:
#                         data[dj]["performance_dates"].append(date)
#                 else:
#                     if date in data[dj]["performance_dates"]:
#                         data[dj]["performance_dates"].remove(date)
#         elif action == 'delete':
#             for dj in data:
#                 if date in data[dj]["performance_dates"]:
#                     data[dj]["performance_dates"].remove(date)
#         return redirect(url_for('index'))
#     current_lineup = [dj for dj, dj_data in data.items() if date in dj_data["performance_dates"]]
#     return render_template('edit_performance.html', data=data, date=date, current_lineup=current_lineup)
#
# @app.route('/edit_dj/<dj_name>', methods=['GET', 'POST'])
# def edit_dj(dj_name):
#     if request.method == 'POST':
#         new_dj_name = request.form['dj_name']
#         if new_dj_name != dj_name:
#             if new_dj_name in data:
#                 return "DJ with this name already exists"
#             data[new_dj_name] = data.pop(dj_name)
#             dj_name = new_dj_name
#
#         performance_dates = request.form['performance_dates'].split(', ')
#         data[dj_name]["performance_dates"] = performance_dates
#         return redirect(url_for('index'))
#
#     dj_data = data[dj_name]
#     return render_template('edit_dj.html', dj_name=dj_name, dj_data=dj_data)
#
# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
import json
import datetime

app = Flask(__name__)

# Path to your JSON data file
DATA_FILE = 'data.json'

# Function to load data from the JSON file
def load_data():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Function to save data to the JSON file
def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Function to get priority color based on performance dates
def get_priority_color(dj_data):
    if not dj_data['performance_dates']:
        return 'blue'

    most_recent_date = max(dj_data['performance_dates'])
    most_recent_date = datetime.datetime.strptime(most_recent_date, '%Y-%m-%d')

    # Calculate time difference from the most recent performance date
    today = datetime.datetime.today()
    delta_days = (most_recent_date - today).days

    if delta_days <= 14 and delta_days >= -14:
        return 'red'
    elif 15 <= delta_days <= 45:
        return 'yellow'
    elif 46 <= delta_days <= 90:
        return 'green'
    else:
        return 'blue'

# Add function to Jinja globals
app.jinja_env.globals['get_priority_color'] = get_priority_color

# Home page showing DJ schedule
@app.route('/')
def index():
    data = load_data()
    performances = {}  # Initialize performances as a dictionary

    for dj, dj_data in data.items():
        for date in dj_data['performance_dates']:
            if date not in performances:
                performances[date] = []
            performances[date].append(dj)

    return render_template('index.html', data=data, performances=performances)

# Add performance page
# @app.route('/add_performance', methods=['GET', 'POST'])
# def add_performance():
#     data = load_data()
#
#     if request.method == 'POST':
#         performance_date = request.form['performance_date']
#         selected_djs = request.form.getlist('djs')
#
#         # Add the selected DJs to their performance_dates
#         for dj in selected_djs:
#             if dj in data:
#                 if performance_date not in data[dj]['performance_dates']:
#                     data[dj]['performance_dates'].append(performance_date)
#
#         save_data(data)  # Save data back to the JSON file
#         return redirect(url_for('index'))  # Redirect to home page
#
#     # Get DJ names for the dropdown list
#     dj_names = list(data.keys())
#     return render_template('add_performance.html', data=data, dj_names=dj_names)
@app.route('/add_performance', methods=['GET', 'POST'])
def add_performance():
    def load_data():
        with open('data.json', 'r') as f:
            return json.load(f)

    def save_data(data):
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)

    data = load_data()

    if request.method == 'POST':
        print("=== FORM SUBMITTED ===")
        for key, value in request.form.items():
            print(f"{key} => {value}")
        print("======================")

        try:
            performance_date = request.form['performance_date']
            # selected_djs = request.form.getlist('djs')  # Make sure the form uses `name="djs"`
            # selected_djs = request.form['lineup'].split(',')  # Convert the comma-separated string to a list
            lineup_raw = request.form.get('lineup')
            if not lineup_raw:
                return "Error: No DJs selected. Please double-click to add DJs to the lineup.", 400

            selected_djs = lineup_raw.split(',')

            for dj in selected_djs:
                if dj in data:
                    if performance_date not in data[dj]['performance_dates']:
                        data[dj]['performance_dates'].append(performance_date)
                        data[dj]['performance_dates'].sort()
                else:
                    data[dj] = {
                        'index': len(data),
                        'performance_dates': [performance_date]
                    }

            save_data(data)
            return redirect(url_for('index'))

        except KeyError as e:
            return f"Error: Missing key {str(e)} in form submission", 400

    # For GET request — show form
    dj_names = list(data.keys())
    return render_template('add_performance.html', dj_names=dj_names, get_priority_color=get_priority_color, data=data)


# Add DJ page
@app.route('/add_dj', methods=['GET', 'POST'])
def add_dj():
    data = load_data()

    if request.method == 'POST':
        dj_name = request.form['dj_name']

        if dj_name not in data:
            dj_index = max([dj_data['index'] for dj_data in data.values()], default=0) + 1
            data[dj_name] = {
                'index': dj_index,
                'performance_dates': []
            }
            save_data(data)  # Save the updated data to the JSON file
            return redirect(url_for('index'))  # Redirect to home page
        else:
            return "DJ already exists!"

    return render_template('add_dj.html')

# Edit DJ page
@app.route('/edit_dj/<string:dj_name>', methods=['GET', 'POST'])
def edit_dj(dj_name):
    data = load_data()

    if dj_name not in data:
        return "DJ not found."

    if request.method == 'POST':
        new_name = request.form['dj_name']
        if new_name != dj_name:
            data[new_name] = data.pop(dj_name)
        data[new_name]['performance_dates'] = request.form.getlist('performance_dates')
        save_data(data)
        return redirect(url_for('index'))

    # Render DJ edit page with current data
    dj_data = data[dj_name]
    return render_template('edit_dj.html', dj_name=dj_name, dj_data=dj_data)

# Edit performance page
@app.route('/edit_performance/<string:performance_date>', methods=['GET', 'POST'])
def edit_performance(performance_date):
    data = load_data()
    if request.method == 'POST':
        updated_djs = request.form.getlist('djs')
        # Update performance dates
        for dj in data:
            if performance_date in data[dj]['performance_dates']:
                if dj not in updated_djs:
                    data[dj]['performance_dates'].remove(performance_date)
            else:
                if dj in updated_djs:
                    data[dj]['performance_dates'].append(performance_date)
        save_data(data)
        return redirect(url_for('index'))

    # Get DJ names for the dropdown list
    dj_names = list(data.keys())
    return render_template('edit_performance.html', performance_date=performance_date, dj_names=dj_names)

if __name__ == '__main__':
    app.run(debug=True)
