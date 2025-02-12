import datetime
import uuid
from collections import OrderedDict
from decimal import Decimal
from enum import Enum
from json import JSONDecoder, JSONEncoder
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    Generic,
    Iterable,
    List,
    Mapping,
    MutableMapping,
    NoReturn,
    Optional,
    Pattern,
    Protocol,
    Sequence,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from django.core.files.base import File
from django.db import models
from django.forms import ImageField as DjangoImageField  # noqa: F401
from rest_framework.serializers import BaseSerializer
from typing_extensions import Final, Literal

class _Empty(Enum):
    sentinel: Literal[0]

empty: Final[Literal[_Empty.sentinel]]

class BuiltinSignatureError(Exception): ...

class CreateOnlyDefault:
    requires_context: bool = ...
    default: Any = ...
    def __init__(self, default: Any) -> None: ...
    def __call__(self, serializer_field: Field[Any, Any, Any, Any]) -> Any: ...

class CurrentUserDefault:
    requires_context: bool = ...
    def __call__(self, serializer_field: Field[Any, Any, Any, Any]) -> Any: ...

class SkipField(Exception): ...

class Option(Protocol):
    start_option_group: bool = ...
    end_option_group: bool = ...
    label: str
    value: str
    display_text: str

def is_simple_callable(obj: Callable[..., Any]) -> bool: ...
def get_attribute(instance: Any, attrs: Optional[List[str]]) -> Any: ...
def set_value(dictionary: MutableMapping[str, Any], keys: Sequence[str], value: Any) -> None: ...
def to_choices_dict(choices: Sequence[Any]) -> OrderedDict[Any, Any]: ...
def flatten_choices_dict(choices: Dict[Any, Any]) -> OrderedDict[Any, Any]: ...
def iter_options(
    grouped_choices: OrderedDict[Any, Any], cutoff: Optional[int] = ..., cutoff_text: Optional[str] = ...
) -> Generator[Option, None, None]: ...
def get_error_detail(exc_info: Any) -> Any: ...

REGEX_TYPE: Pattern[str]
NOT_READ_ONLY_WRITE_ONLY: str
NOT_READ_ONLY_REQUIRED: str
NOT_REQUIRED_DEFAULT: str
USE_READONLYFIELD: str
MISSING_ERROR_MESSAGE: str

_IN = TypeVar("_IN")  # Instance Type
_VT = TypeVar("_VT")  # Value Type
_DT = TypeVar("_DT")  # Data Type
_RP = TypeVar("_RP")  # Representation Type

class SupportsToPython(Protocol):
    def to_python(self, value: Any) -> Any: ...

_DefaultInitial = Union[_VT, Callable[[], _VT], None, _Empty]

class Field(Generic[_VT, _DT, _RP, _IN]):
    """
    Type arguments:
    - _VT: The data type which the validated data will be represented as
    - _DT: The type which unserialized data will be before being transformed into _VT
    - _RT: A primitive type (ex., str or int) which can be used to represent the field's serialized and validated value (Similar to repr())
    - _IN: Type of an instance of this field class
    """

    allow_null: bool = ...
    default: Optional[_VT] = ...
    default_empty_html: Any = ...
    default_error_messages: Dict[str, str] = ...
    default_validators: List[Callable[..., Any]] = ...
    error_messages: Dict[str, str] = ...
    field_name: Optional[str] = ...
    help_text: Optional[str] = ...
    initial: Optional[Union[_VT, Callable[[], _VT]]] = ...
    # NOTE(sbdchd): I made some of these Any so that when declaring a field on
    # a serializer with the same name we don't get a type error.
    label: Any
    parent: BaseSerializer
    read_only: bool
    required: Any
    source: Any
    source_attrs: List[str] = ...
    style: Dict[str, Any]
    write_only: bool
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[_VT] = ...,
        initial: _DefaultInitial[_VT] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable[..., Any]] = ...,
        allow_null: bool = ...,
    ): ...
    def bind(self, field_name: str, parent: BaseSerializer) -> None: ...
    @property
    def validators(self) -> List[Callable[..., Any]]: ...
    @validators.setter
    def validators(self, validators: List[Callable[..., Any]]) -> None: ...
    def get_validators(self) -> List[Callable[..., Any]]: ...
    def get_initial(self) -> Optional[_VT]: ...
    def get_value(self, dictionary: Mapping[Any, Any]) -> Any: ...
    def get_attribute(self, instance: _IN) -> Optional[_RP]: ...
    def get_default(self) -> Optional[_VT]: ...
    def validate_empty_values(self, data: Any) -> Tuple[bool, Any]: ...
    def run_validation(self, data: Any = ...) -> Any: ...
    def run_validators(self, value: Any) -> None: ...
    def to_internal_value(self, data: _DT) -> _VT: ...
    def to_representation(self, value: _VT) -> _RP: ...
    def fail(self, key: str, **kwargs: Any) -> NoReturn: ...
    @property
    def root(self) -> BaseSerializer: ...
    @property
    def context(self) -> Dict[str, Any]: ...
    def __new__(cls, *args: Any, **kwargs: Any) -> Field[Any, Any, Any, Any]: ...
    def __deepcopy__(self, memo: Mapping[Any, Any]) -> Field[Any, Any, Any, Any]: ...

