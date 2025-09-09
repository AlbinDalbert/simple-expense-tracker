import pytest
import json
from models import Expense
from datetime import datetime
from app import create_app, db

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


# tests 
def test_add_valid_expense(client):
    """
    add a valid expense.
    """
    expense_data = {
        "amount": 55.0,
        "category": "Groceries",
        "date": "2025-09-15T10:00:00"
    }
    response = client.post('/expenses', data=json.dumps(expense_data), content_type='application/json')

    assert response.status_code == 201

    expense = Expense.query.first()
    assert expense is not None
    assert expense.category == "Groceries"
    assert expense.amount == 55.0
    

def test_add_invalid_expense(client, app):
    """
    Test posting an invalid expense
    """
    invalid_expense = {"amount": -10, "category": "Invalid"}
    response = client.post('/expenses', data=json.dumps(invalid_expense), content_type='application/json')
    assert response.status_code == 400


def test_getting_expenses(client, app):
    """
    Test if the GET /expenses endpoint works and returns the correct data.
    """
    expense_data = {
        "amount": 55.0,
        "category": "Groceries",
        "date": "2025-09-15T10:00:00"
    }
    response = client.post('/expenses', data=json.dumps(expense_data), content_type='application/json')
    expense_data = {
        "amount": 155.0,
        "category": "Transport",
        "date": "2025-09-16T10:00:00"
    }
    response = client.post('/expenses', data=json.dumps(expense_data), content_type='application/json')

    
    response = client.get('/expenses')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    
    returned_categories = [item['category'] for item in data]
    assert "Groceries" in returned_categories
    assert "Transport" in returned_categories


def test_monthly_summary(client, app):
    """
    Test the monthly summary endpoint /summary/monthly  
    """
    expense_data = {
        "amount": 55.0,
        "category": "Groceries",
        "date": "2025-09-15T10:00:00"
    }
    response = client.post('/expenses', data=json.dumps(expense_data), content_type='application/json')
    
    expense_data = {
        "amount": 95.0,
        "category": "Groceries",
        "date": "2025-09-15T10:00:00"
    }
    response = client.post('/expenses', data=json.dumps(expense_data), content_type='application/json') 

    expense_data = {
        "amount": 155.0,
        "category": "Transport",
        "date": "2025-09-16T10:00:00"
    }
    response = client.post('/expenses', data=json.dumps(expense_data), content_type='application/json')
    
    expense_data = { # should be ignored by summary due to date
        "amount": 55.0,
        "category": "Groceries",
        "date": "2025-07-15T10:00:00"
    }
    response = client.post('/expenses', data=json.dumps(expense_data), content_type='application/json')

    response = client.get('/summary/monthly?year=2025&month=9')
    assert response.status_code == 200
    data = json.loads(response.data)
 
    expected_summary = {
        "Groceries": 150.0,
        "Transport": 155.0
    }

    assert data == expected_summary

def test_empty_month_summary(client):
    """
    Test summary in case of no expenses for the given month.
    """
    response = client.get('/summary/monthly?year=2030&month=1')
    assert response.status_code == 200
    assert response.get_json() == {}


def test_add_expense_missing_category(client):
    """
    test adding expense without category.
    """
    invalid_data = {"amount": 50.0}
    response = client.post('/expenses', data=json.dumps(invalid_data), content_type='application/json')
    assert response.status_code == 400
