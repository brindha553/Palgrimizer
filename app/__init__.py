import os
from flask import Flask, render_template
from app.config import Config
from app.models import db

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    # Ensure required folders exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.instance_path, exist_ok=True)

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints
    from app.routes.main_routes import main_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.dashboard_routes import dashboard_bp
    from app.routes.document_routes import document_bp
    from app.routes.history_routes import history_bp
    from app.routes.assistant_routes import assistant_bp
    from app.routes.api_routes import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(document_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(assistant_bp)
    app.register_blueprint(api_bp)

    # Create tables
    with app.app_context():
        db.create_all()

    # Context Processors & Error Handlers
    @app.context_processor
    def inject_user():
        from flask import session
        from app.models.user import User
        user_id = session.get('user_id')
        current_user = User.query.get(user_id) if user_id else None
        return dict(current_user=current_user)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('base.html', error_code="404", error_message="Page Not Found"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('base.html', error_code="500", error_message="Internal Server Error"), 500

    return app
