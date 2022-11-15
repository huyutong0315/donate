from urllib.request import urlopen

def get_my_ip(): 
    my_ip = urlopen('http://ip.42.pl/raw').read().decode('utf-8')
    return my_ip
# if __name__ == '__main__':
#   GetOuterIP()