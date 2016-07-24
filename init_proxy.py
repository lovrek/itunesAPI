import time
import random


def curl():
    proxiesIP = ['192.161.163.180:3128',
                 '173.208.91.237:3128',
                 '173.234.226.166:3128',
                 '173.234.226.172:3128',
                 '173.208.91.115:3128',
                 '50.31.10.1:3128',
                 '173.208.91.231:3128',
                 '50.31.10.106:3128',
                 '192.161.163.137:3128',
                 '173.208.91.109:3128']

    proxyauth = "60902:9rrWYRhBA"

    user_agents = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
                   'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.9) Gecko/20100508 SeaMonkey/2.0.4',
                   'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
                   'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; da-dk) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1']

    header = {}
    header['Accept'] = "text/xml,application/xml,application/xhtml+xml,application/json,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5"
    header['Cache-Control'] = "max-age=0"
    header['Connection'] = "keep-alive"
    header['Keep-Alive'] = 300
    header['Accept-Charset'] = "ISO-8859-1,utf-8;q=0.7,*;q=0.7"
    header['Accept-Language'] = "en-us,en;q=0.5"
    header['Pragma'] = ""
    header['User-Agent'] = user_agents[random.randint(0,3)]

    proxy = {'http': 'http://' + proxyauth + '@' + proxiesIP[random.randint(0, 9)]}

    time.sleep(random.randint(1, 5)/10)         #delay 100ms - 500 ms

    return {'proxy': proxy, 'header': header}