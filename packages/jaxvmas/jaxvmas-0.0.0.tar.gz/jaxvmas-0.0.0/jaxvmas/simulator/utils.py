#  Copyright (c) 2022-2025.
#  ProrokLab (https://www.proroklab.org/)
#  All rights reserved.

from __future__ import annotations

import os
import warnings
from enum import Enum
from typing import TYPE_CHECKING

import chex
import jax
import jax.numpy as jnp
from beartype import beartype
from jaxtyping import Array, Bool, Float, Int, Scalar, jaxtyped

if TYPE_CHECKING:
    from jaxvmas.simulator.core.entity import Entity
    from jaxvmas.simulator.core.world import World
    from jaxvmas.simulator.rendering import Geom
    from jaxvmas.simulator.scenario import BaseScenario


X = 0
Y = 1
Z = 2
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
VIEWER_DEFAULT_ZOOM = 1.2
INITIAL_VIEWER_SIZE = (700, 700)
LINE_MIN_DIST = 4 / 6e2
COLLISION_FORCE = 100.0
JOINT_FORCE = 130.0
TORQUE_CONSTRAINT_FORCE = 1.0

DRAG = 0.25
LINEAR_FRICTION = 0.0
ANGULAR_FRICTION = 0.0
batch_axis_dim = "batch_axis_dim"
env_index_dim = "env_index_dim"


AGENT_UNBATCHED_ARRAY_TYPE = (
    Float[Array, "..."] | Int[Array, "..."] | Bool[Array, "..."]
)
AGENT_BATCHED_ARRAY_TYPE = (
    Float[Array, f"{batch_axis_dim} ..."]
    | Int[Array, f"{batch_axis_dim} ..."]
    | Bool[Array, f"{batch_axis_dim} ..."]
)

AGENT_ARRAY_TYPE = AGENT_UNBATCHED_ARRAY_TYPE

AGENT_OBS_TYPE = AGENT_ARRAY_TYPE | dict[str, AGENT_ARRAY_TYPE]
AGENT_INFO_TYPE = dict[str, AGENT_ARRAY_TYPE]
AGENT_REWARD_TYPE = AGENT_ARRAY_TYPE

AGENT_PYTREE_TYPE = AGENT_OBS_TYPE | AGENT_INFO_TYPE | AGENT_REWARD_TYPE

OBS_TYPE = list[AGENT_OBS_TYPE] | dict[str, AGENT_OBS_TYPE]
INFO_TYPE = list[AGENT_INFO_TYPE] | dict[str, AGENT_INFO_TYPE]
REWARD_TYPE = list[AGENT_REWARD_TYPE] | dict[str, AGENT_REWARD_TYPE]
DONE_TYPE = AGENT_ARRAY_TYPE

SCENARIO_PYTREE_TYPE = (
    list[OBS_TYPE | REWARD_TYPE | DONE_TYPE | INFO_TYPE]
    | dict[str, OBS_TYPE | REWARD_TYPE | DONE_TYPE | INFO_TYPE]
)


class Color(Enum):
    RED = (0.75, 0.25, 0.25)
    GREEN = (0.25, 0.75, 0.25)
    BLUE = (0.25, 0.25, 0.75)
    LIGHT_GREEN = (0.45, 0.95, 0.45)
    WHITE = (0.75, 0.75, 0.75)
    GRAY = (0.25, 0.25, 0.25)
    BLACK = (0.15, 0.15, 0.15)
    ORANGE = (1.00, 0.50, 0)
    PINK = (0.97, 0.51, 0.75)
    PURPLE = (0.60, 0.31, 0.64)
    YELLOW = (0.87, 0.87, 0)


@jaxtyped(typechecker=beartype)
@chex.assert_max_traces(0)
def _init_pyglet_device():
    available_devices = os.getenv("CUDA_VISIBLE_DEVICES")
    if available_devices is not None and len(available_devices) > 0:
        os.environ["PYGLET_HEADLESS_DEVICE"] = (
            available_devices.split(",")[0]
            if len(available_devices) > 1
            else available_devices
        )