class BooleanField(
    Field[
        bool,
        Union[
            bool,
            None,
            Literal["t"],
            Literal["T"],
            Literal["y"],
            Literal["Y"],
            Literal["yes"],
            Literal["YES"],
            Literal["true"],
            Literal["True"],
            Literal["TRUE"],
            Literal["on"],
            Literal["On"],
            Literal["ON"],
            Literal["1"],
            Literal[1],
            Literal["f"],
            Literal["F"],
            Literal["n"],
            Literal["N"],
            Literal["no"],
            Literal["NO"],
            Literal["false"],
            Literal["False"],
            Literal["FALSE"],
            Literal["off"],
            Literal["Off"],
            Literal["OFF"],
            Literal["0"],
            Literal[0],
        ],
        bool,
        Any,
    ]
):
    TRUE_VALUES: Set[Union[str, bool, int]] = ...
    FALSE_VALUES: Set[Union[str, bool, int, float]] = ...
    NULL_VALUES: Set[Union[str, None]] = ...

class NullBooleanField(
    Field[
        Union[bool, None],
        Union[
            bool,
            None,
            Literal["t"],
            Literal["T"],
            Literal["y"],
            Literal["Y"],
            Literal["yes"],
            Literal["YES"],
            Literal["true"],
            Literal["True"],
            Literal["TRUE"],
            Literal["on"],
            Literal["On"],
            Literal["ON"],
            Literal["1"],
            Literal[1],
            Literal["f"],
            Literal["F"],
            Literal["n"],
            Literal["N"],
            Literal["no"],
            Literal["NO"],
            Literal["false"],
            Literal["False"],
            Literal["FALSE"],
            Literal["off"],
            Literal["Off"],
            Literal["OFF"],
            Literal["0"],
            Literal[0],
            Literal["null"],
            Literal["Null"],
            Literal["NULL"],
            Literal[""],
        ],
        bool,
        Any,
    ]
):
    TRUE_VALUES: Set[Union[str, bool, int]] = ...
    FALSE_VALUES: Set[Union[str, bool, int, float]] = ...
    NULL_VALUES: Set[Union[str, None]] = ...

class CharField(Field[str, str, str, Any]):
    allow_blank: bool = ...
    trim_whitespace: bool = ...
    max_length: Optional[int] = ...
    min_length: Optional[int] = ...
    def __init__(
        self,
        *,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[str] = ...,
        initial: _DefaultInitial[str] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable[..., Any]] = ...,
        allow_null: bool = ...,
        allow_blank: bool = ...,
        trim_whitespace: bool = ...,
        max_length: int = ...,
        min_length: Optional[int] = ...,
    ): ...

class EmailField(CharField): ...

class RegexField(CharField):
    def __init__(
        self,
        regex: Union[str, Pattern[str]],
        *,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[str] = ...,
        initial: _DefaultInitial[str] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable[..., Any]] = ...,
        allow_null: bool = ...,
        allow_blank: bool = ...,
        trim_whitespace: bool = ...,
        max_length: int = ...,
        min_length: Optional[int] = ...,
    ): ...

