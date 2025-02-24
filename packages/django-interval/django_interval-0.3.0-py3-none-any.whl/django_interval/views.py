from django.contrib.contenttypes.models import ContentType
from django.views.generic.base import TemplateView
from django.http import Http404


class IntervalView(TemplateView):
    template_name = "django_interval/interval.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        natural_key = kwargs.get("natural_key")
        app_label, model = natural_key.split(".")
        content_type = ContentType.objects.get_by_natural_key(app_label, model)

        if field := getattr(content_type.model_class(), kwargs.get("field"), None):
            if datestring := self.request.GET.get("datestring"):
                sort_date, from_date, to_date = field.calculate(datestring)
                context["dates"] = {
                    "sort_date": sort_date,
                    "from_date": from_date,
                    "to_date": to_date,
                }
            return context
        raise Http404
