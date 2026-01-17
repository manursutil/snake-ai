# Snake C

Classic Snake game written in C using the **Raylib** and **Raymath** libraries.

The player controls a snake that grows by eating apples. The game ends when the snake collides with the walls or with its own body.

![snake gif](snake.gif)

## Installation and Usage

1. Install the **Raylib** library by following the official documentation: https://github.com/raysan5/raylib?tab=readme-ov-file#build-and-installation

2. Clone the repository:

```bash
git clone https://github.com/manursutil/snake-c.git
cd snake-raylib
```

3. After installation, you can compile and run the program on macOS using gcc:

```bash
gcc snake.c $(pkg-config --libs --cflags raylib) -o snake && ./snake
```

For other operating systems, please refer to the official Raylib documentation.

4. The Raymath library is also required, but the raymath.h file is already included in this repository.

## Controls

- ⬆️ Up Arrow: move up
- ⬇️ Down Arrow: move down
- ⬅️ Left Arrow: move left
- ➡️ Right Arrow: move right

## Project Structure 

```text
.
├── snake.c        # Main source code
├── raymath.h      # Raylib math library
└── README.md
```