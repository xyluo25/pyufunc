import atexit
import contextlib
import queue
import threading
import typing
from pathlib import Path
import time
import os


def build_current_date_str():
    return time.strftime('%Y-%m-%d')


class FileWriter:
    _lock = threading.RLock()

    def __init__(self, file_name: str, log_path=os.getcwd(), max_bytes=1000 * 1000 * 1000, back_count=10):
        self._max_bytes = max_bytes
        self._back_count = back_count
        self.need_write_2_file = bool(file_name)
        if self.need_write_2_file:
            self._file_name = file_name
            self.log_path = log_path
            if not Path(self.log_path).exists():
                print(f'Create log folder {log_path}')
                Path(self.log_path).mkdir(exist_ok=True)
            self._open_file()
            self._last_write_ts = 0
            self._last_del_old_files_ts = 0

    @property
    def file_path(self):
        f_list = list(Path(self.log_path).glob(f'????-??-??.????.{self._file_name}'))
        sn_list = []
        for f in f_list:
            if f'{build_current_date_str()}.' in f.name:
                sn = f.name.split('.')[1]
                sn_list.append(sn)
        if not sn_list:
            return Path(self.log_path) / Path(f'{build_current_date_str()}.0001.{self._file_name}')
        sn_max = max(sn_list)
        if (
            Path(self.log_path) / Path(f'{build_current_date_str()}.{sn_max}.{self._file_name}')
        ).stat().st_size <= self._max_bytes:
            return Path(self.log_path) / Path(f'{build_current_date_str()}.{sn_max}.{self._file_name}')
        new_sn_int = int(sn_max) + 1
        new_sn_str = str(new_sn_int).zfill(4)
        return Path(self.log_path) / Path(f'{build_current_date_str()}.{new_sn_str}.{self._file_name}')

    def _open_file(self):
        self._f = open(self.file_path, encoding='utf8', mode='a')

    def _close_file(self):
        self._f.close()

    def write_2_file(self, msg):
        if self.need_write_2_file:
            with self._lock:
                now_ts = time.time()
                if now_ts - self._last_write_ts > 10:
                    self._last_write_ts = time.time()
                    self._close_file()
                    self._open_file()
                self._f.write(msg)
                self._f.flush()
                if now_ts - self._last_del_old_files_ts > 30:
                    self._last_del_old_files_ts = time.time()
                    self._delete_old_files()

    def _delete_old_files(self):
        f_list = list(Path(self.log_path).glob(f'????-??-??.????.{self._file_name}'))
        # f_list.sort(key=lambda f:f.stat().st_mtime,reverse=True)
        f_list.sort(key=lambda f: f.name, reverse=True)
        for f in f_list[self._back_count:]:
            with contextlib.suppress(FileNotFoundError, PermissionError):
                # print(f'删除 {f} ') # 这里不能print， stdout写入文件，写入文件时候print，死循环
                f.unlink()


class BulkFileWriter:
    _lock = threading.Lock()

    filename__queue_map = {}
    filename__options_map = {}
    filename__file_writer_map = {}

    _get_queue_lock = threading.Lock()

    _has_start_bulk_write = False

    @classmethod
    def _get_queue(cls, file_name):
        if file_name not in cls.filename__queue_map:
            cls.filename__queue_map[file_name] = queue.SimpleQueue()
        return cls.filename__queue_map[file_name]

    @classmethod
    def _get_file_writer(cls, file_name):
        if file_name not in cls.filename__file_writer_map:
            fw = FileWriter(**cls.filename__options_map[file_name])
            cls.filename__file_writer_map[file_name] = fw
        return cls.filename__file_writer_map[file_name]

    def __init__(self, file_name: typing.Optional[str],
                 log_path=os.getcwd(),
                 max_bytes=1000 * 1000 * 1000,
                 back_count=10):
        self.need_write_2_file = bool(file_name)
        self._file_name_key = (log_path, file_name)
        if file_name:
            self.__class__.filename__options_map[self._file_name_key] = {
                'file_name': file_name,
                'log_path': log_path,
                'max_bytes': max_bytes,
                'back_count': back_count,
            }
            self.start_bulk_write()

    def write_2_file(self, msg):
        if self.need_write_2_file:
            with self._lock:
                self._get_queue(self._file_name_key).put(msg)

    @classmethod
    def _bulk_real_write(cls):
        with cls._lock:
            for _file_name, queue in cls.filename__queue_map.items():
                msg_str_all = ''
                while not queue.empty():
                    msg_str_all += str(queue.get())
                if msg_str_all:
                    cls._get_file_writer(_file_name).write_2_file(msg_str_all)

    @classmethod
    def _when_exit(cls):
        # print('结束')
        return cls._bulk_real_write()

    @classmethod
    def start_bulk_write(cls):
        def _bulk_write():
            while 1:
                cls._bulk_real_write()
                time.sleep(0.1)

        if not cls._has_start_bulk_write:
            cls._has_start_bulk_write = True
            threading.Thread(target=_bulk_write, daemon=True).start()


atexit.register(BulkFileWriter._when_exit)

OsFileWriter = FileWriter if os.name == 'posix' else BulkFileWriter
