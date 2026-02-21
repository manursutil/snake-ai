import ctypes
from ctypes import Structure, c_int, POINTER

lib = ctypes.CDLL("build/libsnake.so")

MAX_LENGTH = 500
CELL = 20
WIDTH = 900
HEIGHT = 600


class Vector2i(Structure):
    _fields_ = [("x", c_int), ("y", c_int)]


class SnakeSegment(Structure):
    _fields_ = [("pos", Vector2i)]


class Velocity(Structure):
    _fields_ = [("vx", c_int), ("vy", c_int)]


class Snake(Structure):
    _fields_ = [("body", SnakeSegment * MAX_LENGTH), ("length", c_int), ("v", Velocity)]


class Apple(Structure):
    _fields_ = [("x", c_int), ("y", c_int), ("w", c_int), ("h", c_int)]


class GameState(Structure):
    _fields_ = [
        ("snake", Snake),
        ("apple", Apple),
        ("gameOver", c_int),
        ("score", c_int),
    ]


lib.engine_init.argtypes = [c_int]
lib.engine_reset.argtypes = []
lib.engine_step.argtypes = [c_int]
lib.engine_is_done.restype = c_int
lib.engine_get_score.restype = c_int
lib.engine_get_reward.restype = c_int
lib.engine_get_state.restype = POINTER(GameState)


def state():
    return lib.engine_get_state().contents


def assert_on_grid(x, y):
    assert x % CELL == 0, f"x is off-grid: {x}"
    assert y % CELL == 0, f"y is off-grid: {y}"


def run_checks():
    lib.engine_init(42)

    s0 = state()
    x0 = s0.snake.body[0].pos.x
    y0 = s0.snake.body[0].pos.y
    assert_on_grid(x0, y0)

    # Move right once and verify exactly one-cell movement.
    lib.engine_step(0)
    s1 = state()
    x1 = s1.snake.body[0].pos.x
    y1 = s1.snake.body[0].pos.y
    assert x1 == x0 + CELL, f"expected x={x0 + CELL}, got x={x1}"
    assert y1 == y0, f"expected y={y0}, got y={y1}"
    assert_on_grid(x1, y1)

    # Force an apple directly in front of the head and verify it gets eaten.
    s1.apple.x = x1 + CELL
    s1.apple.y = y1
    score_before = s1.score
    length_before = s1.snake.length

    lib.engine_step(0)
    s2 = state()
    x2 = s2.snake.body[0].pos.x
    y2 = s2.snake.body[0].pos.y

    reward = lib.engine_get_reward()

    assert x2 == x1 + CELL and y2 == y1, "head did not move into apple cell"
    assert s2.score == score_before + 1, (
        f"expected score {score_before + 1}, got {s2.score}"
    )
    assert s2.snake.length == length_before + 1, (
        f"expected length {length_before + 1}, got {s2.snake.length}"
    )
    assert not s2.gameOver, "game should continue after eating apple"
    assert reward == 1, f"expected reward = 1, got reward = {reward}"
    assert_on_grid(x2, y2)

    # Correct Game Over Testing (Out of bounds)
    lib.engine_reset()
    s3 = state()
    s3.snake.body[0].pos.x = WIDTH - CELL
    s3.snake.body[0].pos.y = (HEIGHT // CELL // 2) * CELL
    s3.snake.v.vx = 1
    s3.snake.v.vy = 0

    lib.engine_step(0)
    s4 = state()
    reward_after_game_over = lib.engine_get_reward()

    assert s4.gameOver == 1, "expected game over after moving out of bounds"
    assert lib.engine_is_done() == 1, "engine_is_done() should be 1 after game over"
    assert reward_after_game_over == -1, (
        f"expected reward = -1 on game over, got reward = {reward_after_game_over}"
    )

    print("PASS: engine moves on grid and eats apples correctly.")


if __name__ == "__main__":
    run_checks()
