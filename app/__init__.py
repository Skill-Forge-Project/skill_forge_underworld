from flask import Flask, redirect, url_for, render_template, flash, jsonify, send_file
from app.database_conn import db
from flask_migrate import Migrate
from config import Config
from app.boss_routes import boss_bp


migrate = Migrate()


def create_app():
    # Initialize the Flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the database
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register the Blueprint
    app.register_blueprint(boss_bp)
    
    # Create the database tables
    with app.app_context():
        db.create_all()
    
    return app