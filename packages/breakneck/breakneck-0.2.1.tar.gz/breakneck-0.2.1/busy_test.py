#!/usr/bin/env python

import kipy

kicad = kipy.KiCad()
board = kicad.get_board()

print(board.get_selection())
