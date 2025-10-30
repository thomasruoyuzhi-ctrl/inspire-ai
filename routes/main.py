from flask import Blueprint, request, jsonify, render_template
from core.generator import generate_content

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('index.html')

@main_bp.route('/generate', methods=['POST'])
def generate():
    theme = request.json.get('theme', '励志')
    data = generate_content(theme)
    return jsonify(data)
