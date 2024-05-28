
import logging
import json
import re
import traceback
import importlib
from datetime import date, datetime, time, timezone
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from inspect import istraceback
from collections import OrderedDict

from pyufunc.pkg_configs import config_logging

# code adopted from: https://github.com/madzak/python-json-logger and modified


def merge_record_extra(record: logging.LogRecord,
                       target: dict,
                       reserved: Union[dict, list],
                       rename_fields: dict[str, str] = None) -> dict:

    """Merge extra attributes from LogRecord object into target dictionary

    Args:
        record (logging.LogRecord): LogRecord object
        target (Dict): target dictionary
        reserved (Union[Dict, List]): reserved keys to skip
        rename_fields (Dict[str, str]): Rename field names in the output (Rename levelname to log.level: {'levelname': 'log.level'}). Defaults to None.
    """

    if rename_fields is None:
        rename_fields = {}
    for key, value in record.__dict__.items():
        # this allows to have numeric keys
        if key not in reserved and not (
            hasattr(key, "startswith") and key.startswith("_")
        ):
            target[rename_fields.get(key, key)] = value
    return target


class JsonEncoder(json.JSONEncoder):
    """
    A custom encoder extending the default JSONEncoder
    """

    def default(self, obj):
        if isinstance(obj, (date, datetime, time)):
            return self.format_datetime_obj(obj)

        elif istraceback(obj):
            return "".join(traceback.format_tb(obj)).strip()

        elif type(obj) == Exception or isinstance(obj, Exception) or type(obj) == type:
            return str(obj)

        try:
            return super(JsonEncoder, self).default(obj)

        except TypeError:
            try:
                return str(obj)

            except Exception:
                return None

    def format_datetime_obj(self, obj):
        return obj.isoformat()


