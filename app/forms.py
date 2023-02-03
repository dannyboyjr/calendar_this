from flask_wtf import FlaskForm
from wtforms.fields import (
    BooleanField, DateField, StringField, SubmitField, TextAreaField, TimeField
)
from wtforms.validators import DataRequired, Length, ValidationError
from datetime import datetime


class AppointmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=20)])
    startdate = DateField('startdate', validators=[DataRequired()])
    starttime = TimeField('starttime', validators=[DataRequired()])
    enddate = DateField('enddate',validators=[DataRequired()])
    endtime = TimeField('endtime',validators=[DataRequired()])
    description = TextAreaField("description", validators=[DataRequired()])
    private = BooleanField('private')
    submit = SubmitField('submit')
    
    def validate_end_date(form, field):
        start = datetime.combine(form.start_date.data, form.start_time.data)
        end = datetime.combine(field.data, form.end_time.data)
        if start >= end:
            msg = "End date/time must come after start date/time"
        raise ValidationError(msg)


