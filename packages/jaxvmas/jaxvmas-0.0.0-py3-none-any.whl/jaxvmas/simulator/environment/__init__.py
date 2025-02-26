#  Copyright (c) 2022-2024.
#  ProrokLab (https://www.proroklab.org/)
#  All rights reserved.
from enum import Enum
from typing import TYPE_CHECKING

from jaxvmas.simulator.environment.environment import Environment


class Wrapper(Enum):
    GYMNASIUM = 2
    GYMNASIUM_VEC = 3

    def get_env(self, env: Environment, **kwargs):
        if self is self.GYMNASIUM:
            from jaxvmas.simulator.environment.jaxgym.jaxgymnasium import (
                JaxGymnasiumWrapper,
            )

            env = env.replace(terminated_truncated=True)
            return JaxGymnasiumWrapper.create(env, **kwargs)
        elif self is self.GYMNASIUM_VEC:
            from jaxvmas.simulator.environment.jaxgym.jaxgymnasium_vec import (
                JaxGymnasiumVecWrapper,
            )

            return JaxGymnasiumVecWrapper.create(env, **kwargs)
