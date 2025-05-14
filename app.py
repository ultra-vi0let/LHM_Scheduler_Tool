from flask import Flask, render_template

app = Flask(__name__)

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')  # We'll create this file later

if __name__ == '__main__':
    app.run(debug=True)
