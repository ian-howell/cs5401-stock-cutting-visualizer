import sys


def main():
    shapes = get_shapes()
    print(shapes)


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


def usage():
    usage_str = "Usage: python {}"
    usage_str += "<shapefile> <placementfile> <required_length>"
    print(usage_str.format(sys.argv[0]), file=sys.stderr)


if __name__ == "__main__":
    main()