@jaxtyped(typechecker=beartype)
@chex.assert_max_traces(0)
def save_video(name: str, frame_list: list[Array], fps: int):
    """Requires cv2. Saves a list of frames as an MP4 video."""
    import cv2
    import numpy as np

    video_name = name + ".mp4"

    # Produce a video
    video = cv2.VideoWriter(
        video_name,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (frame_list[0].shape[1], frame_list[0].shape[0]),
    )
    for img in frame_list:
        # Convert JAX array to numpy array
        img = np.asarray(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        video.write(img)
    video.release()


@jaxtyped(typechecker=beartype)
@chex.assert_max_traces(0)
def x_to_rgb_colormap(
    x: Array,
    low: float | None = None,
    high: float | None = None,
    alpha: float = 1.0,
    cmap_name: str = "viridis",
    cmap_res: int = 10,
):
    from matplotlib import cm

    colormap = cm.get_cmap(cmap_name, cmap_res)(range(cmap_res))[:, :-1]
    if low is None:
        low = jnp.min(x)
    if high is None:
        high = jnp.max(x)
    x = jnp.clip(x, low, high)
    if high - low > 1e-5:
        x = (x - low) / (high - low) * (cmap_res - 1)
    x_c0_idx = jnp.floor(x).astype(int)
    x_c1_idx = jnp.ceil(x).astype(int)
    x_c0 = colormap[x_c0_idx, :]
    x_c1 = colormap[x_c1_idx, :]
    t = x - x_c0_idx
    rgb = t[:, None] * x_c1 + (1 - t)[:, None] * x_c0
    colors = jnp.concatenate([rgb, alpha * jnp.ones((rgb.shape[0], 1))], axis=-1)
    return colors


@jaxtyped(typechecker=beartype)
def extract_nested_with_index(data: Array | dict[str, Array], index: Int[Scalar, ""]):
    return jax.tree.map(lambda x: x[index], data)


# Define dimension variables for type annotations
dim_p = "dim_p"


class JaxUtils:
    @staticmethod
    @jaxtyped(typechecker=beartype)
    def clamp_with_norm(
        tensor: Float[Array, f"{batch_axis_dim} ..."], max_norm: Float[Scalar, ""]
    ) -> Float[Array, f"{batch_axis_dim} ..."]:
        norm = jnp.linalg.norm(tensor, axis=-1, keepdims=True)
        normalized = (tensor / norm) * max_norm
        return jnp.where(norm > max_norm, normalized, tensor)

    @staticmethod
    @jaxtyped(typechecker=beartype)
    def rotate_vector(
        vector: Float[Array, f"{batch_axis_dim} ..."],
        angle: Float[Array, f"{batch_axis_dim} ..."],
    ) -> Float[Array, f"{batch_axis_dim} ..."]:
        if len(angle.shape) == len(vector.shape):
            angle = angle.squeeze(-1)

        assert vector.shape[:-1] == angle.shape
        assert vector.shape[-1] == 2

        cos = jnp.cos(angle)
        sin = jnp.sin(angle)
        return jnp.stack(
            [
                vector[..., X] * cos - vector[..., Y] * sin,
                vector[..., X] * sin + vector[..., Y] * cos,
            ],
            axis=-1,
        )

    @staticmethod
    @jaxtyped(typechecker=beartype)
    def cross(
        vector_a: Float[Array, f"{batch_axis_dim} ..."],
        vector_b: Float[Array, f"{batch_axis_dim} ..."],
    ) -> Float[Array, f"{batch_axis_dim} ..."]:
        return (
            vector_a[..., X] * vector_b[..., Y] - vector_a[..., Y] * vector_b[..., X]
        )[..., None]

    @staticmethod
    @jaxtyped(typechecker=beartype)
    def compute_torque(
        f: Float[Array, f"{batch_axis_dim} ..."],
        r: Float[Array, f"{batch_axis_dim} ..."],
    ) -> Float[Array, f"{batch_axis_dim} ..."]:
        return JaxUtils.cross(r, f)

    @staticmethod
    @jaxtyped(typechecker=beartype)
    def where_from_index(
        env_index: Int[Array, f"{env_index_dim}"] | None,
        new_value: Array,
        old_value: Array,
    ):
        """If env_index is nan, return new_value, otherwise return old_value in the env_index position and new_value in all other positions.

        Args:
            env_index (Array): The environment index to use.
            new_value (Array): The value to return if env_index is nan or to use in all positions if env_index is not nan.
            old_value (Array): The value to return in env_index position if env_index is not nan.
        """

        # def env_index_is_nan(
        #     reset_index: Bool[Array, f"{batch_dim}"],
        #     new_value: Array,
        #     old_value: Array,
        # ):
        #     return new_value

        # def env_index_is_not_nan(
        #     reset_index: Bool[Array, f"{batch_dim}"],
        #     new_value: Array,
        #     old_value: Array,
        # ):

        #     mask = jnp.zeros_like(old_value, dtype=jnp.bool)
        #     mask = mask.at[reset_index].set(True)
        #     return jnp.where(mask, new_value, old_value)

        batch_size = old_value.shape[0]
        assert new_value.shape[0] == batch_size

        if env_index is None:
            reset_index = jnp.full((batch_size,), True, dtype=jnp.bool)
        else:
            if env_index.ndim == 0:
                reset_index = jnp.full((batch_size,), False, dtype=jnp.bool)
                reset_index = reset_index.at[env_index].set(True)
            elif env_index.ndim <= batch_size:
                reset_index = jnp.full((batch_size,), False, dtype=jnp.bool)
                reset_index = reset_index.at[env_index].set(True)
            else:
                raise ValueError(
                    f"env_index has shape {env_index.shape} but must be a scalar or have shape {batch_size}"
                )

        return jnp.where(
            jnp.broadcast_to(
                jnp.expand_dims(
                    reset_index, axis=tuple(range(1, len(old_value.shape)))
                ),
                old_value.shape,
            ),
            new_value,
            old_value,
        )


class ScenarioUtils:
    @staticmethod
    @jaxtyped(typechecker=beartype)
    def spawn_entities_randomly(
        entities: list[Entity],
        world: World,
        env_index: Int[Scalar, ""] | None,
        min_dist_between_entities: Float[Scalar, ""],
        x_bounds: tuple[int, int],
        y_bounds: tuple[int, int],
        occupied_positions: Array | None = None,
        disable_warn: bool = False,
    ):
        batch_size = world.batch_dim if env_index is None else 1
        if env_index is None:
            env_index = jnp.asarray(-1)

        if occupied_positions is None:
            occupied_positions = jnp.zeros((batch_size, 0, world.dim_p))

        for entity in entities:
            pos = ScenarioUtils.find_random_pos_for_entity(
                occupied_positions,
                env_index,
                world,
                min_dist_between_entities,
                x_bounds,
                y_bounds,
                disable_warn,
            )
            occupied_positions = jnp.concatenate([occupied_positions, pos], axis=1)
            entity.set_pos(pos.squeeze(1), batch_index=env_index)

    # TODO: Fix this
    @staticmethod
    @jaxtyped(typechecker=beartype)
    def find_random_pos_for_entity(
        occupied_positions: Float[Array, f"{batch_axis_dim} n {dim_p}"],
        env_index: Int[Scalar, ""] | None,
        world,
        min_dist_between_entities: float,
        x_bounds: tuple[int, int],
        y_bounds: tuple[int, int],
        disable_warn: bool = False,
        key: jax.Array = jax.random.PRNGKey(0),
    ) -> Float[Array, f"{batch_axis_dim} 1 {dim_p}"]:
        batch_size = world.batch_dim if env_index is None else 1
        key, subkey = jax.random.split(key)

        def body_fn(carry):
            pos, key, tries = carry
            key, x_key, y_key = jax.random.split(key, 3)

            proposed_pos = jnp.concatenate(
                [
                    jax.random.uniform(
                        x_key,
                        (batch_size, 1, 1),
                        minval=x_bounds[0],
                        maxval=x_bounds[1],
                    ),
                    jax.random.uniform(
                        y_key,
                        (batch_size, 1, 1),
                        minval=y_bounds[0],
                        maxval=y_bounds[1],
                    ),
                ],
                axis=-1,
            )

            dist = jnp.linalg.norm(occupied_positions - proposed_pos, axis=-1)
            overlaps = jnp.any(dist < min_dist_between_entities, axis=1)
            new_pos = jnp.where(overlaps[:, None, None], proposed_pos, pos)

            return (new_pos, key, tries + 1)

        def cond_fn(carry):
            pos, _, tries = carry
            has_overlaps = jnp.any(
                jnp.linalg.norm(occupied_positions - pos, axis=-1)
                < min_dist_between_entities
            )
            return has_overlaps & (tries < 50_000)

        init_pos = jnp.zeros((batch_size, 1, 2))
        initial_carry = (init_pos, subkey, 0)

        final_pos, _, tries = jax.lax.while_loop(cond_fn, body_fn, initial_carry)
        return final_pos

    @staticmethod
    @jaxtyped(typechecker=beartype)
    def check_kwargs_consumed(dictionary_of_kwargs: dict, warn: bool = True):
        if len(dictionary_of_kwargs) > 0:
            message = f"Scenario kwargs: {dictionary_of_kwargs} passed but not used by the scenario."
            if warn:
                warnings.warn(
                    message + " This will turn into an error in future versions."
                )
            else:
                raise ValueError(message)

    @staticmethod
    @jaxtyped(typechecker=beartype)
    @chex.assert_max_traces(0)
    def render_agent_indices(
        scenario: BaseScenario,
        env_index: int,
        start_from: int = 0,
        exclude: list = None,
    ) -> list["Geom"]:
        from jaxvmas.simulator import rendering

        aspect_r = scenario.viewer_size[X] / scenario.viewer_size[Y]
        if aspect_r > 1:
            dimensional_ratio = (aspect_r, 1)
        else:
            dimensional_ratio = (1, 1 / aspect_r)

        geoms = []
        for i, entity in enumerate(scenario.world.agents):
            if exclude is not None and entity in exclude:
                continue
            i = i + start_from
            line = rendering.TextLine(
                text=str(i),
                font_size=15,
                x=(
                    (entity.state.pos[env_index, X] * scenario.viewer_size[X])
                    / (scenario.viewer_zoom**2 * dimensional_ratio[X] * 2)
                    + scenario.viewer_size[X] / 2
                ),
                y=(
                    (entity.state.pos[env_index, Y] * scenario.viewer_size[Y])
                    / (scenario.viewer_zoom**2 * dimensional_ratio[Y] * 2)
                    + scenario.viewer_size[Y] / 2
                ),
            )
            geoms.append(line)
        return geoms

    @staticmethod
    @jaxtyped(typechecker=beartype)
    @chex.assert_max_traces(0)
    def plot_entity_rotation(
        entity: Entity,
        env_index: int,
        length: float = 0.15,
    ) -> "Geom":
        from jaxvmas.simulator import rendering

        color = entity.color
        line = rendering.Line(
            (0, 0),
            (length, 0),
            width=2,
        )
        xform = rendering.Transform()
        xform.set_rotation(entity.state.rot[env_index])
        xform.set_translation(*entity.state.pos[env_index])
        line.add_attr(xform)
        line.set_color(*color)
        return line
