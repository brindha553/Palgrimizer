from datetime import datetime, timezone
import json
from app.models import db

class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(20), nullable=False)  # pdf, docx, txt, rtf, png, jpg
    file_size = db.Column(db.Integer, default=0)
    storage_path = db.Column(db.String(512), nullable=True)
    
    # Text contents
    original_text = db.Column(db.Text, nullable=False)
    corrected_text = db.Column(db.Text, nullable=True)
    
    # Status
    status = db.Column(db.String(30), default='completed')  # pending, processing, completed, error
    language = db.Column(db.String(10), default='en')
    is_deleted = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    report = db.relationship('AnalysisReport', backref='document', uselist=False, cascade='all, delete-orphan')
    corrections = db.relationship('DocumentCorrection', backref='document', lazy='dynamic', cascade='all, delete-orphan')
    versions = db.relationship('DocumentVersion', backref='document', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        report_data = self.report.to_dict() if self.report else None
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'original_filename': self.original_filename,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'status': self.status,
            'language': self.language,
            'is_deleted': self.is_deleted,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'report': report_data
        }

class AnalysisReport(db.Model):
    __tablename__ = 'analysis_reports'

    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False, unique=True)
    
    # Scores (0 to 100)
    overall_score = db.Column(db.Float, default=100.0)
    grammar_score = db.Column(db.Float, default=100.0)
    spelling_score = db.Column(db.Float, default=100.0)
    formatting_score = db.Column(db.Float, default=100.0)
    readability_score = db.Column(db.Float, default=100.0)
    professional_score = db.Column(db.Float, default=100.0)
    alignment_score = db.Column(db.Float, default=100.0)
    typography_score = db.Column(db.Float, default=100.0)
    ai_confidence = db.Column(db.Float, default=98.5)

    # Document Statistics
    word_count = db.Column(db.Integer, default=0)
    character_count = db.Column(db.Integer, default=0)
    sentence_count = db.Column(db.Integer, default=0)
    paragraph_count = db.Column(db.Integer, default=0)
    page_count = db.Column(db.Integer, default=1)
    estimated_reading_time = db.Column(db.Float, default=1.0)  # minutes

    # Categorized error count breakdown (JSON format)
    issue_counts_json = db.Column(db.Text, default='{}')

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def get_issue_counts(self):
        try:
            return json.loads(self.issue_counts_json or '{}')
        except Exception:
            return {}

    def set_issue_counts(self, counts_dict):
        self.issue_counts_json = json.dumps(counts_dict)

    def to_dict(self):
        return {
            'overall_score': self.overall_score,
            'grammar_score': self.grammar_score,
            'spelling_score': self.spelling_score,
            'formatting_score': self.formatting_score,
            'readability_score': self.readability_score,
            'professional_score': self.professional_score,
            'alignment_score': self.alignment_score,
            'typography_score': self.typography_score,
            'ai_confidence': self.ai_confidence,
            'word_count': self.word_count,
            'character_count': self.character_count,
            'sentence_count': self.sentence_count,
            'paragraph_count': self.paragraph_count,
            'page_count': self.page_count,
            'estimated_reading_time': self.estimated_reading_time,
            'issue_counts': self.get_issue_counts()
        }

class DocumentCorrection(db.Model):
    __tablename__ = 'document_corrections'

    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False)
    
    category = db.Column(db.String(50), nullable=False) # grammar, spelling, punctuation, alignment, formatting, readability, etc.
    severity = db.Column(db.String(20), default='medium') # low, medium, high, critical
    original_segment = db.Column(db.Text, nullable=False)
    suggested_segment = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.Text, nullable=False)
    
    start_index = db.Column(db.Integer, default=0)
    end_index = db.Column(db.Integer, default=0)
    
    status = db.Column(db.String(20), default='pending') # pending, accepted, rejected

    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'severity': self.severity,
            'original_segment': self.original_segment,
            'suggested_segment': self.suggested_segment,
            'explanation': self.explanation,
            'start_index': self.start_index,
            'end_index': self.end_index,
            'status': self.status
        }

class DocumentVersion(db.Model):
    __tablename__ = 'document_versions'

    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False)
    version_number = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
