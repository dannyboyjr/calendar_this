from flask import (Blueprint, render_template)
import os
import sqlite3
from datetime import datetime

bp = Blueprint('main', __name__, url_prefix='/')

DB_FILE = os.environ.get("DB_FILE")


@bp.route("/")
def main():
    with sqlite3.connect(DB_FILE) as conn:
        curs = conn.cursor()
        curs.execute(
            """
            SELECT id, name, start_datetime, end_datetime
            FROM appointments
            ORDER BY start_datetime
            """
        )
        results = curs.fetchall()
        rows = []
        for item in results:
            item = list(item)
            item[2] = datetime.strptime(item[2], '%Y-%m-%d %H:%M:%S')
            item[3] = datetime.strptime(item[3], '%Y-%m-%d %H:%M:%S')
            rows.append(item)
    return render_template('main.html', rows=rows)


