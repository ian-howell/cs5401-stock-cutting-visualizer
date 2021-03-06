#!/usr/bin/python3

# File name:      visualizer.py
# Author:         Ian Howell
# Date Created:   09-05-2017
# Python Version: 3.4

import argparse
import numpy as np
import matplotlib.pyplot as plt
import sys


def main():
    fig = plt.figure()
    axes = fig.add_subplot(111)

    width, shapes = get_shapes(args['shapefile'], args['placementfile'])
    if args['length']:
        length = args['length'] + 1  # Pad with one space because of 0-indexing
    else:
        length = 5

    arr = np.zeros(length * width).reshape((width, length))

    curr_shape = 1
    for shape in shapes:
        arr = cut_shape(axes, arr, shape, curr_shape)
        curr_shape += 1

    # If there are no shapes on the sheet, stop
    if (np.count_nonzero(arr) == 0):
        print("There are no shapes on the sheet")
        exit(0)

    arr = np.ma.masked_where(arr == 0, arr)
    axes.imshow(arr, cmap='rainbow')
    axes.invert_yaxis()

    if args['grid']:
        axes.grid(which='major', linewidth=1, alpha=0.5)
        axes.grid(which='minor', linewidth=1, alpha=0.25)

    width = arr.shape[0]
    length = arr.shape[1]

    tick_width = width - (width % 5) + 1
    tick_length = length - (length % 5) + 1
    y_ticks = [y for y in range(0, tick_width, 5)]
    x_ticks = [x for x in range(0, tick_length, 5)]
    plt.yticks(y_ticks)
    plt.xticks(x_ticks)
    plt.minorticks_on()

    plt.show()
    plt.close()


def get_shapes(shapefilename, placementfilename):
    shapes = []
    with open(shapefilename) as sf, open(placementfilename) as pf:
        width, _ = (int(x) for x in sf.readline().strip().split(' '))
        for cut, place_rot in zip(sf, pf):
            shape = {}
            shape['cut'] = tuple(cut.strip().split(' '))
            intermediate = [int(x) for x in place_rot.strip().split(',')]
            shape['loc'] = tuple(intermediate[:2])
            shape['rot'] = intermediate[2]
            shapes.append(shape)
    return width, shapes


def cut_shape(ax, arr, shape, shape_id):
    dir_map = {'U': 0, 'R': 1, 'D': 2, 'L': 3}
    directions = [
            (+1, 0),  # Up
            (0, +1),  # Right
            (-1, 0),  # Down
            (0, -1),  # Left
            ]
    col, row = shape['loc']
    rot = shape['rot']

    # Resize the sheet if needed
    while (col >= arr.shape[1]):
        arr = grow(arr)

    # Add the start square
    add_square(ax, arr, row, col, shape_id)

    # Get the new row and col
    for instruction in shape['cut']:
        direction, count = instruction[0], int(instruction[1])
        tru_dir = directions[(dir_map[direction] + rot) % 4]
        for i in range(count):
            row += tru_dir[0]
            col += tru_dir[1]

            # Resize the sheet if needed
            while (col >= arr.shape[1]):
                arr = grow(arr)

            # Add the current square
            add_square(ax, arr, row, col, shape_id)

    return arr


def grow(arr):
    # new_arr = np.hstack((arr, np.zeros((arr.shape[0], 5))))
    new_arr = np.append(arr, np.zeros((arr.shape[0], 5)), axis=1)
    return new_arr


def add_square(ax, arr, row, col, shape_id):
    if out_of_bounds(row, col, arr.shape[0]):
        # Shape is out of bounds
        fmt = "Shape {} is out of bounds at row {}, col {}"
        print(fmt.format(shape_id, row, col))
    elif (arr[row][col] != 0) and (arr[row][col] != shape_id):
        # Shape is overlapping another shape (not itself)
        fmt = "Shape {} is overlapping shape {} at row {}, col {}"
        print(fmt.format(shape_id, int(arr[row][col]), row, col))
    else:
        arr[row][col] = shape_id
        if args['number']:
            ax.text(col, row, str(shape_id - 1), ha='center', va='center')


def out_of_bounds(r, c, max_r):
    return (r < 0) or (r >= max_r) or (c < 0)


if __name__ == "__main__":
    # Get arguments
    parser = argparse.ArgumentParser(prog=sys.argv[0])
    parser.add_argument('-g', '--grid', action='store_true',
                        help='Turn on gridlines')
    parser.add_argument('-n', '--number', action='store_true',
                        help='Turn on shape_ids')
    parser.add_argument('-s', '--shapefile', action='store', required=True,
                        help='File containing the list of shapes')
    parser.add_argument('-p', '--placementfile', action='store', required=True,
                        help='File containing the placement of shapes')
    parser.add_argument('-l', '--length', action='store', type=int,
                        help='Maximum required length for solution')

    global args
    args = vars(parser.parse_args())

    main()
