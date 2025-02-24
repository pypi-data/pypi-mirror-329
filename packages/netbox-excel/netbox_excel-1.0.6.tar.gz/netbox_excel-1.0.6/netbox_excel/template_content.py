from netbox.plugins import PluginTemplateExtension
class ImportExcelDevice(PluginTemplateExtension):
    model = 'dcim.device'
    def list_buttons(self):
        return self.render('netbox_excel/import_excel.html')
    
class ExportExcelDevice(PluginTemplateExtension):
    model = 'dcim.device'
    def list_buttons(self):
        return self.render('netbox_excel/export_excel.html')

template_extensions = [ExportExcelDevice]