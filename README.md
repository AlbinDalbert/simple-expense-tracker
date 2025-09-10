# simple-expense-tracker


## Overview

A backend application for recording expenses and summarize monthly expenses.


## Endpoints

### [GET] /ping
Just a ping to check if the service is up.

### [GET] /expenses
Get a list of all recorded expenses.

### [GET] /summary/monthly
Get a monthly summary of the given month and year. By default it uses the current month.
| Field      | Type     | Required | Description                      |
| :--------- | :------- | :------- | :------------------------------- |
| `year`   | `integer`  | No      | The year to calculate the summary of |
| `month` | `integer` | No      | The month given as a number (1-12)     |

Example:
```
curl "http://127.0.0.1:5000/summary/monthly?year=2025&month=9"
```

### [POST] /expenses
Adding a new expense including amount and categoty with the option of a date (default date set to now).

| Field      | Type     | Required | Description                      |
| :--------- | :------- | :------- | :------------------------------- |
| `amount`   | `float`  | Yes      | The monetary value of the expense. |
| `category` | `string` | Yes      | The category of the expense.     |
| `date`     | `string` | No       | ISO 8601 format (e.g., "2025-09-15T10:00:00"). |

Example eequest body:
```
{
    "amount": 55.0,
    "category": "Groceries",
    "date": "2025-09-15T10:00:00"
}
```

## Build and Run
*(these instructions are aimed for an linux environment)*

Prerequisites
- Python 3.12+
- pip

Clone the repository and enter the directory.
```
git clone https://github.com/AlbinDalbert/simple-expense-tracker.git
cd simple-expense-tracker
```

Create a virtual environment and intall the dependencies.
```
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

Run the application:
```
flask run
```

And it can now be reached at `http://127.0.0.1:5000`


## CI/CD
Using GitHub Actions, the test suite is automatically executed and ran on push/pull request. The pipeline is defined in `/.github/workflows`.
If tests pass, it then packages the application into a .zip file `expense-tracker.zip`


## Decistions

The decision to use an SQL database was clear for it's strenth in operations over many rows, even if the application doesn't utilize very much of these strenths right now. It's reasonable that any functionality expansion would benefit from it. 

A great improvment that could me implemented to make the behaviour significantly more reliable would be to change the category field into a foreign key to an table with all valid categories. That was decided to be out of scope for this, but it would be a great improvment in reliablilety and stability.
