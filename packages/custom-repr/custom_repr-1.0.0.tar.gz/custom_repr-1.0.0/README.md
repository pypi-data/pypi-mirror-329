# Custom Repr

A simple decorator to add pretty representation to Python classes.

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