class SlugField(CharField):
    allow_unicode: bool = ...
    def __init__(
        self,
        allow_unicode: bool = ...,
        *,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[str] = ...,
        initial: _DefaultInitial[str] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable[..., Any]] = ...,
        allow_null: bool = ...,
        allow_blank: bool = ...,
        trim_whitespace: bool = ...,
        max_length: int = ...,
        min_length: Optional[int] = ...,
    ): ...

class URLField(CharField): ...

class UUIDField(Field[uuid.UUID, Union[uuid.UUID, str, int], str, Any]):
    valid_formats: Sequence[str] = ...
    uuid_format: str
    def __init__(
        self,
        *,
        format: Optional[str] = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[uuid.UUID] = ...,
        initial: _DefaultInitial[uuid.UUID] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable[..., Any]] = ...,
        allow_null: bool = ...,
    ): ...

class IPAddressField(CharField):
    protocol: str
    unpack_ipv4: bool
    def __init__(
        self,
        protocol: str = ...,
        *,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[str] = ...,
        initial: _DefaultInitial[str] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable[..., Any]] = ...,
        allow_null: bool = ...,
        allow_blank: bool = ...,
        trim_whitespace: bool = ...,
        max_length: int = ...,
        min_length: Optional[int] = ...,
    ): ...

class IntegerField(Field[int, Union[float, int, str], int, Any]):
    MAX_STRING_LENGTH: int = ...
    re_decimal: Pattern[str] = ...
    max_value: Optional[int] = ...
    min_value: Optional[int] = ...
    def __init__(
        self,
        *,
        max_value: Optional[int] = ...,
        min_value: Optional[int] = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[int] = ...,
        initial: _DefaultInitial[int] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable[..., Any]] = ...,
        allow_null: bool = ...,
    ): ...

class FloatField(Field[float, Union[float, int, str], str, Any]):
    MAX_STRING_LENGTH: int = ...
    re_decimal: Pattern[str] = ...
    max_value: Optional[float] = ...
    min_value: Optional[float] = ...
    def __init__(
        self,
        *,
        max_value: float = ...,
        min_value: float = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[float] = ...,
        initial: _DefaultInitial[float] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable[..., Any]] = ...,
        allow_null: bool = ...,
    ): ...

class DecimalField(Field[Decimal, Union[int, float, str, Decimal], str, Any]):
    MAX_STRING_LENGTH: int = ...
    max_digits: Optional[int]
    decimal_places: Optional[int]
    coerce_to_string: Optional[bool]
    max_value: Optional[Union[Decimal, int, float]]
    min_value: Optional[Union[Decimal, int, float]]
    localize: bool
    rounding: Optional[str]
    max_whole_digits = Optional[int]
    def __init__(
        self,
        max_digits: Optional[int],
        decimal_places: Optional[int],
        coerce_to_string: bool = ...,
        max_value: Union[Decimal, int, float] = ...,
        min_value: Union[Decimal, int, float] = ...,
        localize: bool = ...,
        rounding: Optional[str] = ...,
        *,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[Decimal] = ...,
        initial: _DefaultInitial[Decimal] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable[..., Any]] = ...,
        allow_null: bool = ...,
    ): ...
    def validate_precision(self, value: Decimal) -> Decimal: ...
    def quantize(self, value: Decimal) -> Decimal: ...

class DateTimeField(Field[datetime.datetime, Union[datetime.datetime, str], str, Any]):
    datetime_parser: Callable[[str, str], datetime.datetime] = ...
    format: Optional[str] = ...
    input_formats: Sequence[str] = ...
    timezone: datetime.tzinfo = ...
    def __init__(
        self,
        format: Optional[str] = ...,
        input_formats: Sequence[str] = ...,
        default_timezone: Optional[datetime.tzinfo] = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[datetime.datetime] = ...,
        initial: _DefaultInitial[datetime.datetime] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable[..., Any]] = ...,
        allow_null: bool = ...,
    ): ...
    def enforce_timezone(self, value: datetime.datetime) -> datetime.datetime: ...
    def default_timezone(self) -> Optional[str]: ...

