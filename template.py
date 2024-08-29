"""
This module demonstrates advanced Python features including error handling, method overloading,
special methods, built-in functions, decorators, method overrides, and dependency injection.
"""

from abc import ABC, abstractmethod
from typing import Type, Union, Callable
import math


class MetaShape(type):
    """
    A metaclass for shapes that enforces the implementation of the `area` method.

    Attributes:
        name (str): The name of the shape.
    """

    def __init__(cls: Type, name: str, bases: tuple, dct: dict) -> None:
        """
        Initialize the metaclass.

        Args:
            cls: The class being initialized.
            name: The name of the class.
            bases: Tuple of base classes.
            dct: Dictionary of class attributes.

        Raises:
            TypeError: If the class does not implement the `area` method.
        """
        super().__init__(name, bases, dct)
        if "area" not in dct:
            raise TypeError(f"{name} must implement the `area` method")


class Shape(ABC):
    """
    Abstract base class for all shapes.

    This class uses the `MetaShape` metaclass to enforce that any subclass must
    implement the `area` method.

    Methods:
        area: Abstract method to calculate the area of the shape.
    """

    @abstractmethod
    def area(self) -> float:
        """
        Abstract method to calculate the area of the shape.

        Subclasses must implement this method.

        Returns:
            float: The area of the shape.
        """
        pass

    def __str__(self) -> str:
        """
        Return a string representation of the shape.

        Returns:
            str: Description of the shape, including its area.
        """
        return f"A shape with area: {self.area()}"

    def __repr__(self) -> str:
        """
        Return an official string representation of the shape.

        Returns:
            str: Official representation of the shape, including its area.
        """
        return f"{self.__class__.__name__}(area={self.area()})"


def validate_positive(value: float) -> float:
    """
    Decorator to ensure a value is positive.

    Args:
        value (float): The value to be validated.

    Returns:
        float: The validated value.

    Raises:
        ValueError: If the value is not positive.
    """
    if value <= 0:
        raise ValueError("Value must be positive")
    return value


class Rectangle(Shape):
    """
    A concrete class representing a rectangle.

    Inherits from `Shape` and implements the `area` method.

    Attributes:
        width (float): The width of the rectangle.
        height (float): The height of the rectangle.

    Methods:
        area: Calculates the area of the rectangle.
    """

    def __init__(self, width: float, height: float) -> None:
        """
        Initialize a new `Rectangle` instance with dependency injection for validation.

        Args:
            width (float): The width of the rectangle.
            height (float): The height of the rectangle.
        """
        self.width = validate_positive(width)  # Use decorator to validate width
        self.height = validate_positive(height)  # Use decorator to validate height

    def area(self) -> float:
        """
        Calculate the area of the rectangle.

        Returns:
            float: The area of the rectangle (width * height).
        """
        return self.width * self.height

    def __add__(self, other: "Rectangle") -> "Rectangle":
        """
        Overload the + operator to combine two rectangles into a larger rectangle.

        Args:
            other (Rectangle): Another rectangle to combine with.

        Returns:
            Rectangle: A new rectangle that is the sum of the two.

        Raises:
            TypeError: If the other object is not a Rectangle.
        """
        if not isinstance(other, Rectangle):
            raise TypeError("Operands must be of type Rectangle")
        return Rectangle(self.width + other.width, self.height + other.height)


class Circle(Shape):
    """
    A concrete class representing a circle.

    Inherits from `Shape` and implements the `area` method.

    Attributes:
        radius (float): The radius of the circle.

    Methods:
        area: Calculates the area of the circle.
    """

    def __init__(self, radius: float) -> None:
        """
        Initialize a new `Circle` instance with dependency injection for validation.

        Args:
            radius (float): The radius of the circle.
        """
        self.radius = validate_positive(radius)  # Use decorator to validate radius

    def area(self) -> float:
        """
        Calculate the area of the circle.

        Returns:
            float: The area of the circle (π * radius^2).
        """
        return math.pi * (self.radius ** 2)

    def __eq__(self, other: "Circle") -> bool:
        """
        Overload the == operator to compare circles based on their radii.

        Args:
            other (Circle): Another circle to compare with.

        Returns:
            bool: True if both circles have the same radius, otherwise False.

        Raises:
            TypeError: If the other object is not a Circle.
        """
        if not isinstance(other, Circle):
            raise TypeError("Operands must be of type Circle")
        return math.isclose(self.radius, other.radius)


def print_area(shape: Shape) -> None:
    """
    Print the area of a given shape.

    This function demonstrates polymorphism by accepting any object that
    inherits from `Shape` and calling its `area` method.

    Args:
        shape (Shape): An instance of a subclass of `Shape`.

    Raises:
        TypeError: If the provided object does not inherit from `Shape`.
    """
    if not isinstance(shape, Shape):
        raise TypeError("The provided object must be an instance of Shape")

    print(f"The area of the shape is: {shape.area()}")


# Example usage:
if __name__ == "__main__":
    # Create instances of Rectangle and Circle
    rect1 = Rectangle(5.0, 10.0)
    rect2 = Rectangle(3.0, 4.0)
    circle1 = Circle(7.0)
    circle2 = Circle(7.0)

    # Demonstrate operator overloading
    combined_rect = rect1 + rect2
    print(f"Combined rectangle area: {combined_rect.area()}")  # Output: Combined rectangle area: 62.0

    # Demonstrate equality operator overloading
    print(f"Circles are equal: {circle1 == circle2}")  # Output: Circles are equal: True

    # Demonstrate string representations
    print(rect1)  # Output: A shape with area: 50.0
    print(repr(rect1))  # Output: Rectangle(area=50.0)

    # Demonstrate exception handling
    try:
        invalid_circle = Circle(-5.0)
    except ValueError as e:
        print(f"Error: {e}")  # Output: Error: Value must be positive

    # Print areas
    print_area(rect1)  # Output: The area of the shape is: 50.0
    print_area(circle1)  # Output: The area of the shape is: 153.93804002589985


