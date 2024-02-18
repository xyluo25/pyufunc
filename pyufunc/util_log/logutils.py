# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from __future__ import absolute_import
from pathlib import Path
import logging
import datetime
import os
import sys
from functools import wraps

from pyutilfunc.pathio.pathutils import path2linux
from pyutilfunc.pkg_config import LOGGING_FOLDER

import datetime
import logging
import os
import smtplib
import sys
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# sys.path.append(r"../../logs/")

def log_writer1(path:str=f"../../syslogs/",info:str="",warning:str="",error:str="",debug: str="",critical: set="") -> None:
    """A function tool to track log info

    Args:
        path (str): [The path to save log file] Defaults to "current folder"
        info (str, optional): [description]. Defaults to "".
        warning (str, optional): [description]. Defaults to "".
        error (str, optional): [description]. Defaults to "".
        debug (str, optional): [description]. Defaults to "".
        critical (set, optional): [description]. Defaults to "".
    """

    if not isinstance(path, str):
        raise Exception("Invalid input, path type error...")
    if not isinstance(info, str):
        raise Exception("Invalid input, info type error...")
    if not isinstance(warning, str):
        raise Exception("Invalid input, warning type error...")
    if not isinstance(error, str):
        raise Exception("Invalid input, error type error...")
    if not isinstance(debug, str):
        raise Exception("Invalid input, debug type error...")
    if not isinstance(critical, str):
        raise Exception("Invalid input, critical type...")


    __filename = os.path.join(path,"log_%s.log"%datetime.datetime.today().strftime("%Y-%m-%d"))

    # datetime,python file name, logging level, message
    logging.basicConfig(filename=__filename,format='%(asctime)s %(name)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p',level=logging.DEBUG)

    if info:
        logging.info(info)
    if warning:
        logging.warning(warning)
    if error:
        logging.error(error)
    if debug:
        logging.debug(debug)
    if critical:
        logging.critical(critical)


def print_and_log(*args, log_level="info", **kwargs):

    kwargs_new = {}
    kwargs_unknown = []
    for key, value in kwargs.items():
        # standard print kwargs
        if key in ["sep", "end", "file", "flush"]:
            kwargs_new[key] = value
        # non-standard print kwargs
        else:
            kwargs_unknown.append(f"{key}={value}")

    print(*args, kwargs_unknown, **kwargs_new)

    if log_level.lower() == "info":
        logging.info(*args)
    elif log_level.lower() == "warning":
        logging.warning(*args)
    elif log_level.lower() == "error":
        logging.error(*args)
    elif log_level.lower() == "debug":
        logging.debug(*args)
    elif log_level.lower() == "critical":
        logging.critical(*args)
    else:
        print(" :info, invalid log level, message will not be logged...")


def log_writer(func, log_dir: str | Path = LOGGING_FOLDER) -> None:

    @wraps(func)
    def wrapper(*args, **kwargs):
        # covert log_dir to absolute path for all OSes
        log_dir_abs = path2linux(log_dir)

        # create log folder if not exist
        if not os.path.isdir(log_dir_abs):
            os.makedirs(log_dir_abs, exist_ok=True)

        # create log file using current date
        __filename = path2linux(
            os.path.join(log_dir_abs,
                         f'{datetime.datetime.now().strftime("%Y_%m_%d")}.log'))

        print("filename:", __filename)
        logging.basicConfig(filename=__filename,
                            format='%(asctime)s %(name)s %(levelname)s: %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.DEBUG)

        res = func(*args, **kwargs)

        return res

    return wrapper


# this function will track error message from log file
def log_error_tracker(path:str=f"../../syslogs/",filename_pattern:str="",level:str="ERROR") -> str:

    _filename = "log_%s.log"%datetime.datetime.today().strftime("%Y_%m_%d")

    if filename_pattern:
        _filename = filename_pattern

    filename = os.path.join(path,_filename)

    with open(filename,"r",encoding="utf-8") as f:
        message_list= []
        for message in f.readlines()[::-1]:
            if level in message:
                message_list.append(message)
    return message_list


class LogErrorAlert:
    def __init__(self,
                 log_dir: str,
                 log_level: str = "ERROR",
                 log_filename_pattern: str = "",
                 mail_text_list: list = [
                     "Hi!", "This is the dashboard error alert"],
                 mail_port: int = 587,
                 mail_user: str = 'xiaolong.ma@fii-usa.com',
                 mail_pass: str = 'Mxl1234!',
                 mail_sender: str = 'xiaolong.ma@fii-usa.com',
                 mail_receiver: str = 'xiangyong.luo@fii-usa.com',
                 mail_isTls: bool = True):
        """[summary]

        Args:
            log_dir (str): the directory that stores log files
            log_level (str, optional): five types of levels: INFO,WARNING,DEBUG,ERROR,CRITICAL. Defaults to "ERROR".
            log_filename_pattern (str, optional): the log filename pattern,eg: log_2022_02_10.log. Defaults to "".
            mail_text_list (list, optional): the mail messages store in list format.each element represent one new line in content area. Defaults to ["Hi!","This is the dashboard error alert"].
            mail_port (int, optional): Defaults to 587.
            mail_user (str, optional): Defaults to 'xiaolong.ma@fii-usa.com'.
            mail_pass (str, optional): Defaults to 'Mxl1234!'.
            mail_sender (str, optional): Defaults to 'xiaolong.ma@fii-usa.com'.
            mail_receiver (str, optional): Defaults to 'xiangyong.luo@fii-usa.com'.
            mail_isTls (bool, optional): Defaults to True.
        """
        self.log_dir = log_dir
        self.log_filename_pattern = log_filename_pattern
        self.log_level = log_level
        self.mail_text_list = mail_text_list
        self.mail_port = mail_port
        self.mail_user = mail_user
        self.mail_pass = mail_pass
        self.mail_sender = mail_sender
        self.mail_receiver = mail_receiver
        self.mail_isTls = mail_isTls

    def error_tracker(self):
        _filename = "log_%s.log" % datetime.datetime.today().strftime("%Y_%m_%d")

        if self.log_filename_pattern:
            _filename = self.log_filename_pattern

        filename = os.path.join(self.log_dir, _filename)

        with open(filename, "r", encoding="utf-8") as f:
            for message in f.readlines()[::-1]:
                if self.log_level in message:
                    self.mail_text_list.append(message)

    def send_alert(self):
        mail_host = 'smtp.office365.com'
        try:
            smtp_obj = smtplib.SMTP(mail_host, self.mail_port)
            if self.mail_isTls:
                smtp_obj.starttls()
            smtp_obj.login(self.mail_user, self.mail_pass)
            #text part
            self.error_tracker()
            message = "\n".join(self.mail_text_list)

            # the default length is 2, and more errors occur if len greater than 3
            if len(message) >= 3:
                part1 = MIMEText(message, 'plain')

                msg = MIMEMultipart('alternative')
                msg['Subject'] = 'GL10 Code Alert'
                msg['From'] = self.mail_sender
                msg['To'] = self.mail_receiver
                msg.attach(part1)

                smtp_obj.sendmail(self.mail_sender,
                                  self.mail_receiver, msg.as_string())
                smtp_obj.quit()
                print('Successfully send the email')

        except Exception as e:
            log_writer(error=str(e))
            print("error", e)
            exit(0)
