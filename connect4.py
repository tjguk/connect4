import os, sys
import itertools

class Board (object):

  def __init__ (self, n_columns=7, n_rows=6, board=None):
    self.columns = range (1, n_columns+1)
    self.rows = range (1, n_rows+1)
    if board:
      self._board = dict (board)
    else:
      self._board = {}

  def __repr__ (self):
    return "<%s: %s>" % (self.__class__.__name__, repr (self._board))

  def __str__ (self):
    return self.as_string ()

  def as_string (self):
    return "\n".join ("|".join (self._board.get ((column, row), ".") for column in self.columns) for row in self.rows[::-1])

  def intersecting_lines (self, column, row):
    yield [(c, r) for c in self.columns for r in self.rows if c == column]
    yield [(c, r) for c in self.columns for r in self.rows if r == row]
    yield [(c, r) for c in self.columns for r in self.rows if c + r == column + row]
    yield [(c, r) for c in self.columns for r in self.rows if c - r == column - row]

  def column_height (self, column):
    return max ([r for c, r in self._board.keys () if c == column] or [0])

  def possible_moves (self):
    for column in self.columns:
      row = 1 + self.column_height (column)
      if row <= max (self.rows):
        yield column, row

  def make_move (self, player, column):
    self._board[column, 1 + self.column_height (column)] = player

  def win_for (self, n_to_win=4):
    for player in set (self._board.values ()):
      winning_run = player * n_to_win

      for row in self.rows:
        if winning_run in "".join (self._board.get ((column, row), ".") for column in self.columns):
          return player

      for column in self.columns:
        if winning_run in "".join (self._board.get ((column, row), ".") for row in self.rows):
          return player

      offsets = range (min (len (self.rows), len (self.columns)))
      for offset in offsets:
        if winning_run in "".join (self._board.get ((column, row), ".") for column in self.columns for row in self.rows if row + column == offset):
          return player
        if winning_run in "".join (self._board.get ((column, row), ".") for column in self.columns for row in self.rows if row - column == offset):
          return player

    return None

  def project (self, player, counter):
    board = self.__class__ (
      n_columns=len (self.columns),
      n_rows=len(self.rows),
      board=self._board
    )
    board.make_move (player, counter)
    return board

class Game (object):

  n_to_win = 4
  players = itertools.cycle (['X', 'O'])

  def __init__ (self):
    self.board = Board ()

  def turn (self, player, column):
    print "Turn for player %r - %r" % (player, column)
    if column not in (c for c, r in self.board.possible_moves ()):
      raise ValueError, "Invalid move"
    self.board.make_move (column, player)

  def play (self):
    print self.board.as_string ()

    while True:
      player = self.players.next ()
      column = int (raw_input ("Player %s: " % player))
      self.turn (player, column)
      print self.board.as_string ()

      winner = self.board.win_for ()
      if winner:
        print "%s wins!" % player
        break

def main ():
  Game ().play ()

if __name__ == '__main__':
  main (*sys.argv[1:])
