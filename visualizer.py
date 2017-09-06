import sys


def main():
    shapes = get_shapes()
    print(shapes)


def get_shapes():
    try:
        shapefilename, placementfilename = sys.argv[1], sys.argv[2]
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
        return shapes
    except IndexError:
        usage = "Usage: python {} <shapefile> <placementfile>"
        print(usage.format(sys.argv[0]), file=sys.stderr)
        exit(1)
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    main()
