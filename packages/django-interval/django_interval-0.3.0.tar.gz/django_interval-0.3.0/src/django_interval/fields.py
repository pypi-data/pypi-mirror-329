import re
from datetime import date
from typing import Callable, Tuple

from django.db.models import CharField, DateField
from django.contrib.contenttypes.models import ContentType
from django.forms import ValidationError
from django.urls import reverse, NoReverseMatch

from django_interval.utils import defaultdateparser
from django_interval.widgets import IntervalWidget


class GenericDateIntervalField(CharField):
    """Add additional fields to the model containing this field
    The check using `hasattr` and `setattr` to check the existence
    of the field is taken from https://github.com/django-money/django-money/blob/main/djmoney/models/fields.py#L255
    Without that the migrations did fail again and again ...
    Apparently this is *also* error prone, so we check with
    if the module is `__fake__` to know if we are running a migration.
    """

    def add_generated_date_field(self, cls, name):
        date_field = DateField(editable=False, blank=True, null=True)
        cls.add_to_class(name, date_field)
        setattr(self, f"_{name}", date_field)

    def contribute_to_class(self, cls, name):
        for field_name in [f"{name}_date_sort", f"{name}_date_from", f"{name}_date_to"]:
            if not hasattr(self, f"_{field_name}") and not cls.__module__ == "__fake__":
                self.add_generated_date_field(cls, field_name)
        super().contribute_to_class(cls, name)
        setattr(cls, name, self)

    def formfield(self, *args, **kwargs):
        content_type = ContentType.objects.get_for_model(self.model)
        natural_key = f"{content_type.app_label}.{content_type.model}"
        try:
            interval_view = reverse("intervalview", args=[natural_key, self.name])
            attrs = {"data-intervaluri": interval_view}
        except NoReverseMatch:
            attrs = {}
        kwargs["widget"] = IntervalWidget(attrs=attrs)
        return super().formfield(*args, **kwargs)


class FuzzyDateParserField(GenericDateIntervalField):
    def __init__(
        self,
        parser: Callable[[str], Tuple[date, date, date]] = defaultdateparser,
        *args,
        **kwargs,
    ):
        self.parser = parser
        super().__init__(*args, **kwargs)

    def _populate_fields(self, model_instance):
        name = self.attname
        value = getattr(model_instance, name)
        skip_date_parsing = getattr(model_instance, "skip_date_parsing", False)
        # this is a workaround until we find out another way to exclude
        # historical models (from `django-simple-history`)
        is_history_model = hasattr(model_instance, "history_id")
        if value and not skip_date_parsing and not is_history_model:
            try:
                date_sort, date_from, date_to = self.calculate(value)
                setattr(model_instance, f"{name}_date_sort", date_sort)
                setattr(model_instance, f"{name}_date_from", date_from)
                setattr(model_instance, f"{name}_date_to", date_to)
            except Exception as e:
                raise ValidationError(f"Error parsing date string: {e}")

    def calculate(self, date_string):
        return self.parser(date_string)

    def pre_save(self, model_instance, add):
        self._populate_fields(model_instance)
        return super().pre_save(model_instance, add)


FROM_PATTERN = r"<from: (?P<day>\d{1,2})\.(?P<month>\d{1,2}).(?P<year>\d{1,4})>"
TO_PATTERN = r"<to: (?P<day>\d{1,2})\.(?P<month>\d{1,2}).(?P<year>\d{1,4})>"
SORT_PATTERN = r"<sort: (?P<day>\d{1,2})\.(?P<month>\d{1,2}).(?P<year>\d{1,4})>"


class FuzzyDateRegexField(FuzzyDateParserField):
    """This Field allows you to define different regexes for
    extracting the `from`, the `to` and the `sort` values from
    the string. So, the string "2024 <sort: 2024-06-31>" could
    be parsed so that the `_date_sort` field is set to
    datetime.date(2024, 6, 1).
    The pattern hat to contain a <year> group, a <month> group and a <day> group.
    """

    def __init__(
        self,
        from_pattern=FROM_PATTERN,
        to_pattern=TO_PATTERN,
        sort_pattern=SORT_PATTERN,
        *args,
        **kwargs,
    ):
        self.from_pattern = from_pattern
        self.to_pattern = to_pattern
        self.sort_pattern = sort_pattern
        super().__init__(*args, **kwargs)

    def _match_to_date(self, regex_match: re.Match) -> date:
        match_dict = regex_match.groupdict()
        print(match_dict.keys())
        if match_dict.keys() >= {"day", "month", "year"}:
            month = match_dict.get("month", "01")
            day = match_dict.get("day", "01")
            return f"{match_dict['year']}-{month}-{day}"
        raise ValueError(
            f"Regex pattern does not contain all needed named groups (year, month, day): {match_dict}"
        )

    def calculate(self, date_string) -> Tuple[date, date, date]:
        sort_date, from_date, to_date = None, None, None
        if match := re.search(self.sort_pattern, date_string):
            sort_date = self._match_to_date(match)
        if match := re.search(self.from_pattern, date_string):
            from_date = self._match_to_date(match)
        if match := re.search(self.to_pattern, date_string):
            to_date = self._match_to_date(match)
        return sort_date, from_date, to_date

    def _populate_fields(self, model_instance):
        super()._populate_fields(model_instance)
        name = self.attname
        value = getattr(model_instance, name)
        sort_date, from_date, to_date = self.calculate(value)
        setattr(model_instance, f"{name}_date_sort", sort_date)
        setattr(model_instance, f"{name}_date_from", from_date)
        setattr(model_instance, f"{name}_date_to", to_date)
