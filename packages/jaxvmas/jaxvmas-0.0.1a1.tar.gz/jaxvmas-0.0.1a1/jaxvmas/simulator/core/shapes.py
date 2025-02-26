from abc import ABC, abstractmethod
from enum import Enum

import jax.numpy as jnp
from beartype import beartype
from jaxtyping import Array, jaxtyped

from jaxvmas.simulator.rendering import Geom
from jaxvmas.simulator.utils import X, Y


class ShapeType(Enum):
    BOX = "box"
    SPHERE = "sphere"
    LINE = "line"


class Shape(ABC):
    def __init__(self, type: ShapeType):
        self.type = type

    @abstractmethod
    def moment_of_inertia(self, mass: float) -> float:
        raise NotImplementedError

    @abstractmethod
    def get_delta_from_anchor(self, anchor: tuple[float, float]) -> Array:
        raise NotImplementedError

    @abstractmethod
    def get_geometry(self) -> "Geom":
        raise NotImplementedError

    @abstractmethod
    def circumscribed_radius(self) -> float:
        raise NotImplementedError


class Box(Shape):
    def __init__(self, length: float = 0.3, width: float = 0.1, hollow: bool = False):
        super().__init__(ShapeType.BOX)
        assert length > 0, f"Length must be > 0, got {length}"
        assert width > 0, f"Width must be > 0, got {length}"
        self._length = length
        self._width = width
        self.hollow = hollow

    @property
    def length(self):
        return self._length

    @property
    def width(self):
        return self._width

    @jaxtyped(typechecker=beartype)
    def get_delta_from_anchor(self, anchor: tuple[float, float]) -> Array:
        return jnp.asarray([anchor[X] * self.length / 2, anchor[Y] * self.width / 2])

    @jaxtyped(typechecker=beartype)
    def moment_of_inertia(self, mass: float):
        return (1 / 12) * mass * (self.length**2 + self.width**2)

    @jaxtyped(typechecker=beartype)
    def circumscribed_radius(self):
        return jnp.sqrt((self.length / 2) ** 2 + (self.width / 2) ** 2)

    @jaxtyped(typechecker=beartype)
    def get_geometry(self) -> "Geom":
        from jaxvmas.simulator import rendering

        l, r, t, b = (
            -self.length / 2,
            self.length / 2,
            self.width / 2,
            -self.width / 2,
        )
        return rendering.make_polygon([(l, b), (l, t), (r, t), (r, b)])


class Sphere(Shape):
    def __init__(self, radius: float = 0.05):
        super().__init__(ShapeType.SPHERE)
        assert radius > 0, f"Radius must be > 0, got {radius}"
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @jaxtyped(typechecker=beartype)
    def get_delta_from_anchor(self, anchor: tuple[float, float]) -> Array:
        delta = jnp.asarray([anchor[X] * self.radius, anchor[Y] * self.radius])
        delta_norm = jnp.linalg.vector_norm(delta)
        # Use jnp.where instead of if statement for jit compatibility
        delta = jnp.where(
            delta_norm > self.radius, delta / (delta_norm * self.radius), delta
        )
        return delta

    @jaxtyped(typechecker=beartype)
    def moment_of_inertia(self, mass: float):
        return (1 / 2) * mass * self.radius**2

    def circumscribed_radius(self):
        return self.radius

    @jaxtyped(typechecker=beartype)
    def get_geometry(self) -> "Geom":
        from jaxvmas.simulator import rendering

        return rendering.make_circle(self.radius)


class Line(Shape):
    def __init__(self, length: float = 0.5):
        super().__init__(ShapeType.LINE)
        assert length > 0, f"Length must be > 0, got {length}"
        self._length = length
        self._width = 2

    @property
    def length(self):
        return self._length

    @property
    def width(self):
        return self._width

    @jaxtyped(typechecker=beartype)
    def moment_of_inertia(self, mass: float) -> float:
        return (1 / 12) * mass * (self.length**2)

    @jaxtyped(typechecker=beartype)
    def circumscribed_radius(self) -> float:
        return self.length / 2

    @jaxtyped(typechecker=beartype)
    def get_delta_from_anchor(self, anchor: tuple[float, float]) -> Array:
        return jnp.asarray([anchor[X] * self.length / 2, 0.0])

    def get_geometry(self) -> "Geom":
        from jaxvmas.simulator import rendering

        return rendering.Line(
            (-self.length / 2, 0),
            (self.length / 2, 0),
            width=self.width,
        )
