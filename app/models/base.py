from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from contextlib import contextmanager
from app.libs.error_code import NotFound, DataBaseNotFound


# 定义子类，用上下文管理器管理每次的错误处理以及回滚
class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


class Query(BaseQuery):
    # def filter_by(self, **kwargs):
    #     if 'is_delete' not in kwargs.keys():
    #         kwargs['is_delete'] = 0
    #     return super(Query, self).filter_by(**kwargs)

    def get_or_404(self, ident):
        rv = self.get(ident)
        if rv is None:
            raise DataBaseNotFound()
        return rv

    def first_or_404(self):
        rv = self.first()
        if rv is None:
            raise DataBaseNotFound()
        return rv


db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    __abstract__ = True

    # is_delete = Column(SmallInteger, server_default='0')

    # 对象转换为字典，要重写的2个方法，可以提取一个到基类
    def __getitem__(self, item):
        return getattr(self, item)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None)
                for c in self.__table__.columns}

    # 接收一个字典，如果这个字典里面的属性和模型里面是一样的，就赋值给它，和jsontodb类似
    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def keys(self):
        return self.fields

    def hide(self, *keys):
        for key in keys:
            self.fields.remove(key)
        return self

    def append(self, *keys):
        for key in keys:
            self.fields.append(key)
        return self

    # def delete(self):
    #     self.status = 0
