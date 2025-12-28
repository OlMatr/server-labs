from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Medicine, Customer, Pharmacist, Supplier, Delivery, DeliveryDetails, Sale, SaleDetails
from .serializers import MedicineSerializer, CustomerSerializer, PharmacistSerializer, SupplierSerializer, DeliverySerializer, DeliveryDetailsSerializer, SaleSerializer, SaleDetailsSerializer
from .repositories import RepositoryFactory

class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

# API фармацевтів
class PharmacistViewSet(viewsets.ModelViewSet):
    queryset = Pharmacist.objects.all()
    serializer_class = PharmacistSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer

class DeliveryDetailsViewSet(viewsets.ModelViewSet):
    queryset = DeliveryDetails.objects.all()
    serializer_class = DeliveryDetailsSerializer

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

class SaleDetailsViewSet(viewsets.ModelViewSet):
    queryset = SaleDetails.objects.all()
    serializer_class = SaleDetailsSerializer



@api_view(['GET'])  # Агрегований звіт
def report(request):
    """Спрощений звіт аптеки"""
    med_repo = RepositoryFactory.get_medicine_repo()
    cust_repo = RepositoryFactory.get_customer_repo()
    pharm_repo = RepositoryFactory.get_pharmacist_repo()
    
    all_medicines = med_repo.get_all()
    
    report_data = {
        'summary': {
            'total_medicines': len(all_medicines),
            'total_customers': len(cust_repo.get_all()),
            'total_pharmacists': len(pharm_repo.get_all()),
            'customers_with_discount': len(cust_repo.get_customers_with_discount()),
        },
        
        'medicines_summary': {
            'by_category': {},
            'need_prescription': len([m for m in all_medicines if m.prescription_required]),
            'average_price': str(sum([m.price for m in all_medicines]) / len(all_medicines) if all_medicines else 0),
        },
        
        'top_3_medicines': [
            {
                'id': med.medicine_id,
                'name': med.medicine_name,
                'price': str(med.price),
                'stock': med.quantity_in_stock
            }
            for med in all_medicines[:3]
        ]
    }
    
    for medicine in all_medicines:
        category = medicine.category or 'Без категорії'
        report_data['medicines_summary']['by_category'][category] = \
            report_data['medicines_summary']['by_category'].get(category, 0) + 1
    
    return Response(report_data)

