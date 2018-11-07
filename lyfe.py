#!/usr/bin/env python3
""" conway's game of life """
import time
import curses
import random
import argparse

def init(pattern):
    """ initialize UNIVERSE """
    iniverse = [[]]*HEIGHT
    for row in range(0, HEIGHT):
        iniverse[row] = [False]*WIDTH
    for coord in pattern:
        iniverse[int(coord[0])][int(coord[1])] = True
    return iniverse

def tick():
    """ advance one generation """
    nextgen = init([])
    for row in range(0, HEIGHT):
        for col in range(0, WIDTH):
            cellstate = UNIVERSE[row][col]
            nbcount = getnbcount([row, col])
            if cellstate:
                if nbcount < 2:
                    nextgen[row][col] = False
                elif nbcount > 3:
                    nextgen[row][col] = False
                else:
                    nextgen[row][col] = True
            else:
                if nbcount == 3:
                    nextgen[row][col] = True
    return nextgen

def simulate(window):
    """ simulate UNIVERSE - wrapped funct for curses"""
    #pylint disable
    global UNIVERSE
    for generation in range(1, GENERATIONS+1):
        window.clear()
        window.addstr('Generation ' + str(generation) + '\n')
        for row in UNIVERSE:
            line = ''
            for col in row:
                if col:
                    line += '*'
                else:
                    line += '.'
            line += '\n'
            window.addstr(line)
        window.refresh()
        time.sleep(TICKTIME)
        UNIVERSE = tick()

def getnbcount(cell):
    """ get count of living neighbors for cell """
    nbcount = 0
    row = cell[0]
    col = cell[1]
    nbcells = [[row-1, col-1], [row-1, col], [row-1, col+1],
               [row, col-1], [row, col+1],
               [row+1, col-1], [row+1, col], [row+1, col+1]]
    for nbcell in nbcells:
        nbrow = nbcell[0]
        nbcol = nbcell[1]
        if nbrow < 0 or nbcol < 0:
            continue
        elif nbrow >= HEIGHT or nbcol >= WIDTH:
            continue
        if UNIVERSE[nbrow][nbcol]:
            nbcount += 1
    return nbcount

def rndpattern():
    """ generate random pattern """
    pattern = []
    for row in range(0, HEIGHT):
        for col in range(0, WIDTH):
            if random.randint(0, 1) % 2 == 0:
                pattern.append([row, col])
    return pattern

def parsepattern(patternfile):
    """ parse initial pattern from file """
    pattern = []
    if patternfile.readline() != '#Life 1.06\n':
        print('unsupported pattern file format - expecting Life 1.06')
        exit(1)
    for line in patternfile:
        # Life 1.06 coordinates have to be reversed (y,x -> x,y) to work here (see TODO.md)
        if line[0] == '#':
            continue
        pattern.append(line.split()[::-1])
    return pattern

# parse arguments
PARSER = argparse.ArgumentParser()
PARSER.add_argument('-H', '--height',
                    type=int, help='universe height (default 10)', default=10)
PARSER.add_argument('-W', '--width',
                    type=int, help='universe width (default 10)', default=10)
PARSER.add_argument('-G', '--generations',
                    type=int, help='generation count (default 10)', default=10)
PARSER.add_argument('-P', '--patternfile',
                    type=argparse.FileType('r'), help='patternfile (default random)')
PARSER.add_argument('-T', '--ticktime',
                    type=float, help='time between ticks (default 1.0)', default=1.0)
ARGS = PARSER.parse_args()

# assign global values
HEIGHT = ARGS.height
WIDTH = ARGS.width
GENERATIONS = ARGS.generations
TICKTIME = ARGS.ticktime

if ARGS.patternfile:
    PATTERN = parsepattern(ARGS.patternfile)
else:
    PATTERN = rndpattern()

UNIVERSE = init(PATTERN)

# main
curses.wrapper(simulate)
