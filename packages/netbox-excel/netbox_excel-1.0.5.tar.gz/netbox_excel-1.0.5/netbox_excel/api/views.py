from rest_framework.routers import APIRootView

from netbox.api.viewsets import NetBoxModelViewSet
from netbox_excel.api.serializers import (
    ImportExcelSerializer,
)
from netbox_excel.models import ImportExcel


class NetboxExcelInfoRootView(APIRootView):
    """
    Netbox Excel API root view
    """

    def get_view_name(self):
        return "Netbox Excel"

class ImportExcelViewSet(NetBoxModelViewSet):
    queryset = ImportExcel.objects.all()
    serializer_class = ImportExcelSerializer