# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################
from __future__ import absolute_import
import os
import socket

computer_name = socket.gethostname()
computer_ip = socket.gethostbyname(computer_name)

# ############## Package Configurations ############## #
pkg_version = "0.3.2"
pkg_name = "pyufunc"
pkg_author = "Mr. Xiangyong Luo, Dr. Xuesong Simon Zhou"
pkg_email = "luoxiangyong01@gmail.com, xzhou74@asu.edu"

__all__ = [
    "pkg_version",
    "pkg_name",
    "pkg_author",
    "pkg_email",
    "config_FUNC_KEYWORD",
    "config_logging",
    "config_datetime_fmt",
    "config_email",
    "config_gmns",
    "config_color",
]

# ############### Function Keywords Configuration ############### #
config_FUNC_KEYWORD = {
    "non-keywords": [],
    "show"        : [],
    "get"         : [],
    "generate"    : [],
    "create"      : [],
    "find"        : [],
    "calc"        : [],
    "run"         : [],
    "group"       : [],
    "check"       : [],
    "validate"    : [],
    "list"        : [],
    "img"         : [],
    "split"       : [],
    "fmt"         : [],
    "cvt"         : [],
    "is"          : [],
    "proj"        : [],
    "github"      : [],
    "pypi"        : [],
    "error"       : [],
    "algo"        : [],
    "gmns"        : [],
}

# ############## Logging Configurations ############## #
config_logging = {
    # log name
    "log_name": {},

    # logging
    "log_level": "WARNING",

    # log folder
    "log_folder": "logs",

    # default log format
    "log_fmt": {
        1: '%(asctime)s - %(name)s - %(filename)s - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s',

        2: '%(asctime)s - %(name)s - [ File "%(pathname)s", line %(lineno)d, in %(funcName)s ] - %(levelname)s - %(message)s',

        3: '%(asctime)s - %(name)s - "%(filename)s" - %(funcName)s - %(lineno)d - %(levelname)s - %(message)s - File "%(pathname)s", line %(lineno)d ',

        4: '%(asctime)s - %(name)s - "%(pathname)s:%(lineno)d" - %(funcName)s - %(levelname)s - %(message)s',  # the default log format

        5: '%(name)s - %(asctime)-15s - %(filename)s - %(lineno)d - %(levelname)s: %(message)s',

        6: '%(asctime)s - %(name)s - "%(filename)s:%(lineno)d" - %(levelname)s - %(message)s',

        7: '[p%(process)d_t%(thread)d] %(asctime)s - %(name)s - "%(pathname)s:%(lineno)d" - %(funcName)s - %(levelname)s - %(message)s',  # include process and thread

        8: '[p%(process)d_t%(thread)d] %(asctime)s - %(name)s - "%(filename)s:%(lineno)d" - %(levelname)s - %(message)s',

        9: f'%(asctime)s-({computer_ip},{computer_name})-[p%(process)d_t%(thread)d] - %(name)s - "%(filename)s:%(lineno)d" - %(funcName)s - %(levelname)s - %(message)s',
    },

    # default log date format
    "log_datefmt": "%Y-%m-%d %H:%M:%S",

    # default log attributes
    "log_attrs": (
        "args",
        "asctime",
        "created",
        "exc_info",
        "exc_text",
        "filename",
        "funcName",
        "levelname",
        "levelno",
        "lineno",
        "module",
        "msecs",
        "message",
        "msg",
        "name",
        "pathname",
        "process",
        "processName",
        "relativeCreated",
        "stack_info",
        "thread",
        "threadName"),

}

# ############### Date Time Format Configuration ############### #
config_datetime_fmt = {

    0: "%Y-%m-%d",  # 0 "YYYY-MM-DD", 2023-07-09
    1: "%Y-%m-%d %H:%M:%S",  # 1 "YYYY-MM-DD HH:MM:SS", 2023-07-09 11:11:11
    2 : "%Y-%m-%d %H:%M:%S.%f",
    # 2 "YYYY-MM-DD HH:MM:SS.MS", 2023-07-09 11:11:11.123456

    3: "%Y/%m/%d",  # 3 "YYYY/MM/DD", 2023/07/09
    4: "%Y/%m/%d %H:%M:%S",  # 4 "YYYY/MM/DD HH:MM:SS", 2023/07/09 11:11:11
    5: "%Y/%m/%d %H:%M:%S.%f",
    # 5 "YYYY/MM/DD HH:MM:SS.MS", 2023/07/09 11:11:11.123456

    6: "%m/%d/%Y",  # 6 "MM/DD/YYYY", 07/09/2023
    7: "%m/%d/%Y %H:%M:%S",  # 7 "MM/DD/YYYY HH:MM:SS", 07/09/2023 11:11:11
    8 : "%m/%d/%Y %H:%M:%S.%f",
    # 8 "MM/DD/YYYY HH:MM:SS.MS", 07/09/2023 11:11:11.123456

    9: "%d/%m/%Y",  # 9 "DD/MM/YYYY", 09/07/2023
    10: "%d/%m/%Y %H:%M:%S",  # 10 "DD/MM/YYYY HH:MM:SS", 09/07/2023 11:11:11
    11 : "%d/%m/%Y %H:%M:%S.%f",
    # 11 "DD/MM/YYYY HH:MM:SS.MS", 09/07/2023 11:11:11.123456

    12 : "%H:%M:%S",  # "HH:MM:SS", 11:11:11
    13 : "%H:%M:%S.%f",  # "HH:MM:SS.MS", 11:11:11.123456

    14: "%m-%d-%Y",  # "MM-DD-YYYY", 07-09-2023
    15: "%m-%d-%Y %H:%M:%S",  # "MM-DD-YYYY HH:MM:SS", 07-09-2023 11:11:11
    16: "%m-%d-%Y %H:%M:%S.%f",  # "MM-DD-YYYY HH:MM:SS.MS", 07-09-2023 11:11:11.123456

    17: "%d-%m-%Y",  # "DD-MM-YYYY", 09-07-2023
    18: "%d-%m-%Y %H:%M:%S",  # "DD-MM-YYYY HH:MM:SS", 09-07-2023 11:11:11
    19: "%d-%m-%Y %H:%M:%S.%f",  # "DD-MM-YYYY HH:MM:SS.MS", 09-07-2023 11:11:11.123456

    29: "%Y-%m",  # "YYYY-MM", 2023-07
    30: "%Y/%m",  # "YYYY/MM", 2023/07
    31: "%m/%Y",  # "MM/YYYY", 07/2023
    32: "%m-%Y",  # "MM-YYYY", 07-2023

    33: "%Y-%m-%d %Z",  # "YYYY-MM-DD %Z", 2023-07-09 UTC
    34: "%Y-%m-%d %H:%M:%S %Z",  # "YYYY-MM-DD HH:MM:SS %Z", 2023-07-09 11:11:11 UTC
    35: "%Y/%m/%d %Z",  # "YYYY/MM/DD %Z", 23/07/09 UTC
    36: "%Y/%m/%d %H:%M:%S %Z",  # "YYYY/MM/DD HH:MM:SS %Z", 23/07/09 11:11:11 UTC

    "default": "%Y-%m-%d",
}

