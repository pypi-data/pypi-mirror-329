from enum import Enum

import chex
import jax.numpy as jnp
from beartype import beartype
from beartype.typing import Callable, Sequence
from jaxtyping import Array, Bool, Float, Int, jaxtyped

from jaxvmas.equinox_utils import (
    equinox_filter_cond_return_dynamic,
)
from jaxvmas.simulator.core.jax_vectorized_object import (
    JaxVectorizedObject,
    batch_axis_dim,
    env_index_dim,
    pos_dim,
)
from jaxvmas.simulator.core.shapes import Shape, Sphere
from jaxvmas.simulator.core.states import EntityState
from jaxvmas.simulator.rendering import Geom
from jaxvmas.simulator.utils import (
    Color,
    JaxUtils,
)


@jaxtyped(typechecker=beartype)
class Entity(JaxVectorizedObject):
    state: EntityState

    gravity: Float[Array, f"{batch_axis_dim} {pos_dim}"] | None

    name: str
    id: int
    movable: bool
    rotatable: bool
    collide: bool
    density: float
    mass: float
    shape: Shape
    v_range: float
    max_speed: float
    color: Enum
    is_joint: bool
    drag: float
    linear_friction: float
    angular_friction: float
    collision_filter: Callable[["Entity"], Bool[Array, "1"]]

    goal: str
    _render: Bool[Array, f"{batch_axis_dim}"] | None

    @classmethod
    @chex.assert_max_traces(0)
    def create(
        cls,
        name: str,
        movable: bool = False,
        rotatable: bool = False,
        collide: bool = True,
        density: float = 25.0,  # Unused for now
        mass: float = 1.0,
        shape: Shape | None = None,
        v_range: float = jnp.nan,
        max_speed: float = jnp.nan,
        color=Color.GRAY,
        is_joint: bool = False,
        drag: float = jnp.nan,
        linear_friction: float = jnp.nan,
        angular_friction: float = jnp.nan,
        gravity: float | Sequence[float] | None = None,
        collision_filter: Callable[["Entity"], Bool[Array, "1"]] = lambda _: True,
    ):
        if shape is None:
            shape = Sphere()
        # name
        name = name
        # entity can move / be pushed
        movable = movable
        # entity can rotate
        rotatable = rotatable
        # entity collides with others
        collide = collide
        # material density (affects mass)
        density = density
        # mass
        mass = mass
        # max speed
        max_speed = max_speed
        v_range = v_range
        # color
        assert isinstance(color, Enum), f"Color must be a Enum, got {type(color)}"
        color = color
        # shape
        shape = shape
        # is joint
        is_joint = is_joint
        # collision filter
        collision_filter = collision_filter
        # drag
        drag = drag
        # friction
        linear_friction = linear_friction
        angular_friction = angular_friction
        # gravity
        # if gravity is None:
        #     gravity = jnp.zeros((batch_dim, dim_p))
        # else:
        if gravity is not None:
            gravity = jnp.asarray(gravity)
        # entity goal
        goal = ""
        # Render the entity
        _render = None
        state = EntityState.create()

        return cls(
            None,
            state,
            gravity,
            name,
            -1,  # id
            movable,
            rotatable,
            collide,
            density,
            mass,
            shape,
            v_range,
            max_speed,
            color,
            is_joint,
            drag,
            linear_friction,
            angular_friction,
            collision_filter,
            goal,
            _render,
        )

    @property
    def is_rendering(self):
        if self._render is None:
            self.reset_render()
        return self._render

    @property
    def moment_of_inertia(self):
        return self.shape.moment_of_inertia(self.mass)

    def replace(self, **kwargs) -> "Entity":
        if "is_rendering" in kwargs:
            is_rendering = kwargs.pop("is_rendering")
            kwargs["_render"] = is_rendering

        return JaxVectorizedObject.replace(self, **kwargs)

    @jaxtyped(typechecker=beartype)
    def reset_render(self):
        return self.replace(_render=jnp.full((self.batch_dim,), True))

    @jaxtyped(typechecker=beartype)
    def collides(self, entity: "Entity"):
        # Here collision_filter is a static variable but entity is not.
        # So we need to use equinox_filter_cond to handle this.
        return equinox_filter_cond_return_dynamic(
            self.collide,
            lambda entity: jnp.asarray(self.collision_filter(entity)),
            lambda entity: jnp.asarray(False),
            entity,
        )

    @chex.assert_max_traces(0)
    @jaxtyped(typechecker=beartype)
    def _spawn(self, id: int, *, batch_dim: int, dim_p: int, **kwargs) -> "Entity":
        if self.gravity is not None:
            chex.assert_shape(self.gravity, (batch_dim, dim_p))
        _render = jnp.full((batch_dim,), True)

        return self.replace(
            batch_dim=batch_dim,
            id=id,
            _render=_render,
            state=self.state._spawn(batch_dim=batch_dim, dim_p=dim_p, **kwargs),
        )

    @jaxtyped(typechecker=beartype)
    def _reset(
        self,
        env_index: Int[Array, f"{env_index_dim}"] | None = None,
    ):
        return self.replace(state=self.state._reset(env_index))

    @jaxtyped(typechecker=beartype)
    def set_pos(
        self,
        pos: Array,
        batch_index: Int[Array, f"{env_index_dim}"] | None = None,
    ):
        return self._set_state_property("pos", pos, batch_index)

    @jaxtyped(typechecker=beartype)
    def set_vel(
        self,
        vel: Array,
        batch_index: Int[Array, f"{env_index_dim}"] | None = None,
    ):
        return self._set_state_property("vel", vel, batch_index)

    @jaxtyped(typechecker=beartype)
    def set_rot(
        self,
        rot: Array,
        batch_index: Int[Array, f"{env_index_dim}"] | None = None,
    ):
        return self._set_state_property("rot", rot, batch_index)

    @jaxtyped(typechecker=beartype)
    def set_ang_vel(
        self,
        ang_vel: Array,
        batch_index: Int[Array, f"{env_index_dim}"] | None = None,
    ):
        return self._set_state_property("ang_vel", ang_vel, batch_index)

    @jaxtyped(typechecker=beartype)
    def _set_state_property(
        self,
        prop_name: str,
        new: Array,
        batch_index: Int[Array, f"{env_index_dim}"] | None = None,
    ):
        chex.assert_scalar(self.batch_dim)

        def batch_index_is_nan(
            batch_index: Int[Array, f"{env_index_dim}"] | None,
            new: Array,
            value: Array,
        ):
            ret = new
            if len(new.shape) > 1 and new.shape[0] == self.batch_dim:
                ret = new
            else:
                if new.ndim == value.ndim - 1:
                    new = new[None]
                ret = new.repeat(self.batch_dim, 0)
            return ret

        def batch_index_is_not_nan(
            batch_index: Int[Array, f"{env_index_dim}"] | None,
            new: Array,
            value: Array,
        ):
            new = jnp.broadcast_to(
                new, value.shape
            )  # This should never happen. Here to make jax jit happy

            new_value = JaxUtils.where_from_index(batch_index, new, value)
            return new_value

        prop_value = jnp.where(
            batch_index is None,
            batch_index_is_nan(batch_index, new, getattr(self.state, prop_name)),
            batch_index_is_not_nan(batch_index, new, getattr(self.state, prop_name)),
        )
        new_state = self.state.replace(**{prop_name: prop_value})
        # there was a notify_observers call in the past, so we need to notify observers manually
        return self.replace(state=new_state)

    @chex.assert_max_traces(0)
    def render(
        self,
        env_index: int = 0,
    ) -> "list[Geom]":
        from jaxvmas.simulator import rendering

        if not self.is_rendering[env_index]:
            return []
        geom = self.shape.get_geometry()
        xform = rendering.Transform()
        geom.add_attr(xform)

        xform.set_translation(*self.state.pos[env_index])
        xform.set_rotation(self.state.rot[env_index].item())

        color = self.color
        if isinstance(color, Array) and len(color.shape) > 1:
            color = color[env_index]
        geom.set_color(*color.value)

        return [geom]
