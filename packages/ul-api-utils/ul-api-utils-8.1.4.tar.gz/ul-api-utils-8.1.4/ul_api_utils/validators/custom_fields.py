import csv
from typing import TypeVar, Generic, List, Union, Generator, Callable, Annotated, Any, get_args
from uuid import UUID

from pydantic import ValidationError, Field, StringConstraints, TypeAdapter
from pydantic_core.core_schema import ValidationInfo

from ul_api_utils.const import CRON_EXPRESSION_VALIDATION_REGEX, MIN_UTC_OFFSET_SECONDS, MAX_UTC_OFFSET_SECONDS

NotEmptyListAnnotation = Annotated[list[Any], Field(min_length=1)]
NotEmptyListStrAnnotation = Annotated[list[str], Field(min_length=1)]
NotEmptyListIntAnnotation = Annotated[list[int], Field(min_length=1)]
NotEmptyListUUIDAnnotation = Annotated[list[UUID], Field(min_length=1)]
CronScheduleAnnotation = Annotated[str, StringConstraints(pattern=CRON_EXPRESSION_VALIDATION_REGEX)]
WhiteSpaceStrippedStrAnnotation = Annotated[str, StringConstraints(strip_whitespace=True)]
UTCOffsetSecondsAnnotation = Annotated[int, Field(ge=MIN_UTC_OFFSET_SECONDS, le=MAX_UTC_OFFSET_SECONDS)]
PgTypePasswordStrAnnotation = Annotated[str, StringConstraints(min_length=6, max_length=72)]
PgTypeShortStrAnnotation = Annotated[str, StringConstraints(min_length=0, max_length=255)]
PgTypeLongStrAnnotation = Annotated[str, StringConstraints(min_length=0, max_length=1000)]
PgTypeInt16Annotation = Annotated[int, Field(ge=-32768, le=32768)]
PgTypePositiveInt16Annotation = Annotated[int, Field(ge=0, le=32768)]
PgTypeInt32Annotation = Annotated[int, Field(ge=-2147483648, le=2147483648)]
PgTypePositiveInt32Annotation = Annotated[int, Field(ge=0, le=2147483648)]
PgTypeInt64Annotation = Annotated[int, Field(ge=-9223372036854775808, le=9223372036854775808)]
PgTypePositiveInt64Annotation = Annotated[int, Field(ge=0, le=9223372036854775808)]


QueryParamsSeparatedListValueType = TypeVar('QueryParamsSeparatedListValueType')


class QueryParamsSeparatedList(Generic[QueryParamsSeparatedListValueType]):
    """
    Supports cases when query parameters are being sent as a string, but you have to assume
    that it is a list.

    F.E. Query string is ?foo=1,2

    Note:
        Sent as a string, but interpreted as List.
    """

    def __init__(self, contains_type: QueryParamsSeparatedListValueType) -> None:
        self.contains_type = contains_type

    def __repr__(self) -> str:
        return f'QueryParamsSeparatedList({super().__repr__()})'

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[[Union[List[str], str], ValidationInfo], List[QueryParamsSeparatedListValueType]], None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, query_param: Union[List[str], str], info: ValidationInfo) -> List[QueryParamsSeparatedListValueType]:
        """
        Validate and convert the query parameter string into a list of the specified type.
        """
        if not isinstance(query_param, list):
            query_param = [query_param]

        reader = csv.reader(query_param, skipinitialspace=True)
        splitted = next(reader)

        adapter = TypeAdapter(get_args(cls)[0])

        validated_items = []
        errors = []

        for value in splitted:
            try:
                validated_items.append(adapter.validate_python(value))
            except ValidationError as e:
                errors.append(e)
        if errors:
            raise ValidationError(errors)

        return validated_items
