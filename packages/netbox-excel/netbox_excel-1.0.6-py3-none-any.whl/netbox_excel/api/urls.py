from netbox.api.routers import NetBoxRouter
from netbox_excel.api.views import (
    NetboxExcelInfoRootView,
    ImportExcelViewSet,
)

router = NetBoxRouter()
router.APIRootView = NetboxExcelInfoRootView

router.register("import_excel", ImportExcelViewSet)
urlpatterns = router.urls
