import numpy as np

from functional.common import DimensionKind
from functional.ffront.fbuiltins import Dimension, Field, float64, FieldOffset, neighbor_sum, where
from functional.ffront.decorator import field_operator, program
from functional.iterator.embedded import np_as_located_field, NeighborTableOffsetProvider

CellDim = Dimension("Cell")
KDim = Dimension("K")

num_cells = 5
num_layers = 6
grid_shape = (num_cells, num_layers)

a_value = 0.5
b_value = 2**53
c_value = 2**53
a = np_as_located_field(CellDim, KDim)(np.full(shape=grid_shape, fill_value=a_value, dtype=np.float64))
b = np_as_located_field(CellDim, KDim)(np.full(shape=grid_shape, fill_value=b_value, dtype=np.float64))
c = np_as_located_field(CellDim, KDim)(np.full(shape=grid_shape, fill_value=c_value, dtype=np.float64))

@field_operator
def trip_add(a: Field[[CellDim, KDim], float64],
            b: Field[[CellDim, KDim], float64],
            c: Field[[CellDim, KDim], float64]) -> Field[[CellDim, KDim], float64]:
        return (a + b) - c                                                     # relocate parentheses

result = np_as_located_field(CellDim, KDim)(np.zeros(shape=grid_shape))
trip_add(a, b, c, out=result, offset_provider={})

print("{} + {} + {} = {} +/- {}".format(a_value, b_value, c_value, np.average(np.asarray(result)), np.std(np.asarray(result))))

print(np.asarray(result))


def macheps(x):
    y = x
    while x + y != x:
        y = y / 2

    return y
