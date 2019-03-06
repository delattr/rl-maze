import sys
import random

import pygame
from pygame.locals import *
import matplotlib.pyplot as plt
import numpy as np

from env import Env
from constants import *

# Initialize pygame
maze = Env()
pygame.init()
pygame.font.init()
font = pygame.font.SysFont('arial', 12)
# Window title
pygame.display.set_caption('MacGyver Labyrinthe')
# Window size
window = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))

state, reward, done = maze.reset()
maze.render(window)
pygame.display.flip()

actions = [0,1,2,3]
Q = np.zeros((TILE*TILE,len(actions)))
episodes = 400
gamma = 0.9
lr = .85
rList = []
for i in range(episodes):
    state, reward, done = maze.reset()
    action = None
    rAll = 0
    while not done:
        # elipson-greedy
        e = 1.0 / ((i//100)+1)
        if np.random.rand(1) < e:
            action = random.choice(actions)
        else:
            action = np.argmax(Q[state, :])

        # Greedy
        # action = np.argmax(Q[state, :]+ np.random.randn(1,4) / (i + 1))

        # Render pygame
        # maze.render(window)
        # pygame.display.flip()
        # pygame.time.Clock()

        new_state, reward, done = maze.move(action) # return new_state, reward, done
        # Update Q table
        Q[state, action] = (1-lr)*Q[state,action] + lr*(reward + gamma * np.max(Q[new_state, :]))
        # Upadate state
        state = new_state
        # Accumulate rewards
        rAll += reward

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
    rList.append(rAll)
    print(i+1,'/', episodes, 'Accumulated Reward:', rAll)

print("Final Q-Table Values")
print(Q)
plt.plot(rList)
plt.xlabel("Episodes")
plt.ylabel("Accumulated rewards")
plt.show()

while True:
    state, reward, done = maze.reset()
    while not done:
        action = np.argmax(Q[state, :])
        new_state, reward, done = maze.move(action)
        state = new_state
        maze.render(window)
        # steps = font.render(f"{i}/{episodes}", True, (255, 255, 255))
        # window.blit(steps, (SCREEN_SIZE - SPRITE_SIZE, SCREEN_SIZE - SPRITE_SIZE))
        # Quit pygame
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
        pygame.display.flip()
        pygame.time.Clock().tick(2)