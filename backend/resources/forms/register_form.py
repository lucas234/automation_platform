# coding=utf-8
# auther：Liul5
# date：10/12/2019 1:30 PM
# tools：PyCharm
# Python：3.7.3

from wtforms import StringField, PasswordField, SelectField, SelectMultipleField, BooleanField
from wtforms.validators import Length, ValidationError, DataRequired, Email, Regexp, EqualTo, Optional
from flask_wtf import FlaskForm
from models.models import User


class RegisterForm(FlaskForm):
    role = BooleanField("Role", validators=[Optional()])
    username = StringField('Username', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired(), Length(4, 16)])
    # pwd_confirm = PasswordField('Confirm Password', validators=[DataRequired(),
    #  EqualTo('password', message='密码不一致!')])
    email = StringField('Email', validators=[Email(message="输入邮箱格式无效！"), Optional()])
    address = StringField('Address', validators=[Optional()])
    phone = StringField('Phone', validators=[Optional(), Regexp(r'1\d{10}', message='手机号码格式错误!')])
    # 单选按钮
    gender = SelectField('Gender', validators=[Optional()], coerce=int, choices=[(1, '男'), (2, '女')])
    # 多选按钮
    tech = SelectMultipleField('擅长领域', coerce=int, validators=[Optional()],
                               choices=[(1, 'python'), (2, 'linux'), (3, 'java'), (4, 'php'), (5, 'ruby'), (6, 'c++')])

    def validate_username(self, field):
        """username validation."""
        user = User.query.filter_by(username=field.data).first()
        if user is not None:
            raise ValidationError('用户名已被注册！')

    def validate_email(self, field):
        """Email validation."""
        user = User.query.filter_by(email=field.data).first()
        if user is not None:
            raise ValidationError('邮箱已被注册！')
