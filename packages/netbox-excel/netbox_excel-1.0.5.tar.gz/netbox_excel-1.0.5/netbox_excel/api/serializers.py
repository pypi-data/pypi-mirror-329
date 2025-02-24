from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer
from netbox_excel.models import ImportExcel


class ImportExcelSerializer(NetBoxModelSerializer):
    display = serializers.SerializerMethodField()
    
    class Meta:
        model = ImportExcel
        fields = (
            "id",
            "name",
            "description",
            "tags",
            "custom_field_data",
            "created",
            "last_updated",
        )
        brief_fields = ("id", "name", "description")

    def get_display(self, obj):
        return f"{obj}"