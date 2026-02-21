import ctypes
from ctypes import Structure, c_float, c_int, POINTER

lib = ctypes.CDLL("build/libsnake.so")

MAX_LENGTH = 500

class Vector2(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float)]

class SnakeSegment(Structure):
    _fields_ = [("pos", Vector2)]

class Velocity(Structure):
    _fields_ = [("vx", c_int),
                ("vy", c_int)]

class Snake(Structure):
    _fields_ = [
        ("body", SnakeSegment * MAX_LENGTH),
        ("length", c_int),
        ("v", Velocity)
    ]

class Apple(Structure):
    _fields_ = [
        ("x", c_int),
        ("y", c_int),
        ("w", c_int),
        ("h", c_int)
    ]

class GameState(Structure):
    _fields_ = [
        ("snake", Snake),
        ("apple", Apple),
        ("gameOver", c_int),
        ("score", c_int)
    ]

lib.engine_init.argtypes = [c_int]
lib.engine_reset.argtypes = []
lib.engine_step.argtypes = [c_int]
lib.engine_is_done.restype = c_int
lib.engine_get_score.restype = c_int
lib.engine_get_state.restype = POINTER(GameState)

lib.engine_init(42)

for _ in range(10):
    lib.engine_step(0)  # move right
    state = lib.engine_get_state().contents
    print("Head:", state.snake.body[0].pos.x,
                  state.snake.body[0].pos.y)