class DateField(Field[datetime.date, Union[datetime.date, str], str, Any]):
    datetime_parser: Callable[[str, str], datetime.datetime] = ...
    format: Optional[str] = ...
    input_formats: Sequence[str] = ...
    def __init__(
        self,
        format: Optional[str] = ...,
        input_formats: Sequence[str] = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[datetime.date] = ...,
        initial: _DefaultInitial[datetime.date] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable[..., Any]] = ...,
        allow_null: bool = ...,
    ): ...

class TimeField(Field[datetime.time, Union[datetime.time, str], str, Any]):
    datetime_parser: Callable[[str, str], datetime.datetime] = ...
    format: Optional[str] = ...
    input_formats: Sequence[str] = ...
    def __init__(
        self,
        format: Optional[str] = ...,
        input_formats: Sequence[str] = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[datetime.time] = ...,
        initial: _DefaultInitial[datetime.time] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable[..., Any]] = ...,
        allow_null: bool = ...,
    ): ...

class DurationField(Field[datetime.timedelta, Union[datetime.timedelta, str], str, Any]):
    max_value: Optional[datetime.timedelta] = ...
    min_value: Optional[datetime.timedelta] = ...
    def __init__(
        self,
        *,
        max_value: Union[datetime.timedelta, int, float] = ...,
        min_value: Union[datetime.timedelta, int, float] = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[datetime.timedelta] = ...,
        initial: _DefaultInitial[datetime.timedelta] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable[..., Any]] = ...,
        allow_null: bool = ...,
    ): ...

class ChoiceField(Field[str, Union[str, int, Tuple[Union[str, int], Union[str, int, Tuple[Any, ...]]]], str, Any]):
    html_cutoff: Optional[int] = ...
    html_cutoff_text: Optional[str] = ...
    allow_blank: bool = ...
    grouped_choices: OrderedDict[Any, Any] = ...
    choice_strings_to_values: Dict[str, Any] = ...
    _choices: OrderedDict[Any, Any] = ...
    def __init__(
        self,
        choices: Sequence[Any],
        *,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Union[_Empty, str, int, Callable[[], str], Callable[[], int]] = ...,
        initial: Union[_Empty, str, int, Callable[[], str], Callable[[], int]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable[..., Any]] = ...,
        allow_null: bool = ...,
        html_cutoff: int = ...,
        html_cutoff_text: str = ...,
        allow_blank: bool = ...,
    ): ...
    def iter_options(self) -> Iterable[Option]: ...
    def _get_choices(self) -> Dict[Any, Any]: ...
    def _set_choices(self, choices: Sequence[Any]) -> None: ...
    choices = property(_get_choices, _set_choices)

class MultipleChoiceField(
    ChoiceField,
    Field[
        str,
        Sequence[Union[str, int, Tuple[Union[str, int], Union[str, int]]]],
        Sequence[Union[str, Tuple[Union[str, int], Union[str, int]]]],
        Any,
    ],
):
    allow_empty: bool = ...
    def __init__(
        self,
        choices: Sequence[Any],
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Union[
            _Empty, Sequence[str], Sequence[int], Callable[[], Sequence[str]], Callable[[], Sequence[int]]
        ] = ...,
        initial: Union[
            _Empty, Sequence[str], Sequence[int], Callable[[], Sequence[str]], Callable[[], Sequence[int]]
        ] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable[..., Any]] = ...,
        allow_null: bool = ...,
        html_cutoff: int = ...,
        html_cutoff_text: str = ...,
        allow_blank: bool = ...,
        allow_empty: bool = ...,
    ): ...

class FilePathField(ChoiceField):
    def __init__(
        self,
        path: str,
        match: str = ...,
        recursive: bool = ...,
        allow_files: bool = ...,
        allow_folders: bool = ...,
        required: bool = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        default: Union[_Empty, str, int, Callable[[], str], Callable[[], int]] = ...,
        initial: Union[_Empty, str, int, Callable[[], str], Callable[[], int]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable[..., Any]] = ...,
        allow_null: bool = ...,
        html_cutoff: int = ...,
        html_cutoff_text: str = ...,
        allow_blank: bool = ...,
    ): ...

