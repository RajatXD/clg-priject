from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from pathlib import Path

app = Flask(__name__)

# Ensure absolute path for SQLite database
db_path = Path(__file__).parent / 'lost_and_found.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)

# Define models
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='lost')

@app.route('/')
def home():
    items = Item.query.all()
    return f"Total items: {len(items)}"

# Create database tables and add sample data
with app.app_context():
    db.create_all()
    
    # Add sample items if database is empty
    if not Item.query.first():
        sample_items = [
            Item(name='Phone', description='Black iPhone found in library', status='found'),
            Item(name='Wallet', description='Brown leather wallet lost in cafeteria', status='lost'),
            Item(name='Keys', description='Car keys with red keychain', status='lost')
        ]
        db.session.add_all(sample_items)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)