from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib.gis.forms import LineStringField, OSMWidget
from django.forms import ModelForm

from routes.models import Route


class RouteForm(ModelForm):
    route = LineStringField(widget=OSMWidget, help_text="Route is read-only", disabled=True)

    class Meta:
        model = Route
        fields = '__all__'


@admin.register(Route)
class RouteAdmin(OSMGeoAdmin):
    form = RouteForm
