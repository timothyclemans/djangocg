from djangocg.contrib.localflavor.mx.models import (
    MXStateField, MXRFCField, MXCURPField, MXZipCodeField)
from djangocg.db import models


class MXPersonProfile(models.Model):
    state = MXStateField()
    rfc = MXRFCField()
    curp = MXCURPField()
    zip_code = MXZipCodeField()

    class Meta:
        app_label = 'localflavor'
