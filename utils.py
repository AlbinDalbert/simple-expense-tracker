import json
import os
import logging

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def log_action(action, message):
    """Logs an action and message to a file."""
    logging.info(f"Action: {action}, Message: {message}")
