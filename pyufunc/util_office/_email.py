# -*- coding:utf-8 -*-
##############################################################
# Created Date: Monday, March 11th 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

import os
import re
from typing import Union
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email import encoders

# For guessing MIME type based on file name extension
import mimetypes

from pyufunc.pkg_configs import email_config
from pyufunc.util_pathio._path import path2linux


def is_valid_email(email: str) -> bool:
    """check if the email is valid

    Args:
        email (str): email address, eg. luoxiangyong01@gmail.com

    Returns:
        bool: True if the email is valid, False otherwise

    Examples:
        >>> from pyufunc import is_valid_email
        >>> is_valid_email("luoxiangyong01@gamil.com")
        True
        >>> is_valid_email("luoxiangyong01")
        False

    """

    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))


def send_email(send_from: str,
               send_to: Union[str, list],
               subject: str,
               message: str,
               smtp_user: str,
               smtp_password: str,
               file_path: Union[str, list] = [],
               cc: Union[str, list] = [],
               bcc: Union[str, list] = [],
               **kwargs) -> bool:
    """send email with attachments

    Args:
        send_from (str): email address of the sender
        send_to (Union[str, list]): email address of the receiver, can be a list of email addresses
        subject (str): email subject
        message (str): the email body
        smtp_user (str): user name of the smtp server, normally the same as the email address
        smtp_password (str): password of the smtp server, if you use gmail, you need to generate an app password
        file_path (Union[str, list], optional): _description_. Defaults to [].
        cc (Union[str, list], optional): cc'd email. Defaults to [].
        bcc (Union[str, list], optional): bcc'd email. Defaults to [].

    Raises:
        ValueError: Invalid email address:
        ValueError: send_to should be a list or a string of email addresses
        ValueError: Invalid email address:
        ValueError: file_path should be a list of file paths
        ValueError: Invalid file:
        ValueError: Unknown email provider:

    Note:
        - User can add message_type = "html" in the kwargs. If message_type is "html", the message will be sent as html format. eg. message_type = "html", message = "<h1>hello world</h1>"
        - User can add verbose = True in the kwargs. If verbose is True, the function will print the email sending status.
        - If you are using gmail, you need to generate an app password for the smtp_password: https://support.google.com/accounts/answer/185833?hl=en


    Returns:
        bool: True if the email is sent successfully, False otherwise
    """

    # TDD, Test Driven Development, check inputs
    if not is_valid_email(send_from):
        raise ValueError(f"Invalid email address: {send_from}")

    # format the send_to to a list
    if isinstance(send_to, str):
        send_to = [send_to]

    # check if send_to is a list
    if not isinstance(send_to, list):
        raise ValueError("send_to should be a list or a string of email addresses")

    # check if all email addresses are valid
    if not all(is_valid_email(email) for email in send_to):
        raise ValueError(f"Invalid email address: {send_to}")

    # check if file_path is a string
    if isinstance(file_path, str):
        file_path = [file_path]

    if file_path and not isinstance(file_path, list):
        raise ValueError("file_path should be a list of file paths")

    # check each file path is valid file
    if file_path:
        # convert the file path to linux format
        file_path = [path2linux(path) for path in file_path]
        for path in file_path:
            if not os.path.isfile(path):
                raise ValueError(f"Invalid file: {path}")

    # format the cc to a list
    if isinstance(cc, str):
        cc = [cc]
    if cc and not isinstance(cc, list):
        raise ValueError("cc should be a list or a string of email addresses")
    if cc and not all(is_valid_email(email) for email in cc):
        raise ValueError(f"Invalid email address: {cc}")

    # format the bcc to a list
    if isinstance(bcc, str):
        bcc = [bcc]
    if bcc and not isinstance(bcc, list):
        raise ValueError("bcc should be a list or a string of email addresses")
    if bcc and not all(is_valid_email(email) for email in bcc):
        raise ValueError(f"Invalid email address: {bcc}")

    # get email configurations from send_from
    email_from_domain = send_from.split("@")[-1]
    email_config_domain = email_config.get(email_from_domain.lower())
    if not email_config_domain:
        raise ValueError(f"Unknown email provider: {email_from_domain}")

    smtp_server, smtp_port = email_config_domain.get("smtp")

    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = "; ".join(send_to)
    msg['Subject'] = subject
    msg['Cc'] = "; ".join(cc)
    msg['Bcc'] = "; ".join(bcc)

    # Attach the email body
    if kwargs.get("message_type") == "html":
        msg.attach(MIMEText(message, 'html'))
    else:
        msg.attach(MIMEText(message, 'plain'))

    # Load the attachment
    def load_attachment(filename: str) -> MIMEBase:

        # Guess the content type based on the file's extension.  Encoding will be
        # ignored, although we should check for simple things like gzip'd or
        # compressed files.

        ctype, encoding = mimetypes.guess_type(filename)

        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed), so
            # use a generic bag-of-bits type.
            ctype = 'application/octet-stream'

        maintype, subtype = ctype.split('/', 1)

        # Check the file type and load the attachment
        if maintype == 'text':
            with open(path) as fp:
                # Note: we should handle calculating the charset
                part = MIMEText(fp.read(), _subtype=subtype)
        elif maintype == 'image':
            with open(path, 'rb') as fp:
                part = MIMEImage(fp.read(), _subtype=subtype)
        elif maintype == 'audio':
            with open(path, 'rb') as fp:
                part = MIMEAudio(fp.read(), _subtype=subtype)
        else:
            with open(path, 'rb') as fp:
                part = MIMEBase(maintype, subtype)
                part.set_payload(fp.read())
            # Encode the payload using Base64
            encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header('Content-Disposition', 'attachment', filename=filename.split("/")[-1])

        return part

    # Open the file to be attached
    if file_path:
        for path in file_path:
            part = load_attachment(path)
            msg.attach(part)

    try:
        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(smtp_user, smtp_password)
        text = msg.as_string()
        server.sendmail(send_from, send_to, text)
        server.quit()

        # print the email description if verbose is True
        verbose = kwargs.get("verbose")
        if verbose:
            print(f"Email description: \nFrom: {send_from} \nTo: {send_to}  \nSubject: {subject}")
            print(f"Message: {message}")
            if file_path:
                print(f"Attachments: {file_path}")

        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
