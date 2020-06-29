# coding=utf-8
# auther：Liul5
# date：10/24/2019 1:40 PM
# tools：PyCharm
# Python：3.7.3

from wtforms import StringField, BooleanField
from wtforms.validators import Length, DataRequired, Optional
from flask_wtf import FlaskForm


class ReportForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=200)])
    result = StringField('Result', validators=[Optional()])
    status = BooleanField("Status", validators=[Optional()])
    user_id = StringField('user_id', validators=[DataRequired()])
    api_id = StringField('api_id', validators=[DataRequired()])
