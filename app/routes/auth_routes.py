import random
from datetime import datetime, timedelta, timezone
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models import db
from app.models.user import User, OTPCode, UserActivity

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return redirect(url_for('dashboard.index'))
        
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = request.form.get('remember') == 'on'

        if not email or not password:
            flash('Please fill in all required fields.', 'danger')
            return render_template('auth/login.html')

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash('Invalid email or password credentials.', 'danger')
            return render_template('auth/login.html')

        # Log in user
        session['user_id'] = user.id
        session['user_name'] = user.full_name
        session['user_email'] = user.email

        # Record activity
        activity = UserActivity(user_id=user.id, action="Logged In", ip_address=request.remote_addr)
        db.session.add(activity)
        db.session.commit()

        flash(f'Welcome back, {user.full_name}!', 'success')
        return redirect(url_for('dashboard.index'))

    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user_id'):
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not full_name or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('auth/register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('An account with this email already exists.', 'warning')
            return render_template('auth/register.html')

        new_user = User(full_name=full_name, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        # Create sample welcome document for the new user
        from app.services.nlp_engine import nlp_detector
        from app.models.document import Document, AnalysisReport, DocumentCorrection
        
        sample_text = (
            "Teh pilgrimizer platform is an enterprise-grade document correction tool. "
            "It automatically detect grammar, spelling, punctuation and alignment mistakes.\n\n"
            "Section 1: executive overview\n"
            "This sample document demonstrates side-by-side comparison, score cards, and inline diff editing. "
            "You can accept or reject individual suggestions, split long sentences, and export to PDF or DOCX format."
        )
        
        analysis = nlp_detector.analyze_document(sample_text)
        doc = Document(
            user_id=new_user.id,
            title="Sample Welcome Document.docx",
            original_filename="Sample Welcome Document.docx",
            file_type="docx",
            file_size=len(sample_text),
            original_text=sample_text,
            corrected_text=analysis["corrected_text"],
            language="en"
        )
        db.session.add(doc)
        db.session.flush()

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

        # Log user in
        session['user_id'] = new_user.id
        session['user_name'] = new_user.full_name
        session['user_email'] = new_user.email

        flash('Registration successful! Welcome to Palgrimizer.', 'success')
        return redirect(url_for('dashboard.index'))

    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out safely.', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        user = User.query.filter_by(email=email).first()
        if user:
            # Generate OTP code
            code = str(random.randint(100000, 999999))
            expires = datetime.now(timezone.utc) + timedelta(minutes=15)
            otp = OTPCode(email=email, code=code, purpose='reset_password', expires_at=expires)
            db.session.add(otp)
            db.session.commit()
            
            return render_template('auth/otp_verify.html', email=email, code_preview=code)
        else:
            flash('No account registered with that email address.', 'danger')

    return render_template('auth/forgot_password.html')

@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    email = request.form.get('email', '').strip().lower()
    code = request.form.get('otp', '').strip()
    new_password = request.form.get('new_password', '')

    otp_record = OTPCode.query.filter_by(email=email, code=code, is_used=False).order_by(OTPCode.id.desc()).first()
    if not otp_record:
        flash('Invalid OTP code entered.', 'danger')
        return render_template('auth/otp_verify.html', email=email)

    otp_record.is_used = True
    user = User.query.filter_by(email=email).first()
    if user and new_password:
        user.set_password(new_password)
        db.session.commit()
        flash('Password reset successful! Please log in with your new password.', 'success')
        return redirect(url_for('auth.login'))

    flash('OTP verified successfully.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/google-login-sim', methods=['POST'])
def google_login_sim():
    # Simulated Google OAuth SSO endpoint
    data = request.json or {}
    email = data.get('email', 'google.user@palgrimizer.io')
    full_name = data.get('name', 'Google SSO User')

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(full_name=full_name, email=email)
        user.set_password('GoogleSSOSecret2026!')
        db.session.add(user)
        db.session.commit()

    session['user_id'] = user.id
    session['user_name'] = user.full_name
    session['user_email'] = user.email

    return jsonify({"status": "success", "redirect_url": url_for('dashboard.index')})