# ############### Email Configuration ############### #
config_email = {
    'gmail.com': {
        'smtp': ('smtp.gmail.com', 587),
        'pop3': ('pop.gmail.com', 995)},
    'office365.com': {
        'smtp': ('smtp.office365.com', 587),
        'pop3': ('outlook.office365.com', 995)},
    'outlook.com': {
        'smtp': ('smtp-mail.outlook.com', 587),
        'pop3': ('outlook.office365.com', 995)},
    'yahoo.com': {
        'smtp': ('smtp.mail.yahoo.com', 587),
        'pop3': ('pop.mail.yahoo.com', 995)},
    'hotmail.com': {
        'smtp': ('smtp-mail.outlook.com', 587),
        'pop3': ('outlook.office365.com', 995)},
    'aol.com': {
        'smtp': ('smtp.aol.com', 587),
        'pop3': ('pop.aol.com', 995)},
    'protonmail.com': {
        'smtp': ('smtp.protonmail.com', 465),
        'pop3': None},  # ProtonMail does not offer POP3 access
    'zoho.com': {
        'smtp': ('smtp.zoho.com', 587),
        'pop3': ('pop.zoho.com', 995)},
    'fastmail.com': {
        'smtp': ('smtp.fastmail.com', 587),
        'pop3': ('mail.messagingengine.com', 995)},
    'qq.com': {
        'smtp': ('smtp.qq.com', 587),
        'pop3': ('pop.qq.com', 995)},
    '163.com': {
        'smtp': ('smtp.163.com', 465),
        'pop3': ('pop.163.com', 995)},
    'asu.edu': {
        'smtp': ('smtp.gmail.edu', 587),
        'pop3': ('pop.gmail.edu', 995)},
}

# ############### GMNS: General Modeling Network Specification configuration #
config_gmns = {
    # specify required fields for node.csv and poi.csv and zone.csv (optional)
    "node_fields": ["node_id", "x_coord", "y_coord",
                    "activity_type", "is_boundary", "poi_id", "ctrl_type"],
    "poi_fields": ["poi_id", "building", "centroid", "area", "geometry"],
    "link_fields": ["link_id", "name", "from_node_id", "to_node_id", "dir_flag",
                    "length", "lanes", "free_speed", "capacity", "link_type", "link_type_name",
                    "geometry", "allowed_uses", "from_biway"],
    "zone_geometry_fields": ["zone_id", "geometry"],
    "zone_centroid_fields": ["zone_id", "x_coord", "y_coord"],
    "data_chunk_size": 1000,  # number of rows to read in each chunk
    "set_cpu_cores": os.cpu_count(),  # number of cpu cores to use
}

# ############### Color initialization ############### #
config_color = {
    "ACCENT"        : ('\x1b[01m', '\x1b[01m'),
    "BLACK"         : ('\x1b[30m', '\x1b[40m'),
    "RED"           : ('\x1b[31m', '\x1b[41m'),
    "GREEN"         : ('\x1b[32m', '\x1b[42m'),
    "YELLOW"        : ('\x1b[33m', '\x1b[43m'),
    "BLUE"          : ('\x1b[34m', '\x1b[44m'),
    "MAGENTA"       : ('\x1b[35m', '\x1b[45m'),
    "CYAN"          : ('\x1b[36m', '\x1b[46m'),
    "WHITE"         : ('\x1b[37m', '\x1b[47m'),
    "DEFAULT"       : ('\x1b[39m', '\x1b[49m'),
    "GRAY"          : ('\x1b[90m', '\x1b[100m'),
    "BRIGHT_RED"    : ('\x1b[91m', '\x1b[101m'),
    "BRIGHT_GREEN"  : ('\x1b[92m', '\x1b[102m'),
    "BRIGHT_YELLOW" : ('\x1b[93m', '\x1b[103m'),
    "BRIGHT_BLUE"   : ('\x1b[94m', '\x1b[104m'),
    "BRIGHT_MAGENTA": ('\x1b[95m', '\x1b[105m'),
    "BRIGHT_CYAN"   : ('\x1b[96m', '\x1b[106m'),
    "BRIGHT_WHITE"  : ('\x1b[97m', '\x1b[107m'),
    # "END"           : ('\x1b[0m',  '\x1b[0m'),
}
