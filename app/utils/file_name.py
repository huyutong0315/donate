import datetime
import os


def generate_file_name(filepath,id):
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    (folder, extension) = os.path.splitext(filepath)
    print(folder,extension)
    filename = folder + '_' + now + extension
    print(filename)


if __name__ == "__main__":
    generate_file_name('E:/pyprojects/seadatabase/app/static/uploads/audios/zhenh_1604057181.wav',3)