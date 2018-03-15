#!/usr/bin/env python

import random
import time
import os
import sys

DEAD   = '.'
LIVING = '@'

class Game(object):
	def __init__(self, x=30, y=30, population_percentage=30, fps=2):
		self.generation = 0
		self.population = 0
		self.x = x     # board's x axis
		self.y = y     # board's y axis
		self.fps = fps # frames per second
		# create board
		self.board = self.empty_board(self.x, self.y)
		# populate board
		for i in range(int(self.x*self.y*population_percentage/100)):
			while True:
				rx = random.randint(0, self.x -1)
				ry = random.randint(0, self.y -1)
				if self.board[ry][rx] == DEAD:
					self.board[ry][rx] = LIVING
					break
		# refresh population
		self.refresh_population()

	def run(self):
		while self.population:
			self.render()
			self.tick()
			time.sleep(1.0/self.fps)

	def empty_board(self, x, y):
		return [ [DEAD for ix in range(x)] for iy in range(y) ]

	def render(self):
		# Clear screen
		if sys.platform in ('linux2', 'linux', 'unix', 'posix', 'darwin'):
			os.system('clear')
		elif sys.platform in ('win32', 'win64', 'cywin'):
			os.system('cls')
		# Print title and stats
		print("Conway's Game Of Life - @joegalaxian")
		print("Board size: %dx%d - Generation: %d - Population: %d" % (self.x, self.y, self.generation, self.population))
		# Print board
		result = ''
		for line in self.board:
			for cell in line:
				result += str(cell) + ' '
			result += '\n'
		result = result[:-1]
		print(result)
			
	def tick(self):
		"""
		Every cell interacts with its eight neighbours, which are the cells that are horizontally, vertically, or diagonally adjacent.
		At each step in time, the following transitions occur:
		1. Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
		2. Any live cell with two or three live neighbours lives on to the next generation.
		3. Any live cell with more than three live neighbours dies, as if by overpopulation.
		4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
		"""
		# calculate next generation
		next_generation_board = self.empty_board(self.x, self.y)
		for iy in range(self.y):
			for ix in range(self.x):
				cell = self.board[iy][ix]
				neig = self.living_neighbours(ix, iy)
				new_cell = DEAD
				if cell == LIVING and neig < 2: new_cell = DEAD
				elif cell == LIVING and neig in(2, 3): new_cell = LIVING
				elif cell == LIVING and neig > 3: new_cell = DEAD
				elif cell == DEAD and neig == 3: new_cell = LIVING
				next_generation_board[iy][ix] = new_cell
		# transit to next generation
		self.board = next_generation_board[:] # flip board
		self.generation += 1                  # increase generation
		self.refresh_population()             # refresh population
		
	def refresh_population(self):
		self.population = 0
		for line in self.board:
			self.population += line.count(LIVING)

	def living_neighbours(self, x, y):
		r = 0
		# count living neighbours from previous line
		try:
			if (self.board[y-1][x-1] == LIVING): r +=1
		except:
			pass
		try:
			if (self.board[y-1][x] == LIVING): r +=1
		except:
			pass
		try:
			if (self.board[y-1][x+1] == LIVING): r +=1
		except: pass
		# count living neighbours from same line
		try:
			if (self.board[y][x-1] == LIVING): r +=1
		except: pass
		try:
			if (self.board[y][x+1] == LIVING): r +=1
		except: pass
		# count living neighbours from next line
		try:
			if (self.board[y+1][x-1] == LIVING): r +=1
		except: pass
		try:
			if (self.board[y+1][x] == LIVING): r +=1
		except: pass
		try:
			if (self.board[y+1][x+1] == LIVING): r +=1
		except: pass
		return r

if __name__ == "__main__":
	game = Game()
	game.run()