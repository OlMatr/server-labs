from django.db import models

class Medicine(models.Model):
    """Ліки"""
    medicine_id = models.AutoField(primary_key=True)
    medicine_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, blank=True, null=True)
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_in_stock = models.IntegerField(default=0)
    expiration_date = models.DateField(blank=True, null=True)
    prescription_required = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'Medicine'
        verbose_name = 'Ліки'
        verbose_name_plural = 'Ліки'
        managed = False
    
    def __str__(self):
        return self.medicine_name


class Supplier(models.Model):
    """Постачальники"""
    supplier_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        db_table = 'Supplier'
        verbose_name = 'Постачальник'
        verbose_name_plural = 'Постачальники'
    
    def __str__(self):
        return self.name


class Delivery(models.Model):
    """Поставки"""
    STATUS_CHOICES = [
        ('В дорозі', 'В дорозі'),
        ('Отримано', 'Отримано'),
        ('Скасовано', 'Скасовано'),
    ]
    
    delivery_id = models.AutoField(primary_key=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    delivery_date = models.DateField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='В дорозі')
    
    class Meta:
        db_table = 'Delivery'
        verbose_name = 'Поставка'
        verbose_name_plural = 'Поставки'
    
    def __str__(self):
        return f"Поставка #{self.delivery_id}"


class DeliveryDetails(models.Model):
    """Деталі поставок"""
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'Delivery_Details'
        verbose_name = 'Деталь поставки'
        verbose_name_plural = 'Деталі поставок'
        unique_together = ('delivery', 'medicine')
    
    def __str__(self):
        return f"{self.medicine.medicine_name} - {self.quantity} шт."


class Customer(models.Model):
    """Клієнти"""
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    discount_card = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'Customer'
        verbose_name = 'Клієнт'
        verbose_name_plural = 'Клієнти'
    
    def __str__(self):
        return self.name


class Pharmacist(models.Model):
    """Фармацевти"""
    pharmacist_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    contact_email = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        db_table = 'Pharmacist'
        verbose_name = 'Фармацевт'
        verbose_name_plural = 'Фармацевти'
    
    def __str__(self):
        return self.name


class Sale(models.Model):
    """Продажі"""
    sale_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    pharmacist = models.ForeignKey(Pharmacist, on_delete=models.CASCADE, blank=True, null=True)
    sale_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    class Meta:
        db_table = 'Sale'
        verbose_name = 'Продаж'
        verbose_name_plural = 'Продажі'
    
    def __str__(self):
        return f"Продаж #{self.sale_id}"


class SaleDetails(models.Model):
    """Деталі продажів"""
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'Sale_Details'
        verbose_name = 'Деталь продажу'
        verbose_name_plural = 'Деталі продажів'
        unique_together = ('sale', 'medicine')
    
    def __str__(self):
        return f"{self.medicine.medicine_name} - {self.quantity} шт."