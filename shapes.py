from abc import ABC, abstractmethod
import math

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

    def __str__(self) -> str:
        return f"A shape with area: {self.area()}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(area={self.area()})"

def validate_positive(value: float) -> float:
    if value <= 0:
        raise ValueError("Value must be positive")
    return value

class Rectangle(Shape):
    def __init__(self, width: float, height: float) -> None:
        self.width = validate_positive(width)
        self.height = validate_positive(height)

    def area(self) -> float:
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius: float) -> None:
        self.radius = validate_positive(radius)

    def area(self) -> float:
        return math.pi * (self.radius ** 2)




