
# 利用AOP思想统一处理异常
# flask提供的处理全局异常
from werkzeug.exceptions import HTTPException

from app.libs.error import APIException
from app.libs.error_code import ServerError
from app.api import create_app
app = create_app()
@app.errorhandler(Exception)
def framework_error(e):
    # APIException
    # HTTPException
    # Exception

    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return APIException(msg, code, error_code)
    else:
        if not app.config['DEBUG']:
            return ServerError()
        else:
            # 在开发模式下，我们还是返回具体的堆栈错误信息
            raise e

if __name__ == '__main__':
    app.run(debug=True)