from flask import Blueprint, render_template, request, jsonify
from app.services.nlp_engine import nlp_detector

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('main/index.html')

@main_bp.route('/features')
def features():
    return render_template('main/features.html')

@main_bp.route('/pricing')
def pricing():
    return render_template('main/pricing.html')

@main_bp.route('/about')
def about():
    return render_template('main/about.html')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        data = request.json or {}
        name = data.get('name', 'User')
        return jsonify({"status": "success", "message": f"Thank you, {name}! Your message has been received."})
    return render_template('main/contact.html')

@main_bp.route('/api/demo-analyze', methods=['POST'])
def demo_analyze():
    data = request.json or {}
    text = data.get('text', '')
    if not text.strip():
        text = "Teh pilgrimizer platform helps to recieve and fix grammar, spelling and formatting errors definitionately."
    
    result = nlp_detector.analyze_document(text)
    return jsonify({"status": "success", "result": result})
