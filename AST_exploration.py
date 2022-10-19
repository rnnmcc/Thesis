import ast
import astunparse
import re
import numpy as np
source_code = "3. + 5. + 6."

source_code_1 = 'x = 73'
source_code_2 = 'x + np.sqrt(3)'

tree_1 = ast.parse(source_code_1)
tree_2 = ast.parse(source_code_2)


# print(astunparse.unparse(tree))
# print(ast.parse(source_code))
# print(tree)

print(ast.dump(tree_1))
print(ast.dump(tree_2))

print(astunparse.unparse(tree_2.body[0].value))
# print((tree_2.body[0].value.op))

# tree_2.body[0].value.op = re.sub('Add','Sub', tree_2.body[0].value.op)

# str1 = 'fre'
# str1 = re.sub('f','d',str1)
# print(str1)

print(astunparse.unparse(tree_2))

str1 = (ast.dump(tree_2))
str2 = re.sub('Add','Sub',str1)
print(str2)
tree_2_new = ast.parse(str2)


# tree.body[0].value = ast.parse('37')
# print(astunparse.unparse(tree))
# print(tree.body[0].targets[0].ctx)

# print(astunparse.unparse(tree.body[0].value.left))
# temp = tree.body[0].value.left.left
# tree.body[0].value.left.left = tree.body[0].value.right
# tree.body[0].value.right = temp

# temp = tree.body[0].value.left.left
# tree.body[0].value.left.left = tree.body[0].value.left.right
# tree.body[0].value.left.right = temp
# print(astunparse.unparse(tree))

# for node in ast.walk(tree):
#     print(node)
#     print(node.__dict__)
    # print("children: " + str([x for x in ast.iter_child_nodes(node)]) + "\n")


class FuncVisitor(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        if len(node.name) == 1:
            print('move on, only one')


# for node in ast.walk(tree):
#     print('\n', node)
#     print(node.__dict__yes)

# print(ast.walk(tree))

class RewriteName(ast.NodeTransformer):
    def visit_Name(self, node):
        return ast.copy_location(ast.Subscript(
            value=ast.Name(id='data', ctx=ast.Load()),
            slice=ast.Index(value=ast.Str(s=node.id)),
            ctx=node.ctx
        ), node)

# newtree = ast.parse(open('dummy.py').read())
# RewriteName().visit(newtree)
# print(astunparse.unparse(newtree))



# hello there