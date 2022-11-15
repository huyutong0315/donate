from pydub import AudioSegment


# 在原文件位置上进行格式转换
def trans_mp3_to_wav(filepath):
    song = AudioSegment.from_mp3(filepath)
    song.export(filepath[:-4] + ".wav", format="wav")
