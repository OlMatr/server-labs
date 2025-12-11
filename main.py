class Medicine:
    def __init__(self, name, price, quantity):
        self._name = name
        self._price = price
        self._quantity = quantity

    @property
    def price(self):
        return self._price

    @property
    def name(self):
        return self._name

    def add_stock(self, amount):
        self._quantity += amount
        return self._quantity

    def info(self):
        return f"{self._name}: {self._price}грн, {self._quantity}шт"

    @staticmethod
    def check_price(price):
        return "Дорогий" if price > 100 else "Дешевий"



class Supplier: # бат кл 2
    def __init__(self, supplier_name):
        self.supplier_name = supplier_name
    
    def get_supplier(self):
        return self.supplier_name


class PrescriptionMedicine(Medicine): # Доч кл 1
    def __init__(self, name, price, quantity, doctor):
        super().__init__(name, price, quantity)
        self.doctor = doctor
    
    def info(self):
        return f"Рецептурний: {self._name}, лікар: {self.doctor}"


class ImportedMedicine(Medicine, Supplier): # Доч кл 2
    def __init__(self, name, price, quantity, supplier, country):
        Medicine.__init__(self, name, price, quantity)
        Supplier.__init__(self, supplier)
        self.country = country
    
    def info(self):
        return f"Імпортний: {self._name} з {self.country}"


if __name__ == "__main__":

    med1 = Medicine("Парацетамол", 30, 60)
    med2 = Medicine("Аспірин", 25, 50)
    
    pres_med = PrescriptionMedicine("Антибіотик", 150, 30, "Григорій")
    import_med = ImportedMedicine("Вітамін С", 80, 200, "Фармако", "Німеччина")
    
    print("Інформація про ліки:")
    print(med1.info())
    print(med2.info())
    print(pres_med.info())
    print(import_med.info())
    
    print("\nЦіни ліків:")
    print(f"{med1.name}: {med1.price}грн")
    print(f"{pres_med.name}: {pres_med.price}грн")
    
    print("\nПоповнення запасу:")
    med1.add_stock(50)
    print(f"Новий запас {med1.name}: {med1.info()}")
    
    print("\nПеревірка цін:")
    print(f"Парацетамол: {Medicine.check_price(med1.price)}")
    print(f"Антибіотик: {Medicine.check_price(pres_med.price)}")
    
    print(f"\nПостачальник імпортних ліків: {import_med.get_supplier()}")
    
    print("\nКілька імпортних ліків:")
    import_med2 = ImportedMedicine("Ібупрофен", 60, 150, "Фармако", "Польща")
    print(import_med.info())
    print(import_med2.info())
    
    print("\nВесь асортимент:")
    all_medicines = [med1, med2, pres_med, import_med, import_med2]
    for medicine in all_medicines:
        print(f"  - {medicine.info()}")