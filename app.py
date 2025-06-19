"""Flask application to manage Ollama models."""

import subprocess
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


def parse_models(output: str):
    """Parse `ollama` command output into a list of model names."""

    lines = output.strip().splitlines()
    models = []
    for line in lines[1:]:
        parts = line.split()
        if parts:
            models.append(parts[0])
    return models


@app.route('/')
def index():
    """Render the main page with the list of models."""

    return render_template('index.html')


@app.route('/api/models')
def list_models():
    """Return available and running model information."""

    list_result = subprocess.run(
        ['ollama', 'list'], capture_output=True, text=True, check=False
    )
    ps_result = subprocess.run(
        ['ollama', 'ps'], capture_output=True, text=True, check=False
    )
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
    """Start the given model."""

    # pylint: disable=consider-using-with
    subprocess.Popen(['ollama', 'run', name])
    return jsonify({'status': 'started', 'model': name})


@app.route('/api/model/<name>/stop', methods=['POST'])
def stop_model(name):
    """Stop the given model."""

    subprocess.run(['ollama', 'stop', name], check=False)
    return jsonify({'status': 'stopped', 'model': name})


@app.route('/api/run', methods=['POST'])
def run_command():
    """Run an arbitrary shell command and return its output."""

    command = request.json.get('command')
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True, check=False
    )
    return jsonify({
        'stdout': result.stdout,
        'stderr': result.stderr,
        'returncode': result.returncode
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
