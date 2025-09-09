from flask import Blueprint, request, jsonify, Flask
from models import db, Expense
from sqlalchemy import func, extract
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok", "message": "App is running"}), 200


@main_bp.route('/expenses', methods=['GET'])
def get_expenses():
    
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    return jsonify([
        {"id": e.id, "amount": e.amount, "category": e.category, "date": e.date.isoformat()}
        for e in expenses
    ]), 200


@main_bp.route('/summary/monthly', methods=['GET'])
def monthly_summary():
    
    year = request.args.get('year', default=datetime.utcnow().year, type=int)
    month = request.args.get('month', default=datetime.utcnow().month, type=int)

    summary = db.session.query(
        Expense.category,
        func.sum(Expense.amount).label('total_amount')
    ).filter(
        extract('year', Expense.date) == year,
        extract('month', Expense.date) == month
    ).group_by(
        Expense.category
    ).all()

    summary_dict = {category: total for category, total in summary}
    return jsonify(summary_dict), 200

@main_bp.route('/expenses', methods=['POST'])
def add_expenses():
    data = request.get_json()

    if not data or 'amount' not in data or 'category' not in data:
        return jsonify({"error": "Missing amount or category"}), 400

    if not isinstance(data['amount'], (int, float)) or data['amount'] <= 0:
        return jsonify({"error": "Amount must be a positive number"}), 400

    try:
        expense_date = datetime.fromisoformat(data['date']) if 'date' in data else datetime.utcnow()
        
        new_expense = Expense(
            amount=data['amount'],
            category=data['category'],
            date=expense_date
        )
        db.session.add(new_expense)
        db.session.commit()
        return jsonify({"message": "Expense added successfully", "id": new_expense.id}), 201
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid date format. Please use ISO format (YYYY-MM-DDTHH:MM:SS)."}), 400


def create_app(config_override=None):
    """The application factory."""
    app = Flask(__name__, instance_relative_config=False, instance_path='/data')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////data/db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if config_override:
        app.config.update(config_override)

    db.init_app(app)

    app.register_blueprint(main_bp)

    return app

app = create_app()
