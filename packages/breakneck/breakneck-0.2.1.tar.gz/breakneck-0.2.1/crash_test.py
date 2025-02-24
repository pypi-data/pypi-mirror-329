#!/usr/bin/env python

import kipy

kicad = kipy.KiCad()
board = kicad.get_board()
footprints = board.get_footprints()
fp = footprints[0]

print(fp)
