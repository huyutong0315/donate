import os
import shutil
import datetime

from pydub import AudioSegment
from app.api import audio
from app.models import json2db_add, json2db, db
from app.models.sound import Sound
from app.models.sound_copy import SoundCopy
from app.utils.file import File
from app.utils.file_rename import file_rename

parent_path = os.path.dirname(os.path.dirname(__file__))
EXPORT_PATH = (parent_path + '/static/uploads/audios/').replace('\\', '/')


# 老板
# 秘书
# 工具人
# 具体命令
# 具体任务
# 命令


# 抽象命令接口，声明接口execute，具体的命令都继承这个接口
class Command:
    def execute(self):
        pass


# 命令接受者，负责执行具体任务，卑微的打工人，同时定义工具人所有能做的任务
class Receiver:
    def __init__(self, origin_file_name, user_id):
        # 源文件名，也就是前端永远显示的那个名字，这样可以很好地把显示的名字和副本关联起来
        self.origin_file_name = origin_file_name
        self.user_id = user_id
        # 通过源文件名找到源文件音频
        self.sound = Sound.query.filter_by(name=self.origin_file_name).first_or_404()
        # 通过源文件音频找到对应它的副本
        self.duplicated_audio = self.sound.duplicated_audio(self.user_id)
        # 通过副本找到副本路径
        self.audio_path = File(audio).get_file_path(self.duplicated_audio.filename)
        self.copy_tmp_path = EXPORT_PATH + 'u' + str(self.user_id) + '_temp_file_' + self.sound.name
        self.copy_tmp_output_path = EXPORT_PATH + 'u' + str(self.user_id) + '_temp_output_file_' + self.sound.name

    def test(self, str):
        print(str)

    # 根据起始和结束时间点复制音频
    def copy(self, start, end):
        audio = AudioSegment.from_file(self.audio_path, format='wav')
        audio[start:end].export(self.copy_tmp_path, format='wav')
        return audio[start:end]

    # 根据起始和结束时间点复制音频,用来导出
    def copy_output(self, start, end):
        audio = AudioSegment.from_file(self.audio_path, format='wav')
        audio[start:end].export(self.copy_tmp_output_path, format='wav')
        return audio[start:end]

    # 将复制的音频粘贴到目标音频指定的时间段，即用复制的音频替换掉某段音频
    def paste_segment(self, target_segment_start, target_segment_end):
        paste_audio = AudioSegment.from_file(self.copy_tmp_path, format='wav')
        audio = AudioSegment.from_file(self.audio_path, format='wav')
        res_audio = audio[:target_segment_start] + paste_audio + audio[target_segment_end:]
        return res_audio,len(paste_audio)

    # 根据起始和结束时间删除目标音频片段
    def delete(self, start, end):
        audio = AudioSegment.from_file(self.audio_path, format='wav')
        res_audio = audio[:start] + audio[end:]
        return res_audio

    # 修改副本后重新输出到副本
    def output(self, audio):
        audio.export(self.audio_path, format='wav')

    # 当前版本编辑进度重置，也就是用当前版本文件重置副本文件
    def reset(self):
        now_version = self.duplicated_audio.now_version
        for sc in self.sound.all_version_desc(self.user_id):
            if sc.version == now_version:
                shutil.copy(File(audio).get_file_path(sc.filename),
                            File(audio).get_file_path(self.duplicated_audio.filename))
                now = datetime.datetime.now()
                with db.auto_commit():
                    self.duplicated_audio.generate_time = now
                break

    # 回退到指定版本，副本也要重置
    def rollback(self, version):
        with db.auto_commit():
            for sc in self.sound.all_version_desc(self.user_id):
                sc.now_version = version
        self.reset()

    # 将副本文件保存成版本文件
    def save_file(self):
        version = self.duplicated_audio.max_version + 1
        now = datetime.datetime.now()
        # new_version_name = 'u' + str(self.user_id) + '_' + str(int(now.timestamp())) + '_v' + str(
        #     version) + '_' + self.sound.name
        version = f'V{version}'
        new_version_name = file_rename([2, 3, 5], self.sound.name,
                                       [str(self.user_id), now.strftime('%Y%m%d%H%M%S'), version])

        self.sound.create_copy(self.duplicated_audio.filename, new_version_name)
        return new_version_name, now

    # 用户点击保存后，将副本文件信息保存到数据库中，一般紧接save方法调用，存入数据库（generate_time需要datetime.datetime类型）
    def save_db(self, filename, generate_time):
        # 准备数据插入SoundCopy表
        version = self.duplicated_audio.max_version + 1
        data = dict(filename=filename, user_id=self.user_id, generate_time=generate_time, version=version,
                    sound_id=self.sound.id, now_version=version, max_version=version)
        json2db(data, SoundCopy)

        # 修改所有版本数据库记录中当前版本和最大版本的信息
        with db.auto_commit():
            for sc in self.sound.all_version_desc(self.user_id):
                sc.now_version = version
                sc.max_version = version
            self.duplicated_audio.generate_time = generate_time


# 具体命令，把命令接受者和多个任务绑定在一起组成一个具体命令，执行函数定义这个命令要求工具人应该完成的具体事情:
# 命令0：复制某段音频，这个命令不会对原文件产生改变
class Copy(Command):
    def __init__(self, receiver, start, end):
        self.receiver = receiver
        self.start = start
        self.end = end

    def execute(self):
        self.receiver.copy(self.start, self.end)

class CopyOutput(Command):
    def __init__(self, receiver, start, end):
        self.receiver = receiver
        self.start = start
        self.end = end

    def execute(self):
        self.receiver.copy_output(self.start, self.end)


# 命令2：粘贴音频到某个时间段，即用复制的音频替换掉目标时间段音频，并输出
class PasteSegment(Command):
    def __init__(self, receiver, target_segment_start, target_segment_end):
        self.receiver = receiver
        self.target_segment_start = target_segment_start
        self.target_segment_end = target_segment_end

    def execute(self):
        audio,audio_len = self.receiver.paste_segment(self.target_segment_start, self.target_segment_end)
        self.receiver.output(audio)
        return audio_len


# 命令3：删除某段音频，并输出
class Delete(Command):
    def __init__(self, receiver, start, end):
        self.receiver = receiver
        self.start = start
        self.end = end

    def execute(self):
        audio = self.receiver.delete(self.start, self.end)
        self.receiver.output(audio)


# 命令4：剪切某段音频，并输出
class Cut(Command):
    def __init__(self, receiver, start, end):
        self.receiver = receiver
        self.start = start
        self.end = end

    def execute(self):
        self.receiver.copy(self.start, self.end)
        audio = self.receiver.delete(self.start, self.end)
        self.receiver.output(audio)


# 命令5：保存版本
class Save(Command):
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        filename, generate_time = self.receiver.save_file()
        self.receiver.save_db(filename, generate_time)


# 命令6：回滚
class RollBack(Command):
    def __init__(self, receiver, version):
        self.receiver = receiver
        self.version = version

    def execute(self):
        self.receiver.rollback(version=self.version)


# 命令6：回滚
class Reset(Command):
    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.reset()


class Test(Command):
    def __init__(self, receiver, str):
        self.receiver = receiver
        self.str = str

    def execute(self):
        self.receiver.test(self.str)


# 命令调用者，秘书，执行一个具体命令，从此一个具体命令有了发起者、接受者和任务，就开干了
class Invoker:
    def execute(self, cmd):
        return cmd.execute()
