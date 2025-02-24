from django import forms
from netbox_excel.models import ImportExcel


class ImportExcelForm(forms.Form):
    file = forms.FileField()

class ExportExcelForm(forms.Form):
    OPTIONS = [
        ('all', 'All'),
        ('current_view', 'Current View'),
    ]
    type = forms.ChoiceField(choices=OPTIONS, label="Select an type")
    # type = forms.CharField(label="type", max_length=100)