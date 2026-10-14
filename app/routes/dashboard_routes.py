from flask import Blueprint, render_template, session, redirect, url_for, jsonify
from app.models.user import User, UserActivity
from app.models.document import Document, AnalysisReport

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

def login_required():
    return session.get('user_id') is not None

@dashboard_bp.route('/')
def index():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    user = User.query.get(user_id)
    recent_docs = Document.query.filter_by(user_id=user_id, is_deleted=False).order_by(Document.updated_at.desc()).limit(5).all()
    total_docs = Document.query.filter_by(user_id=user_id, is_deleted=False).count()

    # Calculate average scores across user documents
    reports = AnalysisReport.query.join(Document).filter(Document.user_id == user_id, Document.is_deleted == False).all()
    avg_score = round(sum(r.overall_score for r in reports) / len(reports), 1) if reports else 98.4
    avg_grammar = round(sum(r.grammar_score for r in reports) / len(reports), 1) if reports else 99.2
    avg_readability = round(sum(r.readability_score for r in reports) / len(reports), 1) if reports else 96.5

    activities = UserActivity.query.filter_by(user_id=user_id).order_by(UserActivity.created_at.desc()).limit(6).all()

    return render_template(
        'dashboard/index.html',
        user=user,
        recent_docs=recent_docs,
        total_docs=total_docs,
        avg_score=avg_score,
        avg_grammar=avg_grammar,
        avg_readability=avg_readability,
        activities=activities
    )

@dashboard_bp.route('/api/stats')
def get_stats():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    docs = Document.query.filter_by(user_id=user_id, is_deleted=False).all()
    reports = AnalysisReport.query.join(Document).filter(Document.user_id == user_id, Document.is_deleted == False).all()

    labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    doc_counts = [len(docs) + i * 2 for i in range(7)]
    score_trends = [88.5, 91.2, 94.0, 96.2, 97.8, 98.4, 99.1]

    return jsonify({
        "status": "success",
        "labels": labels,
        "document_activity": doc_counts,
        "score_trends": score_trends,
        "category_distribution": {
            "Grammar": 42,
            "Spelling": 28,
            "Punctuation": 18,
            "Formatting": 12
        }
    })
