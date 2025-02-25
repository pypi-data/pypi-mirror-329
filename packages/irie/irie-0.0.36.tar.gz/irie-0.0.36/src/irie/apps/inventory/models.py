#===----------------------------------------------------------------------===#
#
#         STAIRLab -- STructural Artificial Intelligence Laboratory
#
#===----------------------------------------------------------------------===#
#
#   Summer 2023, BRACE2 Team
#   Berkeley, CA
#
#----------------------------------------------------------------------------#
from django.db import models
from django.core.validators import int_list_validator
from django.urls import reverse

class Corridor(models.Model):
    id       = models.BigAutoField(primary_key=True)
    name     = models.CharField(max_length=20)
    route    = models.CharField(max_length=100, blank=True)
    assets   = models.ManyToManyField('Asset', related_name='corridors')

    def __str__(self):
        return f"{self.name} ({self.assets.count()})"


class Asset(models.Model):
    id = models.BigAutoField(primary_key=True)
    cesmd = models.CharField(max_length=7, blank=True, null=True)
    calid = models.CharField(max_length=15)
    name  = models.CharField(max_length=100,  blank=True)
    notes = models.CharField(max_length=1024, blank=True, null=True)

    is_complete = models.BooleanField(help_text="Is the asset a complete digital twin")

    nbi_data  = models.JSONField(default=dict, blank=True)
    cgs_data  = models.JSONField(default=list, blank=True)

    # Ground motion sensors
    ground_sensors = models.CharField(validators=[int_list_validator],
                                      max_length=400, blank=True,
                                      help_text="Comma-separated list of ground channel numbers")
    bridge_sensors = models.CharField(validators=[int_list_validator],
                                      max_length=400, blank=True,
                                      help_text="Comma-separated list of bridge channel numbers")

    def __str__(self):
        return f"{self.calid} - {self.name}"

    def get_absolute_url(self):
        return reverse("asset_profile", args=[self.calid])
    
    @property 
    def last_event(self):
        from irie.apps.events.models import EventRecord
        # TODO: use event_date
        try:
            return EventRecord.objects.filter(asset=self).latest("upload_date")
        except EventRecord.DoesNotExist:
            return None

    @property
    def predictors(self):
        from irie.apps.prediction.predictor import PREDICTOR_TYPES
        from irie.apps.prediction.models import PredictorModel
        return {
            p.name: PREDICTOR_TYPES[p.protocol](p)
            for p in PredictorModel.objects.filter(asset=self)
        }

    @property
    def event_count(self):
        from irie.apps.events.models import EventRecord
        return EventRecord.objects.filter(asset=self).count()

    @property
    def rendering(self):
        from irie.apps.prediction.models import PredictorModel
        for predictor in PredictorModel.objects.filter(asset=self):
            if predictor.render_file:
                return predictor.render_file.url

    @property
    def coordinates(self):
        if self.nbi_data:
            for table in self.nbi_data.values():
                if "Latitude" in table:
                    return map(float, map(table.get, ["Latitude", "Longitude"]))

        if self.cgs_data:
            lat, lon = map(self.cgs_data[0].get, ["Latitude", "Longitude"])
            return (float(lat.replace("N", "")), -float(lon.replace("W", "")))

        
        return (None, None)

    class Meta:
        ordering = ["-id"]


class Vulnerability: # (models.Model):
    type    = None
    asset   = None
    notes   = models.CharField(max_length=1024, blank=True, null=True)


class Datum(models.Model):
    name  = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}"

class SensorGroup(models.Model):
    """
    """
    name    = models.CharField(max_length=100)
#   sensors; access with .sensor_set.all()
    asset   = models.ForeignKey(Asset, on_delete=models.RESTRICT)
    datum   = models.ForeignKey(Datum, on_delete=models.RESTRICT)
#   network = models.CharField(max_length=100)
#   events  = None
    def __str__(self):
        return f"{self.name} - {self.datum}"

class Sensor(models.Model):
    # class Status:
    #     active: bool

    x    = models.FloatField()
    y    = models.FloatField()
    z    = models.FloatField()

    dx   = models.FloatField()
    dy   = models.FloatField()
    dz   = models.FloatField()

    group  = models.ForeignKey(SensorGroup, related_name="sensors", on_delete=models.RESTRICT)

    def __str__(self):
        return f"Sensor {self.id} ({self.group.name})"
