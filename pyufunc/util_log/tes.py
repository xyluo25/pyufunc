# -*- coding:utf-8 -*-
##############################################################
# Created Date: Wednesday, May 15th 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


from loga import LogDecorator

# all setup values are optional
logaa = LogDecorator(
    proj_name="tester",  # name of program logging the message
    do_print=True,  # print each log to console
    do_write=True,  # write each log to file
    logfile="mylog.txt",  # custom path to logfile
    truncation=1000,  # longest possible value in extra data
    private_data={"password"},  # set of sensitive args/kwargs
)


@logaa
class Multiplier:
    def __init__(self, base):
        self.base = base

    def multiply(self, n, password):

        self.authenticated = self._do_authentication(password)
        if not self.authenticated:
            raise ValueError("Not authenticated!")
        return self.base * n

    @logaa.ignore
    def _do_authentication(self, password):
        """Not exactly Fort Knox"""
        return password == "tOpSeCrEt"


mult = Multiplier(50)
result = mult.multiply(50, "tOpSeCrEtt")
assert result == 2500  # True
