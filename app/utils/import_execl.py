import csv
from datetime import datetime

from flask import current_app

import pandas as pd

from app.models import json2db, json2db_add


class Import2Execl:


    def __init__(self, model_name, model):
        self.filename = model_name + '_export_' + '.csv'
        self.path = current_app.config['UPLOADED_DOCUMENT_DEST'] + '/' + self.filename
        self.model = model
        self.model_name=model_name

    def import2excel(self,uid):
        header = self.model.__table__.columns.keys()
        with open(self.path, encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)

            list=[]
            for item in reader:
                # 通过node_id导入，修改对象属性值
                data=dict(zip(header,item))
                if 'visit_date' in data and data['visit_date']=='':
                    data['visit_date']=datetime.now().strftime('%Y%m%d%H%M%S')

                if 'collect_time' in data and data['collect_time']=='':
                    data['collect_time']=datetime.now().strftime('%Y%m%d%H%M%S')
                if 'user_id' in data:
                    data['user_id']=uid
                # json2db(data,self.model)=
                id=data.pop('id')
                model=json2db_add(data,self.model)
                id_dict=dict(old_id=id,new_id=model.id)
                list.append(id_dict)
        outfile = open(current_app.config['UPLOADED_DOCUMENT_DEST'] + '/' + self.model_name + 'id副本' + '.csv', "w",
                           encoding="utf-8", newline="")
        outcsv = csv.writer(outfile)
        outcsv.writerow(['old_id','new_id'])
        outcsv.writerow(list)
        outfile.close()


