from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

KANBOARD_API_KEY = 'your_kanboard_api_key'
KANBOARD_API_URL = 'your_kanboard_api_url'

def create_task(project_id, title, description):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "createTask",
        "params": {
            "title": title,
            "project_id": project_id,
            "description": description,
            "api_key": KANBOARD_API_KEY
        }
    }

    response = requests.post(KANBOARD_API_URL, json=payload)
    return response.json()

@app.route('/slack/kanboard', methods=['POST'])
def slack_command():
    try:
        text = request.form['text'].split()
        project_id = text[0]
        title = text[1]
        description = " ".join(text[2:]) if len(text) > 2 else ""

        response = create_task(project_id, title, description)
        if 'result' in response:
            return jsonify({
                'response_type': 'in_channel',
                'text': f'Task "{title}" added to project {project_id}.'
            })
        else:
            return jsonify({
                'response_type': 'ephemeral',
                'text': 'Error adding task. Please check your input and try again.'
            })

    except Exception as e:
        return jsonify({
            'response_type': 'ephemeral',
            'text': f'Error processing command: {e}'
        })

if __name__ == '__main__':
    app.run(port=5000)
