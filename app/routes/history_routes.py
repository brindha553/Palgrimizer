import os
from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify, send_file, current_app
from app.models import db
from app.models.document import Document
from app.services.doc_exporter import doc_exporter

history_bp = Blueprint('history', __name__, url_prefix='/documents')

@history_bp.route('/')
def index():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    query_str = request.args.get('q', '').strip()
    file_type = request.args.get('type', '').strip()
    sort_by = request.args.get('sort', 'newest')

    query = Document.query.filter_by(user_id=user_id, is_deleted=False)

    if query_str:
        query = query.filter((Document.title.ilike(f"%{query_str}%")) | (Document.original_text.ilike(f"%{query_str}%")))

    if file_type:
        query = query.filter_by(file_type=file_type)

    if sort_by == 'oldest':
        query = query.order_by(Document.created_at.asc())
    elif sort_by == 'title':
        query = query.order_by(Document.title.asc())
    else:
        query = query.order_by(Document.created_at.desc())

    documents = query.all()

    return render_template(
        'history/index.html',
        documents=documents,
        query_str=query_str,
        file_type=file_type,
        sort_by=sort_by
    )

@history_bp.route('/<int:doc_id>/export/<format_type>')
def export_doc(doc_id, format_type):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    doc = Document.query.filter_by(id=doc_id, user_id=user_id).first_or_404()
    
    filename_clean = doc.title.rsplit('.', 1)[0]
    export_filename = f"{filename_clean}_corrected.{format_type}"
    export_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'exports')
    os.makedirs(export_dir, exist_ok=True)
    export_path = os.path.join(export_dir, export_filename)

    text_to_export = doc.corrected_text or doc.original_text
    doc_exporter.export_document(doc.title, text_to_export, format_type, export_path)

    return send_file(export_path, as_attachment=True, download_name=export_filename)

@history_bp.route('/<int:doc_id>/delete', methods=['POST'])
def delete_doc(doc_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    doc = Document.query.filter_by(id=doc_id, user_id=user_id).first_or_404()
    doc.is_deleted = True
    db.session.commit()

    flash(f'Document "{doc.title}" moved to trash.', 'info')
    return redirect(url_for('history.index'))

@history_bp.route('/<int:doc_id>/restore', methods=['POST'])
def restore_doc(doc_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    doc = Document.query.filter_by(id=doc_id, user_id=user_id).first_or_404()
    doc.is_deleted = False
    db.session.commit()

    flash(f'Document "{doc.title}" restored successfully.', 'success')
    return redirect(url_for('history.index'))
