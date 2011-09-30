import os, sys
import itertools
import logging

log = logging.getLogger ("connect4")

class Board (object):

  def __init__ (self, n_columns=7, n_rows=6, n_to_win=4, board=None):
    self.columns = range (1, n_columns+1)
    self.rows = range (1, n_rows+1)
    self.n_to_win = n_to_win
    if board:
      self._board = dict (board)
    else:
      self._board = {}

  def __repr__ (self):
    return "<%s: %s>" % (self.__class__.__name__, repr (self._board))

  def __str__ (self):
    return self.as_string ()

  def __getitem__ (self, item):
    return self._board[item]

  def as_string (self):
    return "\n".join ("|".join (self._board.get ((column, row), ".") for column in self.columns) for row in self.rows[::-1])

  def counters (self):
    return dict (self._board)

  def column_height (self, column):
    return max ([r for c, r in self._board.keys () if c == column] or [0])

  def valid_columns (self):
    """Determine all valid columns from the board's current position. This can
    be used both to validate an entered move and to look ahead
    """
    for column in self.columns:
      row = 1 + self.column_height (column)
      if row <= max (self.rows):
        yield column

  def make_move (self, player, column):
    """Make a player's move by "dropping" his counter onto the highest available
    position in a column.
    """
    self._board[column, 1 + self.column_height (column)] = player

  def intersecting_lines (self, column, row):
    """Determine which lines (horizontal, vertical or diagonal) intersect
    a position on the board -- typically one which has just been played.
    """
    yield [(c, r) for c in self.columns for r in self.rows if c == column]
    yield [(c, r) for c in self.columns for r in self.rows if r == row]
    yield [(c, r) for c in self.columns for r in self.rows if c + r == column + row]
    yield [(c, r) for c in self.columns for r in self.rows if c - r == column - row]

  def win_for (self, player, column, row=None):
    """Determine whether a specific player has won. Given the nature of the game,
    only the player who has just moved can possibly have won, and only by completing
    a line which contains his latest position.
    """
    winning_run = player * self.n_to_win
    log.debug ("winning_run = %s", winning_run)
    if row is None:
      row = max (r for c, r in self._board if c == column)
    for line in self.intersecting_lines (column, row):
      log.debug ("line: %s", "".join (self._board.get ((c, r), ".") for (c, r) in line))
      if winning_run in "".join (self._board.get ((c, r), ".") for (c, r) in line):
        return True
    else:
      return False

  def project (self, player, column):
    """Return the state of the board after a player has dropped their counter
    in a particular column. This would usually be used to look ahead.
    """
    board = self.__class__ (
      n_columns=len (self.columns),
      n_rows=len(self.rows),
      board=self._board
    )
    board.make_move (player, column)
    return board

class Game (object):

  n_to_win = 4
  players = itertools.cycle (['X', 'O'])

  def __init__ (self):
    self.board = Board ()

  def turn (self, player, column):
    print "Turn for player %r - %r" % (player, column)
    valid_columns = list (self.board.valid_columns ())
    if column not in valid_columns:
      raise ValueError, "Invalid move"
    self.board.make_move (player, column)

  def play (self):
    print self.board.as_string ()

    while True:
      player = self.players.next ()
      column = int (raw_input ("Player %s: " % player))
      self.turn (player, column)
      print self.board.as_string ()

      if self.board.win_for (player, column):
        print "%s wins!" % player
        break

def main ():
  Game ().play ()

if __name__ == '__main__':
  main (*sys.argv[1:])
