# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


def get_file_size(file_path):
    import os
    return os.path.getsize(file_path)


def write_yaml_file(func=None, *, log_dir: str | Path = LOGGING_FOLDER, ):
    import yaml
    with open(file_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)