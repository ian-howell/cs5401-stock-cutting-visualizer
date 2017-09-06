#!/usr/bin/python3

# File name:      visualizer.py
# Author:         Ian Howell
# Date Created:   09-05-2017
# Python Version: 3.4

import numpy as np
import matplotlib.pyplot as plt
import sys


def main():
    width, length, shapes = get_shapes()

    arr = np.array([0] * length * width).reshape((width, length))

    curr_shape = 1
    for shape in shapes:
        arr = cut_shape(arr, shape, curr_shape)
        curr_shape += 1

    fig, axes = plt.subplots()
    axes.imshow(arr)
    axes.invert_yaxis()
    plt.show()


def get_shapes():
    try:
        shapefilename, placementfilename, length = sys.argv[1:]
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
        return width, int(length), shapes
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        exit(1)
    except:
        usage()
        exit(1)


def cut_shape(arr, shape, shape_id):
    dir_map = {'U': 0, 'R': 1, 'D': 2, 'L': 3}
    directions = [
            (-1, 0),  # Up
            (0, +1),  # Right
            (+1, 0),  # Down
            (0, -1)   # Left
            ]
    height = len(arr)
    col, row = shape['loc']
    rot = shape['rot']
    arr[row][col] = shape_id
    for instruction in shape['cut']:
        direction, count = instruction[0], int(instruction[1])
        tru_dir = directions[(dir_map[direction] + rot) % 4]
        for i in range(count):
            row -= tru_dir[0]
            col += tru_dir[1]
            arr[row][col] = shape_id

    return arr


def usage():
    usage_str = "Usage: python {}"
    usage_str += "<shapefile> <placementfile> <required_length>"
    print(usage_str.format(sys.argv[0]), file=sys.stderr)


if __name__ == "__main__":
    main()
