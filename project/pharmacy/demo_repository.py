import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy.settings')
django.setup()

from pharmacy_app.repositories import RepositoryFactory

med_repo = RepositoryFactory.get_medicine_repo()
cust_repo = RepositoryFactory.get_customer_repo()
pharm_repo = RepositoryFactory.get_pharmacist_repo()

print("\n1. MedicineRepository")
print("-" * 40)
medicines = med_repo.get_all()
print(f"get_all() - записів: {len(medicines)}")
for med in medicines[:10]:
    print(f"  {med.medicine_name} - {med.price} грн")

if medicines:
    target_id = medicines[0].medicine_id
    found = med_repo.get_by_id(target_id)
    if found:
        print(f"get_by_id({target_id}): {found.medicine_name}")

print("\n2. CustomerRepository")
print("-" * 40)
customers = cust_repo.get_all()
print(f"get_all() - клієнтів: {len(customers)}")
print(f"З дисконтом: {len(cust_repo.get_customers_with_discount())}")

print("\n3. PharmacistRepository")
print("-" * 40)
pharmacists = pharm_repo.get_all()
print(f"get_all() - фармацевтів: {len(pharmacists)}")
for pharm in pharmacists:
    print(f"  {pharm.name} - {pharm.position}")

print("\n4. Створення нового запису")
print("-" * 40)
try:
    new = med_repo.create(
        medicine_name="Тестові ліки номер 2",
        category="Тест",
        manufacturer="Тест",
        price=150.00,
        quantity_in_stock=20,
        prescription_required=False
    )
    print(f"Створено: {new.medicine_name}")
    print(f"Тепер ліків: {len(med_repo.get_all())}")
except Exception as e:
    print(f"Помилка: {e}")


print("\n5. Видалення запису")
print("-" * 40)

all_meds = med_repo.get_all()
if all_meds:
    last_id = all_meds[-1].medicine_id
    print(f"Спробуємо видалити запис ID={last_id}")
    
    count_before = len(all_meds)
    deleted = med_repo.delete(last_id)
    
    if deleted:
        count_after = len(med_repo.get_all())
        print(f"✅ Видалено успішно!")
        print(f"   Було: {count_before}, Стало: {count_after}")
    else:
        print("❌ Не вдалося видалити")



print("\n" + "=" * 60)
print(f"Ліки: {len(med_repo.get_all())}")
print(f"Клієнти: {len(cust_repo.get_all())}")
print(f"Фармацевти: {len(pharm_repo.get_all())}")
print("=" * 60)