from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic, Optional, Type, Any
from django.db import models, transaction

T = TypeVar('T', bound=models.Model)

# ІНТ РЕПОЗИТОРІЮ
class IRepository(Generic[T], ABC):
    @abstractmethod
    def get_all(self) -> List[T]:
        pass
    
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        pass
    
    @abstractmethod
    def create(self, **kwargs) -> T:
        pass
    
    @abstractmethod
    def update(self, id: int, **kwargs) -> Optional[T]:
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        pass


class BaseRepository(IRepository[T]):
    def __init__(self, model_class: Type[T]):
        self.model_class = model_class
    
    def get_all(self) -> List[T]:
        try:
            return list(self.model_class.objects.all())
        except Exception as e:
            print(f"Помилка отримання всіх {self.model_class.__name__}: {e}")
            return []
    
    def get_by_id(self, id: int) -> Optional[T]:
        try:
            return self.model_class.objects.get(id=id)
        except (self.model_class.DoesNotExist, Exception):
            try:
                return self.model_class.objects.get(medicine_id=id)
            except self.model_class.DoesNotExist:
                print(f"{self.model_class.__name__} з ID {id} не знайдено")
                return None
            except Exception as e:
                print(f"Помилка отримання {self.model_class.__name__}: {e}")
                return None
    
    def create(self, **kwargs) -> T:
        try:
            with transaction.atomic():
                return self.model_class.objects.create(**kwargs)
        except Exception as e:
            print(f"Помилка створення {self.model_class.__name__}: {e}")
            raise
    
    def update(self, id: int, **kwargs) -> Optional[T]:
        try:
            instance = self.get_by_id(id)
            if instance:
                for key, value in kwargs.items():
                    setattr(instance, key, value)
                instance.save()
                return instance
            return None
        except Exception as e:
            print(f"Помилка оновлення {self.model_class.__name__}: {e}")
            return None
    
    def delete(self, id: int) -> bool:
        try:
            instance = self.get_by_id(id)
            if instance:
                instance.delete()
                return True
            return False
        except Exception as e:
            print(f"Помилка видалення {self.model_class.__name__}: {e}")
            return False
    
    def filter(self, **kwargs) -> List[T]:
        try:
            return list(self.model_class.objects.filter(**kwargs))
        except Exception as e:
            print(f"Помилка фільтрації {self.model_class.__name__}: {e}")
            return []


# РЕПОЗИТОРІЇ
from .models import Medicine, Customer, Pharmacist

class MedicineRepository(BaseRepository):
    def __init__(self):
        super().__init__(Medicine)
    
    def get_medicines_by_category(self, category: str) -> List[Medicine]:
        return self.filter(category=category)
    
    def get_medicines_need_prescription(self) -> List[Medicine]:
        return self.filter(prescription_required=True)


class CustomerRepository(BaseRepository):
    def __init__(self):
        super().__init__(Customer)
    
    def get_customers_with_discount(self) -> List[Customer]:
        return self.filter(discount_card=True)
    
    def get_customer_by_phone(self, phone: str) -> Optional[Customer]:
        customers = self.filter(phone=phone)
        return customers[0] if customers else None


class PharmacistRepository(BaseRepository):
    def __init__(self):
        super().__init__(Pharmacist)
    
    def get_pharmacists_by_position(self, position: str) -> List[Pharmacist]:
        return self.filter(position=position)


# ЄДИНА ТОЧКА ДОСТУПУ
class RepositoryFactory:
    @staticmethod
    def get_medicine_repo() -> MedicineRepository:
        return MedicineRepository()
    
    @staticmethod
    def get_customer_repo() -> CustomerRepository:
        return CustomerRepository()
    
    @staticmethod
    def get_pharmacist_repo() -> PharmacistRepository:
        return PharmacistRepository()