#! /usr/bin/env python3

import pygame
import random
from enum import Enum
from collections import namedtuple


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple("Point", ["x", "y"])

WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 10


class SnakeGame:
    def __init__(self, w=32, h=24):
        self.w = w
        self.h = h

        pygame.init()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 25)

        # init display
        self.display = pygame.display.set_mode(
            (self.w * BLOCK_SIZE, self.h * BLOCK_SIZE)
        )
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()

        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [
            self.head,
            Point(self.head.x - 1, self.head.y),
            Point(self.head.x - 2, self.head.y),
        ]

        self.score = 0
        self.food = None

        self._place_food()

    def _place_food(self):
        self.food = Point(
            random.randint(0, self.w - 1),
            random.randint(0, self.h - 1),
        )

        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.direction = Direction.DOWN

        # 2. move
        self._move(self.direction)  # update the head
        self.snake.insert(0, self.head)

        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score

    def _is_collision(self):
        # hits boundary
        if (
            self.head.x > self.w - 1
            or self.head.x < 0
            or self.head.y > self.h - 1
            or self.head.y < 0
        ):
            return True
        # hits itself
        if self.head in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(
                self.display,
                BLUE,
                pygame.Rect(
                    pt.x * BLOCK_SIZE, pt.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE
                ),
            )

        pygame.draw.rect(
            self.display,
            RED,
            pygame.Rect(
                self.food.x * BLOCK_SIZE,
                self.food.y * BLOCK_SIZE,
                BLOCK_SIZE,
                BLOCK_SIZE,
            ),
        )

        text = self.font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += 1
        elif direction == Direction.LEFT:
            x -= 1
        elif direction == Direction.DOWN:
            y += 1
        elif direction == Direction.UP:
            y -= 1

        self.head = Point(x, y)


if __name__ == "__main__":
    game = SnakeGame()

    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break

    print("Final Score", score)

    pygame.quit()
