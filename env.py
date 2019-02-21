import pygame
from constants import *
import random
import numpy as np
import copy

class Env:

    def __init__(self):

        self.structure = []
        self.wall =[]
        self.corridor = []
        self.size = TILE
        self.start = (0, 1)
        self.end = (TILE - 2,TILE - 1)

        self.block = 'x'
        self.cell = 'o'
        self.guard = 'g'
        visited_cells = set()
        unvisited_cells = set()
        stack = []
        # Generate initial cell blocks for auto generation:
        for y in range(0,self.size):          # TILE == maximum number of sprites for y-axis
            line =[]
            for x in range(0,self.size):      # Maxium number of sprites for x-axis
                if not y % 2:            # Block even number lines
                    line.append(self.block)
                elif x % 2:              # creates cell for  odd number
                    line.append(self.cell)
                    unvisited_cells.add((y, x)) # store postion of cell
                else:
                    line.append(self.block)
            self.structure.append(line)

        #create unvisited cells

        # The depth-first search algorithm of maze generation implemented using backtracking:

        # Make the initial cell the current cell and mark it as visited
        current_cell = (1,1)

        # While there are unvisited cells
        while len(unvisited_cells) > 0:
            wall = ()
            # Define current cell's neighbours
            up = (current_cell[0] - 2, current_cell[1])
            down = (current_cell[0] + 2, current_cell[1])
            left = (current_cell[0], current_cell[1] - 2)
            right = (current_cell[0], current_cell[1] + 2)
            neighbours ={'up':up, 'down':down, 'left':left, 'right':right}
            # Find neighbours which have not been visited
            adjacent_cells = dict((k,v) for (k,v) in neighbours.items() if v in unvisited_cells)

            # If the current cell has any unvisited neighbouring cell
            if adjacent_cells:
                # Choose randomly one of the unvisited neighbours
                direction, next_cell = random.choice(list(adjacent_cells.items()))

                # Push the current cell to the stack
                stack.append(current_cell)
                unvisited_cells.remove(next_cell)
                # Remove the wall between the current cell and the chosen cell
                if direction == 'up':
                    wall = (current_cell[0] - 1, current_cell[1])
                elif direction == 'down':
                    wall = (current_cell[0] + 1, current_cell[1])
                elif direction == 'left':
                    wall = (current_cell[0], current_cell[1] - 1)
                elif direction == 'right':
                    wall = (current_cell[0], current_cell[1] + 1)
                self.structure[wall[0]][wall[1]] = self.cell
                # Make the chosen cell the current cell and mark it as visited
                visited_cells.add(current_cell)
                current_cell = next_cell
            # Else if stack is not empty
            elif unvisited_cells and stack:
                # Pop a cell from the stack
                last_cell = stack.pop()
                # Make it the current cell
                current_cell = last_cell
            self.structure[0][1] = 's'
            self.structure[-2][-1] = 'e'
        self.wall = []
        for i in range(self.size):
            for j in range(self.size):
                if self.structure[i][j] == 'x':
                    self.wall.append((i,j))
    def reset(self):

        reward = 0
        done = False

        # Set position of player, exit, and guard, items
        self.player_position = self.start
        state = 1
        # Copy self.item_place to self.items


        return state, reward, done

    def move(self, action):
        self.action = action
        reward = -1
        done = False

        row = self.player_position[0]
        column = self.player_position[1]

        current_position = self.player_position

        if self.action == 0:  # up
            if row > 0:
                row = row - 1

        elif self.action == 1:  # down
            if row < self.size - 1:
                row = row + 1

        elif self.action == 2:  # left
            if column > 0:
                column = column - 1
        elif self.action == 3:  # right
            if column < self.size - 1:
                column = column + 1

        next_position = (row, column)

        # reward for finding an exit
        if next_position == self.end:
            reward = 1
            done = True  # Restart the game

        self.player_position = next_position

        # Negative reward for hitting the wall
        if next_position in self.wall:
            reward = -0.5
            self.player_position = current_position


        # calcute state from current_position (y,x) ex: width x row + column = state
        state = int(self.size * self.player_position[0] + self.player_position[1])

        return state, reward, done

    def render(self, window):

        self.window = window
        # Load images
        fond = pygame.image.load(FOND).convert()
        wall = pygame.image.load(MUR).convert()
        exit_door = pygame.image.load(EXIT).convert()
        start = pygame.image.load(START).convert()
        # Characters
        macgyver = pygame.image.load(MACGYVER).convert_alpha()
        macgyver = pygame.transform.scale(macgyver, (SPRITE_SIZE, SPRITE_SIZE))
        medoc = pygame.image.load(GARDIEN).convert_alpha()
        medoc = pygame.transform.scale(medoc, (SPRITE_SIZE, SPRITE_SIZE))
        #Items
        needle = pygame.image.load(NIDDLE).convert_alpha()
        tube = pygame.image.load(TUBE).convert_alpha()
        ether = pygame.image.load(ETHER).convert_alpha()
        syringe = pygame.image.load(SYRINGE).convert()
        # Initial screen
        win = pygame.image.load(WIN).convert()
        loose = pygame.image.load(LOOSE).convert()
        welcome = pygame.image.load(WELCOME).convert()

        self.window.blit(fond, (0,0))
        self.window.blit(start,(self.start[1]*SPRITE_SIZE,\
                                     self.start[0]*SPRITE_SIZE))
        self.window.blit(exit_door,(self.end[1]*SPRITE_SIZE,\
                                    self.end[0]*SPRITE_SIZE))

        row = 0
        for i in self.structure:
            column = 0
            for j in i:
                x = column * SPRITE_SIZE
                y = row * SPRITE_SIZE
                if j == 'x':
                    self.window.blit(wall, (x,y))
                column += 1
            row += 1

        self.window.blit(macgyver,(self.player_position[1]*SPRITE_SIZE,\
                                   self.player_position[0]*SPRITE_SIZE))


env = Env()