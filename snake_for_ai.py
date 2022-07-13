#! /usr/bin/env python3

import pygame
import random
import numpy as np
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
SPEED = 100


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

        self.reset()

    def reset(self):
        self.direction = Direction.RIGHT

        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [
            self.head,
            Point(self.head.x - 1, self.head.y),
            Point(self.head.x - 2, self.head.y),
        ]

        self.score = 0
        self.steps_after_last_food = 0
        self.food = None

        self._place_food()

    def _place_food(self):
        self.food = Point(
            random.randint(0, self.w - 1),
            random.randint(0, self.h - 1),
        )

        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):
        self._move(action)
        self.snake.insert(0, self.head)

        reward = 0
        game_over = False
        if self.is_collision() or self.steps_after_last_food > len(self.snake) * 100:
            game_over = True
            reward -= 10
            return game_over, reward, self.score

        if self.head == self.food:
            self.score += 1
            reward = 10
            self.steps_after_last_food = 0
            self._place_food()
        else:
            self.steps_after_last_food += 1
            self.snake.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, reward, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        if pt.x > self.w - 1 or pt.x < 0 or pt.y > self.h - 1 or pt.y < 0:
            return True

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

    def _move(self, action):
        directions = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = directions.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_direction = directions[idx]
        elif np.array_equal(action, [0, 1, 0]):
            new_direction = directions[(idx + 1) % 4]
        elif np.array_equal(action, [0, 0, 1]):
            new_direction = directions[(idx + 3) % 4]

        self.direction = new_direction

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += 1
        elif self.direction == Direction.LEFT:
            x -= 1
        elif self.direction == Direction.DOWN:
            y += 1
        elif self.direction == Direction.UP:
            y -= 1

        self.head = Point(x, y)


if __name__ == "__main__":
    game = SnakeGame()

    while True:
        game_over, reward, score = game.play_step()

        if game_over == True:
            break

    print("Final Score", score)

    pygame.quit()
