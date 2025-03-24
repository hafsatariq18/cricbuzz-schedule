from flask import Flask, render_template, request, jsonify
import requests
import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)


@app.route('/')
def index():
    # return "Hello"
    return render_template('index.html')


@app.route('/search_team', methods=['POST'])
def search_team():
    team_id = request.form.get('team_id')
    if not team_id:
        return jsonify({'error': 'Team ID is required'}), 400

    url = f"https://cricbuzz-cricket.p.rapidapi.com/teams/v1/{team_id}/schedule"
    headers = {
        "x-rapidapi-key": os.getenv('RAPIDAPI_KEY'),
        "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        matches = response.json()
        # print(matches)
        return render_template('results.html', matches=matches)
    else:
        return jsonify({'error': 'Failed to fetch data'}), response.status_code


@app.template_filter('dateformat')
def dateformat(value):
    return datetime.datetime.fromtimestamp(int(value)/1000).strftime('%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)