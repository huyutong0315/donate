import os

from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, IntegerField, PasswordField, FileField, DateTimeField, DecimalField, Form
from wtforms.validators import DataRequired, length, Email, Regexp, ValidationError, Length, EqualTo, AnyOf, Optional

from app.libs.error_code import CreateAccountError, LoginError, InputInfoError
from app.models.user import User

from app.validators.base import BaseForm


class EmailLoginForm(BaseForm):
    account = StringField('电子邮件', validators=[DataRequired(), length(min=1, max=64, message='长度为1-64个字符'), Email()])


class PasswordForm(BaseForm):
    password = PasswordField('密码', validators=[DataRequired(), Regexp(
        r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}$',
        message='密码至少包含 数字和英文，长度6-20')])


class NameLoginForm(BaseForm):
    account = StringField('用户名', validators=[DataRequired()])


class RegisterForm(BaseForm):
    nickname = StringField('用户名', validators=[DataRequired()])
    email = StringField('电子邮件', validators=[DataRequired(), length(min=1, max=64, message='长度为1-64个字符'), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Regexp(
        r'^(?![0-9]+$)([?!a-zA-Z]+$)[0-9A-Za-z]{6,20}$',
        message='密码至少包含 数字和英文，长度6-20')])
    password2 = PasswordField('重复密码', validators=[
        DataRequired(), Regexp(r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}$',
                               message='密码至少包含 数字和英文，长度6-20'),
        EqualTo('password', message='两次输入的密码不相同')])
    location=StringField('位置', validators=[DataRequired()])
    unit=StringField('单位', validators=[DataRequired()])
    phone=StringField('电话', validators=[DataRequired()])
    role=IntegerField('用户角色')
    integral = IntegerField('用户积分')
    # 检测用户名的重复性
    def validate_nickname(self, value):
        if value.data == 'origin' or User.query.filter_by(nickname=value.data).first():
            raise CreateAccountError(msg='用户已存在,创建失败', error_code=1010)
        return self

    # 检测邮箱的重复性
    def validate_email(self, value):
        if User.query.filter_by(email=value.data).first():
            raise CreateAccountError(msg='邮箱已存在,创建失败', error_code=1011)
        return self

    # 检测邮箱的重复性
    def validate_phone(self, value):
        if User.query.filter_by(phone=value.data).first():
            raise CreateAccountError(msg='手机号已存在,创建失败', error_code=1011)
        return self

class SoundFileForm(Form):
    audio = FileField('声音文件', validators=[FileRequired(), FileAllowed(['wav', 'mp3'])])


class PictureFileForm(Form):
    picture = FileField('图片文件', validators=[Optional(strip_whitespace=True),
                                            FileAllowed(['jpg', 'png', 'jpeg', 'JPG', 'PNG', 'JPEG'])])


# class FileForm(Form):
#     audio = FileField('声音文件', validators=[FileRequired(), FileAllowed(['wav', ])])
#     picture = FileField('图片文件', validators=[Optional(strip_whitespace=True), FileAllowed(['jpg', 'png'])])


class ChangePasswordForm(BaseForm):
    oldpassword = PasswordField('旧密码', validators=[DataRequired(), Regexp(
        r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}$',
        message='密码至少包含 数字和英文，长度6-20')])
    newpassword = PasswordField('新密码', validators=[DataRequired(), Regexp(
        r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}$',
        message='密码至少包含 数字和英文，长度6-20')])
    renewpassword = PasswordField('重复新密码', validators=[
        DataRequired(), Regexp(r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}$',
                               message='密码至少包含 数字和英文，长度6-20'),
        EqualTo('newpassword', message='两次输入的密码不相同')])


class ChangePasswordByAdminForm(BaseForm):
    newpassword = PasswordField('新密码', validators=[DataRequired(), Regexp(
        r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}$',
        message='密码至少包含 数字和英文，长度6-20')])
    renewpassword = PasswordField('重复新密码', validators=[
        DataRequired(), Regexp(r'^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}$',
                               message='密码至少包含 数字和英文，长度6-20'),
        EqualTo('newpassword', message='两次输入的密码不相同')])

