# Custom Repr

A lightweight Python library to automatically generate clean __repr__ methods for all your user-declared classes.

## Installation

```sh
pip install custom-repr
```

## Usage

```python
import custom_repr

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

person = Person("John", 30)

print(person)  # Person(name: "John", age: 30)