from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
from datetime import datetime, timedelta

bp = Blueprint("log", __name__)
session_dict = {}

@bp.route("/metric/<key>/sum", methods=("GET",))
def get_aggregates(key):
    if session_dict.get('log') is None or session_dict['log'].get(key) is None:
        error = "No logs yet"
        flash(error)
        return {"error": 404}

    #include only the most recent hour
    aggregate_sum = 0
    for datum in session_dict['log'][key]:
        if datum['timestamp'] > (datetime.now() - timedelta(hours=1)):
            aggregate_sum += datum['value']

    return { "value": aggregate_sum }

@bp.route("/metric/<key>", methods=("POST",))
def event_log(key):
    """Stores the value for a given metric key."""
    if session_dict.get('log') is None:
        session_dict['log'] = {}
    if session_dict['log'].get(key) is None:
        session_dict['log'][key] = []

    value = int(request.form['value'])

    session_dict['log'][key].append({ "value": value, "timestamp": datetime.now() })

    return {} 