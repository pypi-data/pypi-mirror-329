from django.forms.widgets import Input


class IntervalWidget(Input):
    class Media:
        js = ["js/intervalwidget.js",]
        css = {"all": ["css/intervalwidget.css"]}
