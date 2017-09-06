# cs5401-stock-cutting-visualizer
A visualizer for the stock cutting problem

## Getting Started
There's a few quick requirements that will need to be filled to use this tool


### Requirements
This visualizer uses Python and one of its popular libraries, matplotlib.
In order for it to function, your machine will need the following:
* \>= Python 3.4
* \>= matplotlib 1.5.3

### How to use it

The EA project requires you to read in from an input file (hereafter referred
to as the shape file) and to generate a solution file (hereafter referred to as
the placement file). Once you have a working EA and have produced some solution
files (and their required amount of material), you may simply run the
visualizer like so:
```bash
python3 visualizer.py shapes.txt placement.txt 10
```
In the above example, `10` is the minimum amount of material required by the
solution.

### Example
Example files and outputs are found in the `examples` directory.  
Given `shapes.txt`:
```
5 2
R1,D1
D1,L4,R1,U3,R3
```
and your solution file `placement.txt`:
```
3,2,1
4,1,0
```
with an optimal solution of `5`, the visualizer will produce this image:
![Visualization of Stock-Cutting Problem](examples/visual.png?raw=true)


## TODO
* Test with more than 2 shapes
* Change colors. They're kinda ugly as is
