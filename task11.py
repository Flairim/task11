from collections import UserDict
from datetime import date, datetime


class PhoneValueError(Exception):
    ...

class NoNameError(Exception):
    ...

class NoPhoneError(Exception):
    ...

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    ...

class Birthday(Field):
    def __init__(self, value):
        self.value = value
    
    @property
    def birthday(self):
        return self.value
    
    @birthday.setter
    def birthday(self, new_value) -> datetime:
        if new_value:
            self.value = date.fromisoformat(new_value)

class Phone(Field):
    def __init__(self, value:str):
        self._value = value
        
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value):
        if len(new_value) != 10:
            raise ValueError("Phone must be 10 symbols")
        if not new_value.isdigit():
            raise ValueError("Phone must include only numbers")
        self._value = new_value
    

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def add_phone(self, phone:Phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == phone:
                self.phones[i] = Phone(new_phone)
                return None
        raise ValueError("This phone phone does not exist")
        
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
            else:
                continue
    
    def days_to_birthday(self):
        today = date.today()
        today_year = today.year
        
        if self.birthday:
            b = date.fromisoformat(str(self.birthday))
            if today > b:
                b = b.replace(year = today_year + 1)
                return (b - date.today()).days
            elif today <= b:
                b = b.replace(year = today_year)
                return (b - date.today()).days
        return f"There is no birthday input for {self.name}."
    
    def __repr__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday on {self.birthday}"

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday on {self.birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name:str):
        return self.data[name]
        
    def delete(self, name):
        if name in self.data:
            self.data.pop(name)
        else:
            return ValueError(f"{name} is not exist")
        
    def iterator(self, n = 2):
        return Iterable(n, self.data)
    

class Iterable:
    def __init__(self, n, databook):
        self._n = n
        self._databook = databook
        self._start = 0
        self._end = len(self._databook)
    
    def __iter__(self):
        return self
    

    def __next__(self):
        if self._start < self._end:
            self._start += self._n
            result = self._databook[self._start-self._n:self._start]
            return result
        raise StopIteration




def main():
    book = AddressBook()

    john_record = Record("John", "1998-10-29")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.days_to_birthday()

    book.add_record(john_record)

    jane_record = Record("Jane", "1980-10-01")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)
    
    tol_record = Record("Aleks", "1973-06-09")
    tol_record.add_phone("0952811340")
    book.add_record(tol_record)

    for name, record in book.data.items():
        print(record)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john) 
    print(tol_record.days_to_birthday())
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")
    print(book.data.items())
    iterator = book.iterator(1)
    print(iterator)
    book.delete("Jane")

if __name__ == '__main__':
    main()