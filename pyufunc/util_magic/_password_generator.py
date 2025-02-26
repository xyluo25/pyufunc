# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, February 4th 2024
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

import secrets
import string


def generate_password(pwd_len: int = 15, lowercase: bool = True,
                      uppercase: bool = True, digit: bool = True,
                      special_char: bool = True,
                      config: dict = {"num_lowercase": 1,
                                      "num_uppercase": 1,
                                      "num_digit": 1,
                                      "num_special_char": 1}) -> str:
    """Generate a random password with given length and character types.

    Location:
        The function defined in pyufunc/util_common/_password_generator.py.

    Args:
        pwd_len (int, optional): total length of password. Defaults to 15.
        lowercase (bool, optional): whether to include lowercase in password. Defaults to True.
        uppercase (bool, optional): whether to include uppercase in password. Defaults to True.
        digit (bool, optional): whether to include digits in password. Defaults to True.
        special_char (bool, optional): whether to include special character in password. Defaults to True.
        config (_type_, optional): Defaults to {"num_lowercase": 1, "num_uppercase": 1,
                                                "num_digit": 1, "num_special_char": 1}.

    Raises:
        ValueError: if the total length of password in config is longer than the password length.

    Returns:
        str: the generated password.

    Examples:
        >>> generate_password()
        '5#4X6v8&9^0%1$2'
    """

    # check total config length
    config_length = sum(config[key] for key in config if key.startswith("num_"))

    if config_length > pwd_len:
        raise ValueError("The total length of password in config is longer than the password length.")

    # create random number of characters for each type with length on config
    lowercase = [secrets.choice(string.ascii_lowercase) for _ in range(config["num_lowercase"])]
    uppercase = [secrets.choice(string.ascii_uppercase) for _ in range(config["num_uppercase"])]
    digit = [secrets.choice(string.digits) for _ in range(config["num_digit"])]
    special_char = [secrets.choice(string.punctuation) for _ in range(config["num_special_char"])]

    all_chars = string.ascii_letters + string.digits + string.punctuation
    remaining_length = pwd_len - config_length
    password_list = lowercase + uppercase + digit + special_char + \
        [''.join(secrets.choice(all_chars) for _ in range(remaining_length))]

    # password_list = list(password)
    secrets.SystemRandom().shuffle(password_list)
    return ''.join(password_list)
