import csv
import datetime

import xlsxwriter
from flask import current_app

from app.libs.enums import SignalTypeEnum


class Export2Excel:
    tuple_data = []

    def __init__(self,model_name,model):
        self.filename = model_name + '_export_'  + '.csv'
        self.path = current_app.config['UPLOADED_DOCUMENT_DEST'] + '/' + self.filename
        self.model=model

    def export2excel(self):
        outfile = open(self.path, "w", encoding="utf-8", newline="")
        outcsv = csv.writer(outfile)
        header = self.model.__table__.columns.keys()
        records = self.model.query.all()
        for record in records:
            outcsv.writerow([getattr(record, c) for c in header])
        outfile.close()
        # # 创建一个新Excel文件并添加一个工作表。
        # workbook = xlsxwriter.Workbook(self.path)
        # worksheet = workbook.add_worksheet()
        #
        # # 格式预设
        # header = workbook.add_format({
        #     'bold': True,  # 字体加粗
        #     'border': 1,  # 单元格边框宽度
        #     'align': 'center',  # 水平对齐方式
        #     'valign': 'vcenter',  # 垂直对齐方式
        #     'fg_color': '#F4B084',  # 单元格背景颜色
        #     'text_wrap': True,  # 是否自动换行
        # })
        # content = workbook.add_format({
        #     'border': 1,  # 单元格边框宽度
        #     'align': 'center',  # 水平对齐方式
        #     'valign': 'vcenter',  # 垂直对齐方式
        #     'text_wrap': True,  # 是否自动换行
        # })
        # # date_format = workbook.add_format({'num_format': 'mmmm d yyyy',
        # #                                    'align': 'center',  # 水平对齐方式
        # #                                    'valign': 'vcenter',  # 垂直对齐方式
        # #                                    'text_wrap': True,  # 是否自动换行
        # #                                    })
        #
        #
        # worksheet.set_row(0, height=30)
        # if self.signal_type == SignalTypeEnum.RadiatedNoise.value:
        #     worksheet.set_column('A:Y', 27.8)
        #     header_keys = (
        #         ['A1', '文件名'], ['B1', '版本'], ['C1', '信号类型'], ['D1', '目标类型'], ['E1', '目标弦号'], ['F1', '国别'],
        #         ['G1', '目标航速'],
        #         ['H1', '目标深度'], ['I1', '目标距离'], ['J1', '采集时间'], ['K1', '采集海域'], ['L1', '采集平台'], ['M1', '主机'],
        #         ['N1', '辅机'], ['O1', '转速'], ['P1', '轴数'], ['Q1', '叶片数'], ['R1', '低频线谱数量'], ['S1', '低频线谱频率'],
        #         ['T1', '目标图像'], ['U1', '功率谱'], ['V1', 'LOFAR谱'], ['W1', 'DEMON谱'], ['X1', 'MEL谱'], ['Y1', '分类识别结果'])
        #     for column, key in (header_keys):
        #         worksheet.write(column, key, header)
        #
        #     for i in range(len(self.tuple_data)):
        #         worksheet.set_row(i + 1, height=115)
        #     row = 1
        #     col = 0
        #     # Iterate over the data and write it out row by row.
        #     for a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y in (self.tuple_data):
        #         worksheet.write(row, col, a, content)  # 文件名
        #         worksheet.write_number(row, col + 1, b, content)  # 版本
        #         worksheet.write(row, col + 2, c, content)  # 信号类型
        #         if d:
        #             worksheet.write(row, col + 3, d, content)  # 目标类型
        #         if e:
        #             worksheet.write(row, col + 4, e, content)  # 目标弦号
        #         if f:
        #             worksheet.write(row, col + 5, f, content)  # 国别
        #         if g:
        #             worksheet.write_number(row, col + 6, g, content)  # 目标航速
        #         if h:
        #             worksheet.write_number(row, col + 7, h, content)  # 目标深度
        #         if i:
        #             worksheet.write_number(row, col + 8, i, content)  # 目标距离
        #         if j:
        #             worksheet.write_datetime(row, col + 9, j, content)  # 采集时间
        #         if k:
        #             worksheet.write(row, col + 10, k, content)  # 采集海域
        #         if l:
        #             worksheet.write(row, col + 11, l, content)  # 采集平台
        #         if m:
        #             worksheet.write(row, col + 12, m, content)  # 主机
        #         if n:
        #             worksheet.write(row, col + 13, n, content)  # 辅机
        #         if o:
        #             worksheet.write_number(row, col + 14, o, content)  # 转速
        #         if p:
        #             worksheet.write_number(row, col + 15, p, content)  # 轴数
        #         if q:
        #             worksheet.write_number(row, col + 16, q, content)  # 叶片数
        #         if r:
        #             worksheet.write_number(row, col + 17, r, content)  # 低频线谱数量
        #         if s:
        #             worksheet.write_number(row, col + 18, s, content)  # 低频线谱频率
        #         if t is not None:
        #             worksheet.insert_image(row, col + 19, t, {'object_position': 3})  # 目标图像
        #         if u is not None:
        #             worksheet.insert_image(row, col + 20, u, {'object_position': 3})  # 功率谱
        #         if v is not None:
        #             worksheet.insert_image(row, col + 21, v, {'object_position': 3})  # LOFAR谱
        #         if w is not None:
        #             worksheet.insert_image(row, col + 22, w, {'object_position': 3})  # DEMON谱
        #         if x is not None:
        #             worksheet.insert_image(row, col + 23, x, {'object_position': 3})  # MEL谱
        #         if y is not None:
        #             worksheet.write(row, col + 24, y, content)  # 分类识别结果
        #         row += 1
        # elif self.signal_type == SignalTypeEnum.TargetEcho.value:
        #     worksheet.set_column('A:Q', 27.8)
        #     header_keys = (
        #         ['A1', '文件名'], ['B1', '版本'], ['C1', '信号类型'], ['D1', '目标类型'], ['E1', '目标弦号'], ['F1', '国别'],
        #         ['G1', '目标航速'],
        #         ['H1', '目标深度'], ['I1', '目标距离'], ['J1', '采集时间'], ['K1', '采集海域'], ['L1', '采集平台'], ['M1', '主动脉冲形式'],
        #         ['N1', '回波长度'], ['O1', '回波宽度'], ['P1', '目标图像'], ['Q1', '回波时频图'])
        #     for column, key in (header_keys):
        #         worksheet.write(column, key, header)
        #
        #     for i in range(len(self.tuple_data)):
        #         worksheet.set_row(i + 1, height=115)
        #     row = 1
        #     col = 0
        #     # Iterate over the data and write it out row by row.
        #     for a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q in (self.tuple_data):
        #         worksheet.write(row, col, a, content)  # 文件名
        #         worksheet.write_number(row, col + 1, b, content)  # 版本
        #         worksheet.write(row, col + 2, c, content)  # 信号类型
        #         if d:
        #             worksheet.write(row, col + 3, d, content)  # 目标类型
        #         if e:
        #             worksheet.write(row, col + 4, e, content)  # 目标弦号
        #         if f:
        #             worksheet.write(row, col + 5, f, content)  # 国别
        #         if g:
        #             worksheet.write_number(row, col + 6, g, content)  # 目标航速
        #         if h:
        #             worksheet.write_number(row, col + 7, h, content)  # 目标深度
        #         if i:
        #             worksheet.write_number(row, col + 8, i, content)  # 目标距离
        #         if j:
        #             worksheet.write_datetime(row, col + 9, j, content)  # 采集时间
        #         if k:
        #             worksheet.write(row, col + 10, k, content)  # 采集海域
        #         if l:
        #             worksheet.write(row, col + 11, l, content)  # 采集平台
        #         if m:
        #             worksheet.write(row, col + 12, m, content)  # 主动脉冲形式
        #         if n:
        #             worksheet.write_number(row, col + 13, n, content)  # 回波长度
        #         if o:
        #             worksheet.write_number(row, col + 14, o, content)  # 回波宽度
        #         if p is not None:
        #             worksheet.insert_image(row, col + 15, p, {'object_position': 3})  # 目标图像
        #         if q is not None:
        #             worksheet.insert_image(row, col + 16, q, {'object_position': 3})  # 回波时频图
        #         row += 1
        # elif self.signal_type == SignalTypeEnum.ActivePulse.value:
        #     worksheet.set_column('A:S', 27.8)
        #     header_keys = (
        #         ['A1', '文件名'], ['B1', '版本'], ['C1', '信号类型'], ['D1', '目标类型'], ['E1', '目标弦号'], ['F1', '声纳类型'],
        #         ['G1', '国别'],
        #         ['H1', '目标航速'],
        #         ['I1', '目标深度'], ['J1', '目标距离'], ['K1', '采集时间'], ['L1', '采集海域'], ['M1', '采集平台'], ['N1', '主动脉冲形式'],
        #         ['O1', '中心频率'], ['P1', '脉冲宽度'], ['Q1', '重复周期'], ['R1', '目标图像'], ['S1', '脉冲视频图'])
        #     for column, key in (header_keys):
        #         worksheet.write(column, key, header)
        #
        #     for i in range(len(self.tuple_data)):
        #         worksheet.set_row(i + 1, height=115)
        #     row = 1
        #     col = 0
        #     # Iterate over the data and write it out row by row.
        #     for a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q,r,s in (self.tuple_data):
        #         worksheet.write(row, col, a, content)  # 文件名
        #         worksheet.write_number(row, col + 1, b, content)  # 版本
        #         worksheet.write(row, col + 2, c, content)  # 信号类型
        #         if d:
        #             worksheet.write(row, col + 3, d, content)  # 目标类型
        #         if e:
        #             worksheet.write(row, col + 4, e, content)  # 目标弦号
        #         if f:
        #             worksheet.write(row, col + 5, f, content)  #
        #         if g:
        #             worksheet.write(row, col + 6, g, content)  # 国别
        #         if h:
        #             worksheet.write_number(row, col + 7, h, content)  # 目标航速
        #         if i:
        #             worksheet.write_number(row, col + 8, i, content)  # 目标深度
        #         if j:
        #             worksheet.write_number(row, col + 9, j, content)  # 目标距离
        #         if k:
        #             worksheet.write_datetime(row, col + 10, k, content)  # 采集时间
        #         if l:
        #             worksheet.write(row, col + 11, l, content)  # 采集海域
        #         if m:
        #             worksheet.write(row, col + 12, m, content)  # 采集平台
        #         if n:
        #             worksheet.write(row, col + 13, n, content)  # 主动脉冲形式
        #         if o:
        #             worksheet.write_number(row, col + 14, o, content)  # 中心频率
        #         if p:
        #             worksheet.write_number(row, col + 15, p, content)  # 脉冲宽度
        #         if q:
        #             worksheet.write_number(row, col + 16, q, content)  # 重复周期
        #         if r is not None:
        #             worksheet.insert_image(row, col + 17, r, {'object_position': 3})  # 目标图像
        #         if s is not None:
        #             worksheet.insert_image(row, col + 18, s, {'object_position': 3})  # 脉冲时频图
        #         row += 1
        #
        #
        #
        #
        #
        # # expenses = (
        # #     ['Rent', '2020-03-21 21:21:32', url],
        # #     ['Gas', '2020-03-21 21:21:32', url],
        # #     ['Food', '2020-03-21 21:21:32', url],
        # #     ['Gym', '2020-03-21 21:21:32', url],
        # # )
        #
        # # 加宽图片列
        #
        # # worksheet.set_column(1, 35)
        # # worksheet.set_default_row(35)
        #
        # # 插入一张缩放了的图片。
        # # worksheet.write('A23', '插入一张缩放了的图片：')
        # # worksheet.insert_image('B23', url, {'x_scale': 0.5, 'y_scale': 0.5,'postioning':3})
        #
        # # postioning有以下允许的值：
        # # 1.移动和调整单元格的大小
        # # 2.移动但不调整单元格的大小（默认）
        # # 3.不移动或调整单元格的大小
        #
        # workbook.close()
