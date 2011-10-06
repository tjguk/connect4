import os, sys
import logging
import unittest

import connect4
#~ connect4.log.setLevel (logging.DEBUG)
connect4.log.addHandler (logging.StreamHandler ())

class TestBoard (unittest.TestCase):

  def setUp (self):
    self.players = connect4.Players ("OX")
    self.board = connect4.Board (self.players)

  def tearDown (self):
    pass

  def test_empty_board (self):
    board = connect4.Board (self.players)
    self.assertFalse (board._board)

  def test_board_rows (self):
    board = connect4.Board (self.players, n_rows=3)
    self.assertEqual (board.rows, [1, 2, 3])

  def test_board_columns (self):
    board = connect4.Board (self.players, n_columns=3)
    self.assertEqual (board.columns, [1, 2, 3])

  def test_board_to_win (self):
    board = connect4.Board (self.players, n_to_win=3)
    self.assertNotEqual (board.win_for ('X', 1), ("win", "X"))
    board.make_move ('X', 1)
    self.assertNotEqual (board.win_for ('X', 1), ("win", "X"))
    board.make_move ('X', 1)
    self.assertNotEqual (board.win_for ('X', 1), ("win", "X"))
    board.make_move ('X', 1)
    self.assertEqual (board.win_for ('X', 1), ("win", "X"))

  def test_valid_columns (self):
    self.assertEqual (list (self.board.valid_columns ()), self.board.columns)
    self.assertListEqual (self.board.valid_columns (), self.board.columns)
    self.board.make_move ('X', 1)
    self.assertEqual (self.board.valid_columns ()[1], 2)
    for i in self.board.rows:
      self.board.make_move ('X', 2)
    self.assertNotIn (2, self.board.valid_columns ())

  def test_column_height (self):
    self.assertEqual (self.board.column_height (1), 0)
    self.board.make_move ('X', 1)
    self.assertEqual (self.board.column_height (1), 1)

  def test_make_move (self):
    self.assertEqual (self.board._board, {})
    self.board.make_move ('X', 1)
    self.assertEqual (self.board._board, {(1, 1) : 'X'})

  def test_intersecting_lines (self):
    board = connect4.Board (self.players, 3, 3)
    self.assertEqual (
      set (tuple (line) for line in board.intersecting_lines (2, 2)),
      set ([
        ((1, 1), (2, 2), (3, 3)),
        ((1, 3), (2, 2), (3, 1)),
        ((1, 2), (2, 2), (3, 2)),
        ((2, 1), (2, 2), (2, 3))
      ])
    )

  def test_project (self):
    board = self.board.project ('X', 1)
    self.assertIsNot (board, self.board)
    self.assertNotEqual (board._board, self.board._board)
    self.assertDictEqual (board._board, {(1, 1) : 'X'})

class TestPlayers (unittest.TestCase):

  def setUp (self):
    self.players = connect4.Players ("ABC")

  def test_next (self):
    self.assertEqual (self.players.next (), "A")

  def test_cycle (self):
    self.assertEqual (self.players.next (), "A")
    self.assertEqual (self.players.next (), "B")
    self.assertEqual (self.players.next (), "C")
    self.assertEqual (self.players.next (), "A")

  def test_peek (self):
    self.players.next ()
    self.assertEqual (self.players.peek (), "B")

  def test_this (self):
    self.assertEqual (self.players.next (), "A")
    self.assertEqual (self.players.this (), "A")
    self.assertEqual (self.players.next (), "B")
    self.assertEqual (self.players.this (), "B")

if __name__ == '__main__':
  unittest.main ()