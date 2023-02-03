from flask import (Blueprint, render_template, redirect)
import os
import sqlite3
from datetime import datetime
from app.forms import AppointmentForm

bp = Blueprint('main', __name__, url_prefix='/')

DB_FILE = os.environ.get("DB_FILE")


@bp.route("/", methods=["GET", "POST"])
def main():
    form = AppointmentForm()
    if form.validate_on_submit():
        params = {
            'name': form.name.data,
            'start_datetime': datetime.combine(form.startdate.data, form.starttime.data),
            'end_datetime': datetime.combine(form.enddate.data, form.endtime.data),
            'description': form.description.data,
            'private': form.private.data
        }
        with sqlite3.connect(DB_FILE) as conn:
            curs = conn.cursor()
            curs.execute(
                """
                INSERT INTO appointments(name, start_datetime, end_datetime, description, private)
                VALUES
                (:name, :start_datetime, :end_datetime, :description, :private)
                """, params
            )
        return redirect('/')
                
                
    with sqlite3.connect(DB_FILE) as conn:
        curs = conn.cursor()
        curs.execute(
            """
            SELECT id, name, start_datetime, end_datetime, description
            FROM appointments
            ORDER BY start_datetime
            """
        )
        results = curs.fetchall()
        print(results)
        rows = []
        for item in results:
            item = list(item)
            item[2] = datetime.strptime(item[2], '%Y-%m-%d %H:%M:%S')
            item[3] = datetime.strptime(item[3], '%Y-%m-%d %H:%M:%S')
            rows.append(item)
    return render_template('main.html', rows=rows, form=form)


