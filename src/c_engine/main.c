#include "engine.h"
#include "raylib.h"
#include <time.h>

int main(void) {
    InitWindow(WIDTH, HEIGHT, "Snake");
    SetTargetFPS(FPS);

    engine_init((int)time(NULL));

    int frameCounter = 0;
    int moveEveryNFrames = FPS / MOVES_PER_SECOND;

    while (!WindowShouldClose()) {
        frameCounter++;

        int action = -1;
        if (IsKeyDown(KEY_RIGHT))
            action = 0;
        if (IsKeyDown(KEY_LEFT))
            action = 1;
        if (IsKeyDown(KEY_UP))
            action = 2;
        if (IsKeyDown(KEY_DOWN))
            action = 3;

        if (frameCounter >= moveEveryNFrames) {
            engine_step(action);
            frameCounter = 0;
        }

        BeginDrawing();
        ClearBackground(RAYWHITE);

        GameState *s = engine_get_state();

        // Draw grid
        for (int x = 0; x <= WIDTH; x += CELL)
            DrawLine(x, 0, x, HEIGHT, LIGHTGRAY);
        for (int y = 0; y <= HEIGHT; y += CELL)
            DrawLine(0, y, WIDTH, y, LIGHTGRAY);

        // Draw snake
        for (int i = 0; i < s->snake.length; i++) {
            DrawRectangle((int)s->snake.body[i].pos.x, (int)s->snake.body[i].pos.y, CELL, CELL,
                          i == 0 ? DARKBLUE : BLUE);
        }

        // Draw apple
        DrawRectangle(s->apple.x, s->apple.y, s->apple.w, s->apple.h, RED);

        DrawText(TextFormat("Score: %d", s->score), 10, 10, 20, BLACK);

        if (s->gameOver)
            DrawText("Game Over", WIDTH / 2 - 80, HEIGHT / 2 - 20, 40, RED);

        EndDrawing();
    }

    CloseWindow();
    return 0;
}
