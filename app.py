from flask import Flask, send_from_directory, request, jsonify
import csv
import os

app = Flask(__name__, static_url_path='', static_folder='.')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/tci_test')
def tci_test_page():
    return send_from_directory('.', 'tci_test.html')

@app.route('/submit_test', methods=['POST'])
def submit_test():
    data = request.get_json(force=True)
    user_id = data.get('userId')
    answers = data.get('answers')
    if not user_id or not isinstance(answers, list):
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
    file_exists = os.path.exists('responses.csv')
    with open('responses.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            header = ['userId'] + [f'q{i}' for i in range(1, len(answers)+1)]
            writer.writerow(header)
        writer.writerow([user_id] + answers)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
