#===----------------------------------------------------------------------===#
#
#         STAIRLab -- STructural Artificial Intelligence Laboratory
#
#===----------------------------------------------------------------------===#
from django import forms
from django.forms import formset_factory
from irie.apps.inventory.models import Asset, SensorGroup, Sensor

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = '__all__'

class SensorGroupForm(forms.ModelForm):
    class Meta:
        model = SensorGroup
        fields = ['name', 'datum']

class SensorForm(forms.ModelForm):
    class Meta:
        model = Sensor
        fields = ['x', 'y', 'z', 'dx', 'dy', 'dz']
        labels = {
            'x': 'x',
            'y': 'y',
            'z': 'z',
            'dx': 'dx',
            'dy': 'dy',
            'dz': 'dz',
        }


# Create a formset for multiple sensors
SensorFormSet = formset_factory(SensorForm, extra=3)  # Default to 3 empty sensor forms
