#!/usr/bin/python3

# File name:      visualizer.py
# Author:         Ian Howell
# Date Created:   09-05-2017
# Python Version: 3.4

import argparse
import numpy as np
import matplotlib.pyplot as plt
import sys


def main(args):
    width, shapes = get_shapes(args['shapefile'], args['placementfile'])
    length = args['length']

    arr = np.array([0] * length * width).reshape((width, length))

    curr_shape = 1
    for shape in shapes:
        arr = cut_shape(arr, shape, curr_shape)
        curr_shape += 1

    fig, axes = plt.subplots()
    axes.imshow(arr)
    axes.invert_yaxis()

    if args['grid']:
        axes.grid(which='major', linewidth=1, alpha=0.5)
        axes.grid(which='minor', linewidth=1, alpha=0.25)

    y_ticks = [y for y in range(0, width, 5)]
    x_ticks = [x for x in range(0, length, 5)]
    plt.yticks(y_ticks)
    plt.xticks(x_ticks)
    plt.minorticks_on()

    plt.show()


def get_shapes(shapefilename, placementfilename):
    shapes = []
    with open(shapefilename) as sf, open(placementfilename) as pf:
        width, _ = (int(x) for x in sf.readline().strip().split(' '))
        for cut, place_rot in zip(sf, pf):
            shape = {}
            shape['cut'] = tuple(cut.strip().split(','))
            intermediate = [int(x) for x in place_rot.strip().split(',')]
            shape['loc'] = tuple(intermediate[:2])
            shape['rot'] = intermediate[2]
            shapes.append(shape)
    return width, shapes


def cut_shape(arr, shape, shape_id):
    dir_map = {'U': 0, 'R': 1, 'D': 2, 'L': 3}
    directions = [
            (-1, 0),  # Up
            (0, +1),  # Right
            (+1, 0),  # Down
            (0, -1)   # Left
            ]
    col, row = shape['loc']
    rot = shape['rot']
    arr[row][col] = shape_id
    for instruction in shape['cut']:
        direction, count = instruction[0], int(instruction[1])
        tru_dir = directions[(dir_map[direction] + rot) % 4]
        for i in range(count):
            row -= tru_dir[0]
            col += tru_dir[1]
            if (row >= 0) and (col >= 0):
                arr[row][col] = shape_id

    return arr


if __name__ == "__main__":
    # Get arguments
    parser = argparse.ArgumentParser(prog=sys.argv[0])
    parser.add_argument('-g', '--grid', action='store_true',
                        help='Turn on gridlines')
    parser.add_argument('-s', '--shapefile', action='store', required=True,
                        help='File containing the list of shapes')
    parser.add_argument('-p', '--placementfile', action='store', required=True,
                        help='File containing the placement of shapes')
    parser.add_argument('-l', '--length', action='store',
                        type=int, required=True,
                        help='Maximum required length for solution')
    args = parser.parse_args()

    main(vars(args))
