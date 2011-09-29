import os, sys
import itertools

class Game (object):

  columns = range (1, 8)
  rows = range (1, 7)
  n_to_win = 4
  players = itertools.cycle (['X', 'O'])

  def __init__ (self):
    self.board = {}

  def __str__ (self):
    return self.board_as_string ()

  def board_as_string (self):
    return "\n".join ("|".join (self.board.get ((column, row), ".") for column in self.columns) for row in self.rows[::-1])

  def turn (self, player, column):
    print "Turn for player %r - %r" % (player, column)
    row = 1 + max ([r for c, r in self.board.keys () if c == column] or [0])

    if column not in self.columns:
      print "Column must be between %d and %d" % (min (self.columns), max (self.columns))
    elif row not in self.rows:
      print "Column %d is already full" % column
    else:
      print "Intersecting:"
      for line in self.intersecting_lines (column, row):
        print line
      self.board[column, row] = player

  def intersecting_lines (self, column, row):
    yield [(c, r) for c in self.columns for r in self.rows if c == column]
    yield [(c, r) for c in self.columns for r in self.rows if r == row]
    yield [(c, r) for c in self.columns for r in self.rows if c + r == column + row]
    yield [(c, r) for c in self.columns for r in self.rows if c - r == column - row]

  def check_for_win (self, player):
    winning_run = player * self.n_to_win

    for row in self.rows:
      if winning_run in "".join (self.board.get ((column, row), ".") for column in self.columns):
        return True

    for column in self.columns:
      if winning_run in "".join (self.board.get ((column, row), ".") for row in self.rows):
        return True

    offsets = range (min (len (self.rows), len (self.columns)))
    for offset in offsets:
      if winning_run in "".join (self.board.get ((column, row), ".") for column in self.columns for row in self.rows if row + column == offset):
        return True
      if winning_run in "".join (self.board.get ((column, row), ".") for column in self.columns for row in self.rows if row - column == offset):
        return True

    return False

  def possible_moves (self):
    return [column for column in self.columns if max ([r for c, r in self.board.keys () if c == column] or [0]) < len (self.rows)]

  def play (self):
    print self.board_as_string ()

    while True:
      player = self.players.next ()
      column = int (raw_input ("Player %s: " % player))
      self.turn (player, column)
      print self.board_as_string ()

      if self.check_for_win (player):
        print "%s wins!" % player
        break

def main ():
  Game ().play ()

if __name__ == '__main__':
  main (*sys.argv[1:])
