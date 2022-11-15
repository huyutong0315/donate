from app.libs.error import APIException


class ServerError(APIException):
    # code = 500
    msg = 'sorry, we made a mistake ^_^'
    error_code = 999


# 为我们自定义的validator验证器,定制错误码
class ParameterException(APIException):
    # code = 400
    msg = 'invalid parameter'
    error_code = 1001
class Forbiden(APIException):
    # code = 400
    msg = '你只能修改自己出的题目或者题目不存在'
    error_code = 401


class NotFound(APIException):
    # code = 404
    msg = 'the resource are not_found.'
    error_code = 1002


class DataBaseNotFound(APIException):
    msg = 'database query not found.'
    error_code = 1027


class AuthFailed(APIException):
    # code = 401 # 401代表授权失败，可能账号密码错误
    msg = 'authorization failed'
    error_code = 1003


class Forbidden(APIException):
    # code = 403    #权限无法访问
    msg = 'forbidden,not in scope'
    error_code = 1004


class CreateAccountError(APIException):
    msg = 'Create Account Error'
    error_code = 1005


class LoginError(APIException):
    msg = 'Login Error'
    error_code = 1013


class InputInfoError(APIException):
    msg = 'Input Info Error'
    error_code = 1018

class NameRepeated(APIException):
    msg = 'Name has been occupied'
    error_code = 1019
