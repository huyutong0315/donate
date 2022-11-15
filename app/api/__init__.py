from flask_cors import *
from flask_uploads import configure_uploads, DOCUMENTS

from app.app import Flask
from app.libs.email import mail
from app.libs.rewrite_flask_upload import MyUploadSet
from app.utils.folder import create_folder
from flask_compress import Compress
photo = MyUploadSet('photo', ('jpg','png','jpeg','JPG','PNG','JPEG'))
audio = MyUploadSet('audio', ('mp3','wav'))
document = MyUploadSet('document',DOCUMENTS)
compress = Compress()


def register_blueprints(app):
    from app.api.v1 import create_blueprint_v1
    app.register_blueprint(create_blueprint_v1(), url_prefix='/v2')  # 给蓝图 路由绑定固定的前缀/v1


def register_plugin(app):
    from app.models.base import db
    db.init_app(app)
    with app.app_context():
        db.create_all()


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    # 导入配置文件
    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.secure')
    CORS(app, supports_credentials=True)

    app.config['COMPRESS_REGISTER'] = False
    compress.init_app(app)
    # CORS(app, resources={r"/*": {"origins": "*"}}, send_wildcard=True)
    register_blueprints(app)
    register_plugin(app)
    mail.init_app(app)
    configure_uploads(app, [photo,audio,document])
    create_folder(app.config['UPLOADED_AUDIO_DEST'])
    create_folder(app.config['UPLOADED_PHOTO_DEST'])
    create_folder(app.config['UPLOADED_DOCUMENT_DEST'])

    return app
