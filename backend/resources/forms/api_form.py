# coding=utf-8
# auther：Liul5
# date：10/12/2019 1:30 PM
# tools：PyCharm
# Python：3.7.3

from wtforms import StringField, BooleanField
from wtforms.validators import Length, ValidationError, DataRequired, Optional, URL
from flask_wtf import FlaskForm
from models.models import ApiModel, User


class ApiForm(FlaskForm):
    status = BooleanField("Status", validators=[Optional()])
    name = StringField('Name', validators=[DataRequired(), Length(max=200)])
    description = StringField('Description', validators=[Optional()])
    project = StringField('Project', validators=[Optional()])
    method = StringField('Method', validators=[DataRequired()])
    # url = StringField('Url', validators=[DataRequired(), URL(message="url格式不正确！")])
    url = StringField('Url', validators=[DataRequired()])
    header = StringField('Header', validators=[Optional()])
    body = StringField('Body', validators=[Optional()])
    user_id = StringField('user_id', validators=[DataRequired()])
    tags = StringField('Tags', validators=[Optional()])
    imp = StringField('Imp', validators=[Optional()])

    def validate_url(self, field):
        """Email validation."""
        url = ApiModel.query.filter_by(url=field.data).first()
        if url is not None:
            raise ValidationError('该Url已经被添加！')

    def validate_user_id(self, field):
        """user_id validation."""
        user = User.query.filter_by(id=field.data).first()
        if not user:
            raise ValidationError('用户不存在！')
