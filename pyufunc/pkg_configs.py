# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

import os
from pyufunc.util_pathio._path import path2linux


# ############## Package Configurations ############## #
pkg_version = "0.2.3"
pkg_name = "pyufunc"
pkg_author = "Mr. Xiangyong Luo, Dr. Xuesong Simon Zhou"
pkg_email = "luoxiangyong01@gmail.com, xzhou74@asu.edu"

# ############## Logging Configurations ############## #
# system logging
IS_LOG = True

# logging default folder
LOGGING_FOLDER = path2linux(os.path.join(os.getcwd(), "syslogs"))

# ############### Date Time Format Configuration ############### #
pkg_dt_fmt_seq = {
    # "YYYY-MM-DD HH:MM:SS", 2023-07-09 11:11:11
    0 : "%Y-%m-%d %H:%M:%S",

    # "YYYY-MM-DD HH:MM:SS.MS", 2023-07-09 11:11:11.123456
    1 : "%Y-%m-%d %H:%M:%S.%f",

    # "MM/DD/YYYY HH:MM:SS", 07/09/2023 11:11:11
    2 : "%m/%d/%Y %H:%M:%S",
    # "MM/DD/YYYY HH:MM:SS.MS", 07/09/2023 11:11:11.123456
    3 : "%m/%d/%Y %H:%M:%S.%f",

    # "DD/MM/YYYY HH:MM:SS", 09/07/2023 11:11:11
    4 : "%d/%m/%Y %H:%M:%S",
    # "DD/MM/YYYY HH:MM:SS.MS", 09/07/2023 11:11:11.123456
    5 : "%d/%m/%Y %H:%M:%S.%f",

    6 : "%Y-%m-%d",  # "YYYY-MM-DD", 2023-07-09
    7 : "%m/%d/%Y",  # "MM/DD/YYYY", 07/09/2023
    8 : "%d/%m/%Y",  # "DD/MM/YYYY", 09/07/2023

    9 : "%H:%M:%S",  # "HH:MM:SS", 11:11:11
    10 : "%H:%M:%S.%f",  # "HH:MM:SS.MS", 11:11:11.123456
}

# ############### Function Keywords Configuration ############### #
ufunc_keywords = {
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
    "split"       : [],
    "fmt"         : [],
    "cvt"         : [],
    "is"          : [],
    "proj"        : [],
    "github"      : [],
    "pypi"        : []

}


# ############### Email Configuration ############### #
email_config = {
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
        # ProtonMail does not offer POP3 access
        'pop3': None},
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
