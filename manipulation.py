import ast
import numpy as np
import astunparse
import random
import copy


class BinOpFilter(ast.NodeTransformer):
    def visit_BinOp(self, node):
        # Preprocessing: convert all instances of division and subtraction to multiplication and addidtion

        if isinstance(node.op, ast.Sub):  # replace '-_' with '+ (-_)'
            temp = node.right
            node.right = ast.UnaryOp(ast.USub(), temp)
            node.op = ast.Add()

        self.generic_visit(node)  # ensures all child nodes are visited

        # different approach for '/' ... as there will be '/' in the output, generic_visit would never stop
        for tempnode in ast.walk(node):
            if isinstance(node.op, ast.Div):  # replace '/_' with '* (1/_)'
                temp = node.right
                node.right = ast.BinOp(ast.Num(n=1.), ast.Div(), temp)
                node.op = ast.Mult()

        return node


class BinOpPermute(ast.NodeTransformer):
    # visit BinOps and changes order of 'associative' reductions

    # generate list of valid operation types to manipulate
    op1 = '<_ast.Add'
    op2 = '<_ast.Mult'
    op3 = '<_ast.Sub'
    op4 = '<_ast.Div'
    op5 = '<_ast.Pow'

    assosiative_ops = tuple([op1, op2])

    # function to perform a swap with child node to the left
    def left_swap(self, temp_node):
        temp = temp_node.right
        temp_node.right = temp_node.left.right
        temp_node.left.right = temp
        temp_node = temp_node.left
        return temp_node

    def exterior_swap(self, end_node):
        temp_node = end_node
        temp = temp_node.right
        temp_node.right = temp_node.left
        temp_node.left = temp
        return end_node

    def sweep(self, node_list: list, node, direction=1, probability=1):
        # direction=1 => right to left
        # direction=-1 => left to right

        nnodes = len(node_list)
        end_node = node_list[-1]

        if direction == 1:
            for i in np.arange(nnodes - 1):
                temp_node = self.left_swap(node_list[i])
                if random.random() < probability:
                    print(astunparse.unparse(node))

            end_node = self.exterior_swap(end_node)
            if random.random() < probability:
                print(astunparse.unparse(node))

        elif direction == -1:  # right to left
            end_node = self.exterior_swap(end_node)
            if random.random() < probability:
                print(astunparse.unparse(node))

            for i in np.arange(nnodes - 1):
                temp_node = self.left_swap(node_list[nnodes - i - 2])  # check
                if random.random() < probability:
                    print(astunparse.unparse(node))

        return  # node, node_list

    ##-------------------------------------------------------------------------------------------------------

    def generate_permutations(self, node, node_list, probability=1):
        orig_node_dump = ast.dump(copy.copy(node))  # stop generating once this reappears
        temp_node = node

        nnodes = len(node_list)

        end_node = node_list[-1]
        start_node = node_list[0]

        print(astunparse.unparse(node))  # remove this to avoid duplicate
        count = 0
        if nnodes > 1:
            while count == 0 or ast.dump(node) != orig_node_dump:
                self.sweep(node_list, node, 1, probability)  # right to left
                start_node = self.left_swap(start_node)  # rightmost
                if random.random() < probability:
                    print(astunparse.unparse(node))
                self.sweep(node_list, node, -1, probability)  # left to right
                end_node = self.exterior_swap(end_node)  # leftmost
                if random.random() < probability:
                    print(astunparse.unparse(node))
                count += 1

        elif nnodes == 1:  # case where there are only two swappable elements
            print(astunparse.unparse(node))
            node = self.exterior_swap(node)
            print(astunparse.unparse(node))

        return node

    def visit_BinOp(self, node, probability=1):
        op_type = str(node.op)


        # generate list of valid operation types to manipulate
        op1 = '<ast.Add'
        op2 = '<ast.Mult'
        # op3 = '<_ast.Sub'
        # op4 = '<_ast.Div'
        # op5 = '<_ast.Pow'

        print(op_type.startswith(op1))


        assosiative_ops = tuple([op1, op2])

        if op_type.startswith(assosiative_ops):  # proceed if op at node is associative
            temp_node = node
            start_node = node

            node_list = [temp_node]  # initialise with original node

            count = 0

            # specific permutation for demonstration purposes - reverses series of three adds/mults
            while isinstance(temp_node.left, ast.BinOp):
                if type(temp_node.left.op) == type(temp_node.op):  # check if child node is another BinOp of the same type
                    self.left_swap(temp_node)
                    temp_node = temp_node.left
                    self.exterior_swap(temp_node)
                    temp_node = start_node
                    self.left_swap(temp_node)
                    break
                    # node_list.append(temp_node)

                else:
                    break


            # while isinstance(temp_node.left, ast.BinOp):
            #     if type(temp_node.left.op) == type(temp_node.op):  # check if child node is another BinOp of the same type
            #         temp_node = temp_node.left
            #         node_list.append(temp_node)
            #         count += 1
            #     else:
            #         break
            #
            # self.generate_permutations(node, node_list, probability)

        else:
            return node

        return node



source_code = '''
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
'''
source_code_basic = '''
a + b - c
'''
tree = ast.parse(source_code)

vis_filter = BinOpFilter()
vis_filter.visit(tree)
# vis_print = BinOpPrint()
# vis_print.visit(tree)

vis_permute = BinOpPermute()
tree = vis_permute.visit(tree)

print(astunparse.unparse(tree))