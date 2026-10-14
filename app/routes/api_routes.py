import os
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for, flash, current_app
from app.models import db
from app.models.user import User
from app.services.ocr_engine import ocr_service
from app.services.nlp_engine import nlp_detector

api_bp = Blueprint('api', __name__)

@api_bp.route('/ocr-scan', methods=['POST'])
def ocr_scan():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    if 'image_file' not in request.files:
        return jsonify({"status": "error", "message": "No image file provided."}), 400

    file = request.files['image_file']
    filename = secure_filename(file.filename or 'scanned_doc.png')
    save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'ocr', filename)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    file.save(save_path)

    extracted_text = ocr_service.extract_text_from_image(save_path)
    analysis = nlp_detector.analyze_document(extracted_text)

    return jsonify({
        "status": "success",
        "extracted_text": extracted_text,
        "analysis": analysis
    })

@api_bp.route('/voice-dictation-analyze', methods=['POST'])
def voice_dictation_analyze():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    data = request.json or {}
    transcript = data.get('transcript', '')
    if not transcript:
        return jsonify({"status": "error", "message": "No voice transcript received."}), 400

    analysis = nlp_detector.analyze_document(transcript)
    return jsonify({
        "status": "success",
        "analysis": analysis
    })

@api_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    user = User.query.get(user_id)

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')

        if full_name:
            user.full_name = full_name

        if current_password and new_password:
            if user.check_password(current_password):
                user.set_password(new_password)
                flash('Password updated successfully.', 'success')
            else:
                flash('Incorrect current password.', 'danger')

        db.session.commit()
        session['user_name'] = user.full_name
        flash('Profile settings saved successfully.', 'success')
        return redirect(url_for('api.settings'))

    return render_template('profile/settings.html', user=user)
