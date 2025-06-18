from flask import Flask, jsonify, request, render_template
import subprocess

app = Flask(__name__)


def parse_models(output: str):
    lines = output.strip().splitlines()
    models = []
    for line in lines[1:]:
        parts = line.split()
        if parts:
            models.append(parts[0])
    return models


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/models')
def list_models():
    list_result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
    ps_result = subprocess.run(['ollama', 'ps'], capture_output=True, text=True)
    available = parse_models(list_result.stdout)
    running = set(parse_models(ps_result.stdout))
    return jsonify([
        {
            'name': name,
            'running': name in running
        } for name in available
    ])


@app.route('/api/model/<name>/start', methods=['POST'])
def start_model(name):
    subprocess.Popen(['ollama', 'run', name])
    return jsonify({'status': 'started', 'model': name})


@app.route('/api/model/<name>/stop', methods=['POST'])
def stop_model(name):
    subprocess.run(['ollama', 'stop', name])
    return jsonify({'status': 'stopped', 'model': name})


@app.route('/api/run', methods=['POST'])
def run_command():
    command = request.json.get('command')
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return jsonify({
        'stdout': result.stdout,
        'stderr': result.stderr,
        'returncode': result.returncode
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
