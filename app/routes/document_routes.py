import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, current_app
from app.models import db
from app.models.user import UserActivity
from app.models.document import Document, AnalysisReport, DocumentCorrection, DocumentVersion
from app.services.nlp_engine import nlp_detector
from app.services.doc_parser import doc_parser

document_bp = Blueprint('document', __name__)

@document_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        # Handle file upload or pasted text
        pasted_text = request.form.get('pasted_text', '').strip()
        file = request.files.get('document_file')

        text_content = ""
        filename = "Untitled Document.txt"
        file_type = "txt"
        file_size = 0

        if file and file.filename:
            filename = secure_filename(file.filename)
            file_type = filename.rsplit('.', 1)[-1].lower() if '.' in filename else 'txt'
            save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(save_path)
            file_size = os.path.getsize(save_path)
            
            # Extract text
            text_content = doc_parser.extract_text(save_path, file_type)
        elif pasted_text:
            text_content = pasted_text
            filename = f"Pasted_Text_{len(pasted_text)}.txt"
            file_size = len(pasted_text)
        else:
            flash('Please select a document file or paste document text.', 'warning')
            return render_template('document/upload.html')

        # Run AI NLP Error Analysis
        analysis = nlp_detector.analyze_document(text_content)

        # Create Document DB Record
        doc = Document(
            user_id=user_id,
            title=filename,
            original_filename=filename,
            file_type=file_type,
            file_size=file_size,
            original_text=text_content,
            corrected_text=analysis["corrected_text"],
            language="en"
        )
        db.session.add(doc)
        db.session.flush()

        # Create Analysis Report DB Record
        report = AnalysisReport(
            document_id=doc.id,
            overall_score=analysis["scores"]["overall_score"],
            grammar_score=analysis["scores"]["grammar_score"],
            spelling_score=analysis["scores"]["spelling_score"],
            formatting_score=analysis["scores"]["formatting_score"],
            readability_score=analysis["scores"]["readability_score"],
            professional_score=analysis["scores"]["professional_score"],
            alignment_score=analysis["scores"]["alignment_score"],
            typography_score=analysis["scores"]["typography_score"],
            word_count=analysis["statistics"]["word_count"],
            character_count=analysis["statistics"]["character_count"],
            sentence_count=analysis["statistics"]["sentence_count"],
            paragraph_count=analysis["statistics"]["paragraph_count"],
            page_count=analysis["statistics"]["page_count"],
            estimated_reading_time=analysis["statistics"]["estimated_reading_time"]
        )
        report.set_issue_counts(analysis["issue_counts"])
        db.session.add(report)

        # Create individual corrections
        for c in analysis["corrections"]:
            corr = DocumentCorrection(
                document_id=doc.id,
                category=c["category"],
                severity=c["severity"],
                original_segment=c["original_segment"],
                suggested_segment=c["suggested_segment"],
                explanation=c["explanation"],
                start_index=c["start_index"],
                end_index=c["end_index"]
            )
            db.session.add(corr)

        # Record activity
        activity = UserActivity(user_id=user_id, action=f"Uploaded {filename}", details=f"Score: {report.overall_score}%")
        db.session.add(activity)

        db.session.commit()

        flash('Document uploaded and analyzed successfully!', 'success')
        return redirect(url_for('document.studio', doc_id=doc.id))

    return render_template('document/upload.html')

@document_bp.route('/document/<int:doc_id>')
def studio(doc_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    doc = Document.query.filter_by(id=doc_id, user_id=user_id, is_deleted=False).first_or_404()
    report = doc.report
    corrections = DocumentCorrection.query.filter_by(document_id=doc.id).all()

    return render_template(
        'document/studio.html',
        doc=doc,
        report=report,
        corrections=corrections
    )

@document_bp.route('/api/document/<int:doc_id>/accept-correction', methods=['POST'])
def accept_correction(doc_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    data = request.json or {}
    correction_id = data.get('correction_id')
    
    corr = DocumentCorrection.query.filter_by(id=correction_id, document_id=doc_id).first()
    if not corr:
        return jsonify({"status": "error", "message": "Correction not found"}), 404

    corr.status = 'accepted'
    db.session.commit()

    # Recalculate document health score
    doc = Document.query.get(doc_id)
    pending_count = DocumentCorrection.query.filter_by(document_id=doc_id, status='pending').count()
    if doc.report:
        doc.report.overall_score = min(100.0, round(doc.report.overall_score + 1.5, 1))
        db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Suggestion accepted.",
        "new_score": doc.report.overall_score if doc.report else 100.0,
        "pending_count": pending_count
    })

@document_bp.route('/api/document/<int:doc_id>/reject-correction', methods=['POST'])
def reject_correction(doc_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    data = request.json or {}
    correction_id = data.get('correction_id')
    
    corr = DocumentCorrection.query.filter_by(id=correction_id, document_id=doc_id).first()
    if not corr:
        return jsonify({"status": "error", "message": "Correction not found"}), 404

    corr.status = 'rejected'
    db.session.commit()

    pending_count = DocumentCorrection.query.filter_by(document_id=doc_id, status='pending').count()

    return jsonify({
        "status": "success",
        "message": "Suggestion rejected.",
        "pending_count": pending_count
    })

@document_bp.route('/api/document/<int:doc_id>/apply-all', methods=['POST'])
def apply_all_corrections(doc_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    DocumentCorrection.query.filter_by(document_id=doc_id, status='pending').update({"status": "accepted"})
    doc = Document.query.get(doc_id)
    if doc.report:
        doc.report.overall_score = 99.8
        doc.report.grammar_score = 99.8
        doc.report.spelling_score = 100.0
        doc.report.formatting_score = 99.5
    
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "All AI corrections applied successfully!",
        "new_score": 99.8
    })

@document_bp.route('/api/document/<int:doc_id>/reanalyze', methods=['POST'])
def reanalyze_document(doc_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    doc = Document.query.get(doc_id)
    data = request.json or {}
    updated_text = data.get('text', doc.original_text)

    # Save current version
    v_count = DocumentVersion.query.filter_by(document_id=doc_id).count()
    version = DocumentVersion(document_id=doc_id, version_number=v_count+1, content=doc.corrected_text or doc.original_text, description="Auto-saved before re-analysis")
    db.session.add(version)

    # Re-run NLP engine
    analysis = nlp_detector.analyze_document(updated_text)
    doc.original_text = updated_text
    doc.corrected_text = analysis["corrected_text"]

    # Update report
    if doc.report:
        doc.report.overall_score = analysis["scores"]["overall_score"]
        doc.report.grammar_score = analysis["scores"]["grammar_score"]
        doc.report.spelling_score = analysis["scores"]["spelling_score"]
        doc.report.formatting_score = analysis["scores"]["formatting_score"]
        doc.report.readability_score = analysis["scores"]["readability_score"]
        doc.report.word_count = analysis["statistics"]["word_count"]
        doc.report.character_count = analysis["statistics"]["character_count"]
        doc.report.sentence_count = analysis["statistics"]["sentence_count"]
        doc.report.set_issue_counts(analysis["issue_counts"])

    # Clear old corrections and populate new
    DocumentCorrection.query.filter_by(document_id=doc_id).delete()
    for c in analysis["corrections"]:
        corr = DocumentCorrection(
            document_id=doc.id,
            category=c["category"],
            severity=c["severity"],
            original_segment=c["original_segment"],
            suggested_segment=c["suggested_segment"],
            explanation=c["explanation"],
            start_index=c["start_index"],
            end_index=c["end_index"]
        )
        db.session.add(corr)

    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Document re-analyzed with fresh score calculation.",
        "analysis": analysis
    })
