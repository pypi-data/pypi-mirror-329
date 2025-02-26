# Custom Repr Library

A lightweight Python library designed to offer a custom representation for user-defined classes. This library enables users to visualize class attributes and methods with enhanced formatting using the Rich library. Please be aware that this library employs monkey patching so it should be use with caution.

## Installation

To install the library, use pip:

```bash
pip install custom-repr
```

## Usage

### Basic Usage

To use the custom representation, simply import the library:

```python
import custom_repr

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello, my name is {self.name}."

# Create an instance
person = Person("Alice", 30)

print(person) # The output will be: 
# Person => { name: "Alice", age: 30 }
# [ greet() ] 
```

### Configuration

You can configure the output format of the custom representation using the `custom_repr_config` function. This function allows you to choose whether to display attributes, methods, or both.

#### Function Signature

```python
from custom_repr import custom_repr_config

custom_repr_config(attributes=True, methods=True)
```

#### Examples

- **Show both attributes and methods** (default behavior):

  ```python
  custom_repr_config(True, True)
  ```

- **Show only attributes**:

  ```python
  custom_repr_config(True, False)
  ```

- **Show only methods**:

  ```python
  custom_repr_config(False, True)
  ```

- **Show only the class name**:

  ```python
  custom_repr_config(False, False)
  ```

### Example

```python
from custom_repr import custom_repr_config

# Configure to show only attributes
custom_repr_config(True, False)

class Car:
    def __init__(self, make, model):
        self.make = make
        self.model = model

    def drive(self):
        return "Vroom!"

car = Car("Toyota", "Corolla")
print(car) # Outputs: Car => { make: "Toyota", model: "Corolla" }

# Configure to show only the class name
custom_repr_config(False, False)
print(car)  # Outputs: Car
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.