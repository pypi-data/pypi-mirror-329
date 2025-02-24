from django.db import models
from django.urls import reverse
from django.utils import safestring

from netbox.models import NetBoxModel
from utilities.querysets import RestrictedQuerySet
from netbox.models.features import TagsMixin

class ImportExcel(NetBoxModel,TagsMixin):
    name = models.CharField(max_length=128)
    file = models.FileField(upload_to='dcim/devices/import/excel')
    deivce_error = models.CharField(null=True, blank=True)
    deivce_type_error = models.CharField(null=True, blank=True)
    deivce_role_error = models.CharField(null=True, blank=True)
    rack_error = models.CharField(null=True, blank=True)
    manufacturer_error = models.CharField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class ExportExcel(models.Model):
    id = models.IntegerField(primary_key=True)
    rack = models.CharField(null=True, blank=True)
    u_number = models.CharField(null=True, blank=True)
    u_end = models.CharField(null=True, blank=True)
    position = models.CharField(null=True, blank=True)
    device_name = models.CharField(null=True, blank=True)
    device_role = models.CharField(null=True, blank=True) # chủng loại 
    owner_device = models.CharField(null=True, blank=True) # Quản lý
    contract_number = models.CharField(null=True, blank=True) # So HD
    serial_number = models.CharField(null=True, blank=True)
    device_type = models.CharField(null=True, blank=True) # Model 
    device_description = models.CharField(null=True, blank=True)
    year_of_investment = models.CharField(null=True, blank=True)
    