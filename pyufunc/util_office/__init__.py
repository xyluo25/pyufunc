# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from ._email import is_valid_email, send_email
from ._printer import printer_file

__all__ = [

    # .email
    "is_valid_email",
    "send_email",

    # .printer
    "printer_file",
]