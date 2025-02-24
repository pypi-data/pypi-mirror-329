from django.urls import path
from netbox_excel import views

urlpatterns = [
    path('import/excel', views.ImportExcelView, name='import_file'),
    path('export/excel', views.ExportExcelView, name='export_file'),
    # path('dcim/devices/import-excel', CustomDeviceBulkImportView.as_view(), name='import_excel'),
]