class JsonFormatter(logging.Formatter):
    """
    A custom formatter to format logging records as json strings.
    Extra values will be formatted as str() if not supported by
    json default encoder
    """

    def __init__(self,
                 *args: Any,
                 json_default: Union[Callable, str] = None,
                 json_encoder: Union[Callable, str] = None,
                 json_serializer: Union[Callable, str] = json.dumps,
                 json_indent: Union[int, str] = None,
                 json_ensure_ascii: bool = True,
                 prefix: str = "",
                 rename_fields: Optional[dict] = None,
                 static_fields: Optional[dict] = None,
                 reserved_attrs: Tuple[str, ...] = config_logging["log_attrs"],
                 timestamp: Union[bool, str] = False,
                 **kwargs: Any):  # sourcery skip: dict-assign-update-to-union
        """Initializes the formatter with the specified parameters.

        Args:
            json_default (Union[Callable, str]): a function for encoding non-standard objects as outlined in https://docs.python.org/3/library/json.html. Defaults to None.
            json_encoder (Union[Callable, str]): optional custom encoder. Defaults to None.
            json_serializer (Union[Callable, str]): a :meth:`json.dumps`-compatible callable that will be used to serialize the log record. Defaults to json.dumps.
            json_indent (Union[int, str]): indent parameter for json.dumps. Defaults to None.
            json_ensure_ascii (bool): ensure_ascii parameter for json.dumps. Defaults to True.
            prefix (str): an optional string prefix added at the beginning of the formatted string. Defaults to "".
            rename_fields (Optional[dict]): an optional dict, used to rename field names in the output. Rename message to @message: {'message': '@message'}. Defaults to None.
            static_fields (Optional[dict]): an optional dict, used to add fields with static values to all logs. Defaults to None.
            reserved_attrs (Tuple[str]): an optional list of fields that will be skipped when outputting json log record. Defaults to config_logging["log_attrs"].
            timestamp (Union[bool, str]): an optional string/boolean field to add a timestamp when outputting the json log record. If string is passed, timestamp will be added to log record using string as key. If True boolean is passed, timestamp key will be "timestamp". Defaults to False.
        """

        self.json_default = self._str_to_fn(json_default)
        self.json_encoder = self._str_to_fn(json_encoder)
        self.json_serializer = self._str_to_fn(json_serializer)
        self.json_indent = json_indent
        self.json_ensure_ascii = json_ensure_ascii
        self.prefix = prefix
        self.rename_fields = rename_fields or {}
        self.static_fields = static_fields or {}
        self.reserved_attrs = dict(zip(reserved_attrs, reserved_attrs))
        self.timestamp = timestamp

        # super(JsonFormatter, self).__init__(*args, **kwargs)
        logging.Formatter.__init__(self, *args, **kwargs)
        if not self.json_encoder and not self.json_default:
            self.json_encoder = JsonEncoder

        self._required_fields = self.parse()
        self._skip_fields = dict(
            zip(self._required_fields, self._required_fields))
        self._skip_fields.update(self.reserved_attrs)

    def _str_to_fn(self, fn_as_str):
        """
        If the argument is not a string, return whatever was passed in.
        Parses a string such as package.module.function, imports the module
        and returns the function.

        :param fn_as_str: The string to parse. If not a string, return it.
        """
        if not isinstance(fn_as_str, str):
            return fn_as_str

        path, _, function = fn_as_str.rpartition(".")
        module = importlib.import_module(path)
        return getattr(module, function)

    def parse(self) -> List[str]:
        """
        Parses format string looking for substitutions

        This method is responsible for returning a list of fields (as strings)
        to include in all log messages.
        """
        if isinstance(self._style, logging.StringTemplateStyle):
            formatter_style_pattern = re.compile(r"\$\{(.+?)\}", re.IGNORECASE)
        elif isinstance(self._style, logging.StrFormatStyle):
            formatter_style_pattern = re.compile(r"\{(.+?)\}", re.IGNORECASE)
        elif isinstance(self._style, logging.PercentStyle):
            formatter_style_pattern = re.compile(r"%\((.+?)\)", re.IGNORECASE)
        else:
            raise ValueError(f"Invalid format: {self._fmt}")

        return formatter_style_pattern.findall(self._fmt) if self._fmt else []

    def add_fields(
        self,
        log_record: Dict[str, Any],
        record: logging.LogRecord,
        message_dict: Dict[str, Any],
    ) -> None:
        """
        Override this method to implement custom logic for adding fields.
        """
        for field in self._required_fields:
            log_record[field] = record.__dict__.get(field)

        log_record |= self.static_fields
        log_record.update(message_dict)
        merge_record_extra(
            record,
            log_record,
            reserved=self._skip_fields,
            rename_fields=self.rename_fields,
        )

        if self.timestamp:
            key = self.timestamp if type(self.timestamp) == str else "timestamp"  # noqa: E721
            log_record[key] = datetime.fromtimestamp(
                record.created, tz=timezone.utc)

        self._perform_rename_log_fields(log_record)

    def _perform_rename_log_fields(self, log_record):
        for old_field_name, new_field_name in self.rename_fields.items():
            log_record[new_field_name] = log_record[old_field_name]
            del log_record[old_field_name]

    def process_log_record(self, log_record):
        """
        Override this method to implement custom logic
        on the possibly ordered dictionary.
        """
        return log_record

    def jsonify_log_record(self, log_record):
        """Returns a json string of the log record."""
        return self.json_serializer(
            log_record,
            default=self.json_default,
            cls=self.json_encoder,
            indent=self.json_indent,
            ensure_ascii=self.json_ensure_ascii,
        )

    def serialize_log_record(self, log_record: Dict[str, Any]) -> str:
        """Returns the final representation of the log record."""
        return f"{self.prefix}{self.jsonify_log_record(log_record)}"

    def format(self, record: logging.LogRecord) -> str:
        """Formats a log record and serializes to json"""
        message_dict: Dict[str, Any] = {}

        if isinstance(record.msg, dict):
            message_dict = record.msg
            record.message = ""
        else:
            record.message = record.getMessage()

        # only format time if needed
        if "asctime" in self._required_fields:
            record.asctime = self.formatTime(record, self.datefmt)

        # Display formatted exception, but allow overriding it in the
        # user-supplied dict.
        if record.exc_info and not message_dict.get("exc_info"):
            message_dict["exc_info"] = self.formatException(record.exc_info)
        if not message_dict.get("exc_info") and record.exc_text:
            message_dict["exc_info"] = record.exc_text

        # Display formatted record of stack frames
        # default format is a string returned from :func:`traceback.print_stack`
        if record.stack_info and not message_dict.get("stack_info"):
            message_dict["stack_info"] = self.formatStack(record.stack_info)

        log_record: Dict[str, Any] = OrderedDict()
        self.add_fields(log_record, record, message_dict)
        log_record = self.process_log_record(log_record)

        return self.serialize_log_record(log_record)
