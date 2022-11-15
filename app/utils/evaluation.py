import math
import operator

from app.utils.cdemon import demon_amalysis_path_version


def THD_DEMON(file_url):
    x, y = demon_amalysis_path_version(file_url)
    max_index, max_number = max(enumerate(y), key=operator.itemgetter(1))
    sum1 = 0
    sum2 = 0
    for i in range(1, 10):
        if (i * max_index < 500):
            sum1 += y[i * max_index] * y[i * max_index]
        else:
            sum1 += 0
    sum2 = sum1 - y[max_index] * y[max_index]
    return math.sqrt(sum2 / sum1)
