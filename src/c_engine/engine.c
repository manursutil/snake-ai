#include "engine.h"
#include <stdlib.h>
#include <time.h>

static GameState state;
static int last_reward = 0;

static Vector2i getApplePosition(void) {
    int cols = WIDTH / CELL;
    int rows = HEIGHT / CELL;
    int posX = (rand() % cols) * CELL;
    int posY = (rand() % rows) * CELL;
    return (Vector2i){posX, posY};
}

void engine_reset(void) {
    state.snake.length = 1;
    state.snake.body[0].pos = (Vector2i){(WIDTH / CELL / 2) * CELL, (HEIGHT / CELL / 2) * CELL};
    state.snake.v = (Velocity){1, 0};
    Vector2i applePos = getApplePosition();
    state.apple.x = (int)applePos.x;
    state.apple.y = (int)applePos.y;
    state.apple.w = CELL;
    state.apple.h = CELL;
    state.gameOver = 0;
    state.score = 0;
}

void engine_init(int seed) {
    srand(seed);
    engine_reset();
}

void engine_step(int action) {
    if (state.gameOver)
        return;

    switch (action) {
    case 0:
        state.snake.v = (Velocity){1, 0};
        break;
    case 1:
        state.snake.v = (Velocity){-1, 0};
        break;
    case 2:
        state.snake.v = (Velocity){0, -1};
        break;
    case 3:
        state.snake.v = (Velocity){0, 1};
        break;
    default:
        break;
    }

    // Move body
    for (int i = state.snake.length - 1; i > 0; i--) {
        state.snake.body[i].pos = state.snake.body[i - 1].pos;
    }
    state.snake.body[0].pos.x += state.snake.v.vx * CELL;
    state.snake.body[0].pos.y += state.snake.v.vy * CELL;

    Vector2i head = state.snake.body[0].pos;

    // Wall collision
    if (head.x < 0 || head.x >= WIDTH || head.y < 0 || head.y >= HEIGHT) {
        state.gameOver = 1;
        last_reward = -1;
        return;
    }

    // Check collision with itself
    for (int i = 1; i < state.snake.length; i++) {
        if (head.x == state.snake.body[i].pos.x && head.y == state.snake.body[i].pos.y) {
            state.gameOver = 1;
            last_reward = -1;
            return;
        }
    }

    // Eat apple
    if (head.x == state.apple.x && head.y == state.apple.y) {
        if (state.snake.length < MAX_LENGTH) {
            state.snake.body[state.snake.length] = state.snake.body[state.snake.length - 1];
            state.snake.length++;
        }
        Vector2i applePos = getApplePosition();
        state.apple.x = (int)applePos.x;
        state.apple.y = (int)applePos.y;
        state.score++;
        last_reward = 1;
    }
}

int engine_is_done(void) { return state.gameOver; }

int engine_get_score(void) { return state.score; }

int engine_get_reward(void) { return last_reward; }

GameState *engine_get_state(void) { return &state; }
