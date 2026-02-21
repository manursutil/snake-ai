import numpy as np


class SnakeEnv:
    CELL = 20
    WIDTH = 900
    HEIGHT = 600

    def __init__(self, lib) -> None:
        self.lib = lib
        self.lib.engine_init(42)

    def reset(self) -> np.ndarray:
        self.lib.engine_reset()
        return self._get_obs()

    def step(self, action: int) -> tuple[np.ndarray, float, bool]:
        self.lib.step(action)
        obs = self._get_obs()
        reward = self.lib.engine_get_reward()
        done = self.lib.engine_is_done()

        return obs, reward, done

    def _get_obs(self) -> np.ndarray:
        state = self.lib.engine_get_state().contents

        head_x = int(state.snake.body[0].pos.x) // SnakeEnv.CELL
        head_y = int(state.snake.body[0].pos.y) // SnakeEnv.CELL

        vx = state.snake.v.vx
        vy = state.snake.v.vy

        moving_left = 1 if (vx, vy) == (-1, 0) else 0
        moving_right = 1 if (vx, vy) == (1, 0) else 0
        moving_up = 1 if (vx, vy) == (0, -1) else 0
        moving_down = 1 if (vx, vy) == (0, 1) else 0

        apple_x = state.apple.x // SnakeEnv.CELL
        apple_y = state.apple.y // SnakeEnv.CELL

        food_left = 1 if apple_x < head_x else 0
        food_right = 1 if apple_x > head_x else 0
        food_up = 1 if apple_y < head_y else 0
        food_down = 1 if apple_y > head_x else 0

        forward = (vx, vy)
        left = (-vy, vx)
        right = (vy, -vx)

        danger_straight = (
            1 if self._danger_at(state, head_x + forward[0], head_y + forward[1]) else 0
        )
        danger_left = (
            1 if self._danger_at(state, head_x + left[0], head_y + left[1]) else 0
        )
        danger_right = (
            1 if self._danger_at(state, head_x + right[0], head_y + right[1]) else 0
        )

        obs = np.array(
            [
                moving_left,
                moving_right,
                moving_up,
                moving_down,
                food_left,
                food_right,
                food_up,
                food_down,
                danger_left,
                danger_right,
                danger_straight,
            ],
            dtype=np.float32,
        )

        return obs

    def _danger_at(self, state, x, y):
        if (
            x < 0
            or x >= SnakeEnv.WIDTH // SnakeEnv.CELL
            or y < 0
            or y >= SnakeEnv.HEIGHT // SnakeEnv.CELL
        ):
            return True

        for i in range(1, state.snake.length):
            bx = int(state.snake.body[i].pos.x) // SnakeEnv.CELL
            by = int(state.snake.body[i].pos.y) // SnakeEnv.CELL
            if bx == x and by == y:
                return True

        return False
