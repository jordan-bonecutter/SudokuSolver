#
#
#
#

import numpy as np
import json

class sudoku:
  def __init__(self, board=None):
    # setup board
    self.board = np.zeros((9, 9), dtype=np.uint8)
    if board is not None:
      for y in range(9):
        for x in range(9):
          self.board[y, x] = board[y][x]

    # we will keep track of what numbers are in each column, row and
    # block using lists of booleans. Sure, we could use a set but this
    # will ultimately be faster and take up around the same memory
    self.colused = [[False]*9 for _ in range(9)]
    self.rowused = [[False]*9 for _ in range(9)]
    self.blockused = [[[False]*9 for _ in range(3)] for _ in range(3)]

    for y in range(9):
      for x in range(9):
        val = self.board[y, x]
        if val != 0:
          val -= 1
          self.colused[x][val] = True
          self.rowused[y][val] = True
          self.blockused[y//3][x//3][val] = True


  @classmethod
  def fromFile(cls, fd):
    board = json.load(fd) 
    return cls(board)


  def valid(self, position, val):
    # just check if that value is in the row, column, and block
    y, x = position
    val -= 1
    return (not self.colused[x][val]) and (not self.rowused[y][val]) and (not self.blockused[y//3][x//3][val])


  def place(self, position, val):
    # fill in a spot
    # return True if the move was valid and completed
    # and False otherwise
    y, x = position
    if self.valid(position, val):
      self.board[y, x] = val
      val -= 1
      self.colused[x][val] = True
      self.rowused[y][val] = True
      self.blockused[y//3][x//3][val] = True
      return True
    return False


  def unplace(self, position):
    # undo a move if there is a number there
    y, x = position
    val = self.board[y, x]
    if val != 0:
      self.board[y, x] = 0
      val -= 1
      self.colused[x][val] = False
      self.rowused[y][val] = False
      self.blockused[y//3][x//3][val] = False


  def _solve(self, solns, exhaustive=False):
    # recursively try each possible available move.
    # if you reach a dead end then backtrack
    if not exhaustive and len(solns) > 0:
      return
    for y in range(9):
      for x in range(9):
        if self.board[y, x] == 0:
          for val in range(1, 10):
            if self.place((y, x), val):
              self._solve(solns, exhaustive)
              self.unplace((y, x))
          return solns
    solns.append(sudoku(self.board.copy()))

    
  def solve(self, exhaustive=False):
    return self._solve([], exhaustive)

    
  def __str__(self):
    ret = ''
    for y in range(9):
      for x in range(9):
        ret += str(self.board[y, x])
        if x != 8:
          ret += ' '
        elif y != 8:
          ret += '\n'
    return ret

