from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ImportExcelForm, ExportExcelForm
from netbox_excel.models import ExportExcel
from django.views.decorators.csrf import requires_csrf_token
from netbox_excel.export import get_device, export_all_view_rack, export_only_device, export_all_rack
import openpyxl


@requires_csrf_token
def ImportExcelView(request):
    if request.method == 'POST':
        form = ImportExcelForm(request.POST, request.FILES)
    else:
        form = ImportExcelForm()
    return render(request, 'netbox_excel/import_excel_console_log.html', {'form': form})

@requires_csrf_token
def ExportExcelView(request):
    if request.method == 'POST':
        # quick_search = request.POST.get('quick_search')
        type = request.POST.get('type')

        if type == "only_device":
            workbook = export_only_device()
        else: 
            #workbook = export_all_view_rack()
            workbook = export_all_rack()
        # add header response
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename="device_export_excel.xlsx"'

        workbook.save(response)
        return response
        # return HttpResponseRedirect("/dcim/devices/")
    else:
        # form = ExportExcelForm()
        return HttpResponseRedirect("/dcim/devices/")