#ifndef ENGINE_H
#define ENGINE_H

#define WIDTH 900
#define HEIGHT 600
#define FPS 60
#define MOVES_PER_SECOND 10
#define CELL 20
#define MAX_LENGTH 500

typedef struct {
    int vx, vy;
} Velocity;

typedef struct {
    int x;
    int y;
} Vector2i;

typedef struct {
    Vector2i pos;
} SnakeSegment;

typedef struct {
    SnakeSegment body[MAX_LENGTH];
    int length;
    Velocity v;
} Snake;

typedef struct {
    int x, y, w, h;
} Apple;

typedef struct {
    Snake snake;
    Apple apple;
    int gameOver;
    int score;
} GameState;

void engine_init(int seed);
void engine_reset(void);
void engine_step(int action);

int engine_is_done(void);
int engine_get_score(void);
int engine_get_reward(void);

GameState *engine_get_state(void);

#endif
