from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib.gis.forms import LineStringField, OSMWidget
from django.forms import ModelForm

from biketracks.tracks.models import Track


class TrackForm(ModelForm):
    track = LineStringField(widget=OSMWidget, help_text="Track is read-only", disabled=True)

    class Meta:
        model = Track
        fields = '__all__'


@admin.register(Track)
class TrackAdmin(OSMGeoAdmin):
    form = TrackForm
