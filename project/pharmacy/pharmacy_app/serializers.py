from rest_framework import serializers
from .models import Medicine, Customer, Pharmacist, Supplier, Delivery, DeliveryDetails, Sale, SaleDetails

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

# Serializer для фармацевтів  
class PharmacistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacist
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class DeliverySerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    
    class Meta:
        model = Delivery
        fields = '__all__'

class DeliveryDetailsSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.medicine_name', read_only=True)
    delivery_info = serializers.CharField(source='delivery.delivery_date', read_only=True)
    
    class Meta:
        model = DeliveryDetails
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    pharmacist_name = serializers.CharField(source='pharmacist.name', read_only=True)
    
    class Meta:
        model = Sale
        fields = '__all__'

class SaleDetailsSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.medicine_name', read_only=True)
    sale_info = serializers.CharField(source='sale.sale_date', read_only=True)
    
    class Meta:
        model = SaleDetails
        fields = '__all__'