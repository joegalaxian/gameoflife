#!/usr/bin/env python

import random
import time
import os

DEAD  = '.'
ALIVE = '@'
FPS   = 5 # frames per second

class Game(object):
	def __init__(self, x=10, y=10, percentage=40):
		self.gen = 0
		self.x = x
		self.y = y
		self.population = int(x*y*percentage/100)

		# create board
		self.board = self.empty_board(self.x, self.y)

		# populate board
		for i in range(self.population):
			while True:
				rx = random.randint(0, self.x -1)
				ry = random.randint(0, self.y -1)
				if self.board[ry][rx] == DEAD:
					self.board[ry][rx] = ALIVE
					break

	def empty_board(self, x, y):
		return [ [DEAD for ix in range(x)] for iy in range(y) ]

	def render(self):
		print("Game Of Life - @joegalaxian")
		print("Board size: %dx%d - Generation: %d - Population: %d" % (self.x, self.y, self.gen, self.population))
		result = ''
		for line in self.board:
			for cell in line:
				result += str(cell) + ' '
			result += '\n'
		result = result[:-1]
		print result

	def tick(self):
		"""
		Every cell interacts with its eight neighbours, which are the cells that are horizontally, vertically, or diagonally adjacent.
		At each step in time, the following transitions occur:
		1. Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
		2. Any live cell with two or three live neighbours lives on to the next generation.
		3. Any live cell with more than three live neighbours dies, as if by overpopulation.
		4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
		"""
		new_board = self.empty_board(self.x, self.y)
		for iy in range(self.y):
			for ix in range(self.x):
				cell = self.board[iy][ix]
				neig = self.living_neighbours(ix, iy)
				new_cell = DEAD
				if cell == ALIVE and neig < 2: new_cell = DEAD
				elif cell == ALIVE and neig in(2, 3): new_cell = ALIVE
				elif cell == ALIVE and neig > 3: new_cell = DEAD
				elif cell == DEAD and neig == 3: new_cell = ALIVE
				new_board[iy][ix] = new_cell

		# flip the board
		self.gen += 1
		self.board = new_board[:]

		# recalculate population
		self.population = 0
		for line in self.board:
			self.population += line.count(ALIVE)

	def living_neighbours(self, x, y):
		r = 0

		# previous line
		try:
			if (self.board[y-1][x-1] == ALIVE): r +=1
		except:
			pass

		try:
			if (self.board[y-1][x] == ALIVE): r +=1
		except:
			pass

		try:
			if (self.board[y-1][x+1] == ALIVE): r +=1
		except: pass

		# same line
		try:
			if (self.board[y][x-1] == ALIVE): r +=1
		except: pass
		try:
			if (self.board[y][x+1] == ALIVE): r +=1
		except: pass

		# next line
		try:
			if (self.board[y+1][x-1] == ALIVE): r +=1
		except: pass
		try:
			if (self.board[y+1][x] == ALIVE): r +=1
		except: pass
		try:
			if (self.board[y+1][x+1] == ALIVE): r +=1
		except: pass
		
		#r = random.randint(0,8)
		return r


def main():
	try:
		game = Game(50, 30, 25)
		while game.population:
			os.system('clear')
			game.render()
			game.tick()
			time.sleep(1.0/FPS)
	except KeyboardInterrupt:
		print("Program terminated")

if __name__ == "__main__":
	main()