class FileField(Field[File, File, Union[str, None], Any]):  # this field can return None without raising!
    max_length: int = ...
    allow_empty_file: bool = ...
    use_url: bool = ...
    def __init__(
        self,
        *,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Union[_Empty, File, Callable[[], File]] = ...,
        initial: Union[_Empty, File, Callable[[], File]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable[..., Any]] = ...,
        allow_null: bool = ...,
        max_length: int = ...,
        allow_empty_file: bool = ...,
        use_url: bool = ...,
    ): ...

class ImageField(FileField):
    _DjangoImageField: SupportsToPython = ...
    def __init__(
        self,
        *,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Union[_Empty, File, Callable[[], File]] = ...,
        initial: Union[_Empty, File, Callable[[], File]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable[..., Any]] = ...,
        allow_null: bool = ...,
        max_length: int = ...,
        allow_empty_file: bool = ...,
        use_url: bool = ...,
        _DjangoImageField: Type[SupportsToPython] = ...,
    ): ...

class _UnvalidatedField(Field[Any, Any, Any, Any]): ...

class ListField(Field[List[Any], List[Any], List[Any], Any]):
    child: Field[Any, Any, Any, Any] = ...
    allow_empty: bool = ...
    max_length: Optional[int] = ...
    min_length: Optional[int] = ...
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Union[_Empty, List[Any], Callable[[], List[Any]]] = ...,
        initial: Union[_Empty, List[Any], Callable[[], List[Any]]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable[..., Any]] = ...,
        allow_null: bool = ...,
        *,
        child: Field[Any, Any, Any, Any] = ...,
        allow_empty: bool = ...,
        max_length: int = ...,
        min_length: int = ...,
    ): ...
    def run_child_validation(self, data: List[Mapping[Any, Any]]) -> Any: ...

class DictField(Field[Dict[Any, Any], Dict[Any, Any], Dict[Any, Any], Any]):
    child: Field[Any, Any, Any, Any] = ...
    allow_empty: bool = ...
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Union[_Empty, Dict[Any, Any], Callable[[], Dict[Any, Any]]] = ...,
        initial: Union[_Empty, Dict[Any, Any], Callable[[], Dict[Any, Any]]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable[..., Any]] = ...,
        allow_null: bool = ...,
        *,
        child: Field[Any, Any, Any, Any] = ...,
        allow_empty: bool = ...,
    ): ...
    def run_child_validation(self, data: Any) -> Any: ...

class HStoreField(DictField):
    child: CharField = ...

class JSONField(
    Field[Union[Dict[str, Any], List[Dict[str, Any]]], Union[Dict[str, Any], List[Dict[str, Any]]], str, Any]
):
    binary: bool = ...
    encoder: Optional[JSONEncoder] = ...
    decoder: Optional[JSONDecoder] = ...
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Union[_Empty, Mapping[Any, Any], Callable[[], Mapping[Any, Any]]] = ...,
        initial: Union[_Empty, Mapping[Any, Any], Callable[[], Mapping[Any, Any]]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable[..., Any]] = ...,
        allow_null: bool = ...,
        *,
        binary: bool = ...,
        encoder: JSONEncoder = ...,
        decoder: JSONDecoder = ...,
    ): ...

class ReadOnlyField(Field[Any, Any, Any, Any]): ...
class HiddenField(Field[Any, Any, Any, Any]): ...

class SerializerMethodField(Field[Any, Any, Any, Any]):
    method_name: str = ...
    def __init__(
        self,
        method_name: str = ...,
        *,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable[..., Any]] = ...,
        allow_null: bool = ...,
    ): ...

class ModelField(Field[Any, Any, Any, Any]):
    model_field: models.Field[Any, Any] = ...
    max_length: int = ...
    def __init__(
        self,
        model_field: models.Field[Any, Any],
        *,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable[..., Any]] = ...,
        allow_null: bool = ...,
        max_length: int = ...,
    ): ...
