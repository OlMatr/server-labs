from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicineViewSet, CustomerViewSet, PharmacistViewSet, SupplierViewSet, DeliveryViewSet, DeliveryDetailsViewSet, SaleViewSet, SaleDetailsViewSet, report

router = DefaultRouter()
router.register(r'medicines', MedicineViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'pharmacists', PharmacistViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'deliveries', DeliveryViewSet)
router.register(r'delivery-details', DeliveryDetailsViewSet)
router.register(r'sales', SaleViewSet)
router.register(r'sale-details', SaleDetailsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('report/', report, name='report'),
]