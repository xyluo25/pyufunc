# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

import contextlib
import socket


def get_host_ip():
    ip = ''
    host_name = ''
    # noinspection PyBroadException
    with contextlib.suppress(Exception):
        sc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sc.connect(('8.8.8.8', 80))
        ip = sc.getsockname()[0]
        host_name = socket.gethostname()
        sc.close()
    return ip, host_name


computer_ip, computer_name = get_host_ip()


def validate_url(url):
    import re
    return bool(re.match(r'^https?:/{2}\w.+$', url))
