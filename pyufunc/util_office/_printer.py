# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

import socket


def printer_file(fname_lst: list, host: str, port: int = 9100) -> None:
    """Send data to a network printer.

    Args:
        fname_lst (list): a list of files or binary data
        host (str): the host of the printer
        port (int, optional): printer port. Defaults to 9100.

    Raises:
        Exception: Invalid inputs...
        Exception: Error connecting to printer: {e}

    Example:
        >>> import pyufunc as pf
        >>> pf.network_printer(["test.txt"], "printer_host_name")

    Returns:
        None: None
    """

    try:
        net_printer = socket.socket(socket.AF_INF, socket.SOCK_STREAM)
        net_printer.connect((host, port))
        data_binary = []

        if not fname_lst:
            raise Exception("Invalid inputs...")

        if isinstance(fname_lst[0], bytes):
            data_binary = fname_lst

        if isinstance(fname_lst[0], str):
            with open(fname_lst, "rb") as f:
                data_binary = f.read()

        if data_binary:
            for data in data_binary:
                net_printer.send(data)
            net_printer.close()
        else:
            raise Exception("Invalid inputs...")
    except Exception as e:
        print("Error connecting to printer: ", e)
    return None
