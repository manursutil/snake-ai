# Snake AI (WIP)

Work in progress reinforcement learning project for Snake, built in Python with a C engine backend.

The goal is to train an AI agent to play Snake by interacting with the engine through Python.

![snake gif](snake.gif)

## Status

This project is currently a **work in progress**.

- The C engine exists under `src/c_engine`.
- A Python integration test exists under `src/python_ai/test_env.py`.
- Training pipeline and full RL loop are still under development.

## Installation

1. Clone this repository:

```bash
git clone https://github.com/manursutil/snake-c.git
cd snake-c
```

2. Ensure the build script is executable:

```bash
chmod +x build.sh
```

3. Ensure Python 3 is installed.

Optional (only for playable C game mode):
- Install Raylib with `pkg-config` support:
https://github.com/raysan5/raylib?tab=readme-ov-file#build-and-installation

## Usage

Build the shared engine library for Python:

```bash
./build.sh engine
```

Run the Python engine integration test:

```bash
python3 src/python_ai/test_env.py
```

Optional: build and run the playable C game:

```bash
./build.sh game
./build/snake
```

## Controls

- ⬆️ Up Arrow: move up
- ⬇️ Down Arrow: move down
- ⬅️ Left Arrow: move left
- ➡️ Right Arrow: move right

## Project Structure 

```text
.
├── build.sh                 # Builds game binary or shared engine library
├── build/                   # Build artifacts (snake, libsnake.so)
├── raymath.h                # Math header used by C engine
├── snake.gif                # Demo gif
├── src
│   ├── c_engine
│       ├── main.c           # Rendering loop + input
│       ├── engine.c         # Game logic/state updates
│       ├── engine.h         # Engine API and shared types/constants
│   └── python_ai
│       └── test_env.py      # ctypes-based Python test against C engine
└── README.md
```
