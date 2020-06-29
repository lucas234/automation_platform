# coding=utf-8
# auther：Liul5
# date：10/10/2019 4:59 PM
# tools：PyCharm
# Python：3.7.3

from wtforms import StringField, PasswordField
from wtforms.validators import Length, ValidationError, DataRequired
from models.models import User
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired(), Length(4, 16)])

    # 验证函数必须以validate_开头，加上定义的字段password等结尾，否则无效
    def validate_password(self, field):
        if not self.get_user():
            raise ValidationError('the username or password is wrong!')
        if not self.get_user().verify_password(field.data):
            raise ValidationError('the username or password is wrong!')

    def get_user(self):
        return User.query.filter_by(username=self.username.data).first()


