class GameTreeNode(object):
    __slots__ = 'parent', 'children', 'value','y_coordinate','x_coordinate','board'

    def __init__(self,board,y_coordinate=None,x_coordinate=None,value=None):
        self.parent = None
        self.board=board
        self.children = []
        self.y_coordinate=y_coordinate
        self.x_coordinate = x_coordinate
        self.value = value

    def add_child(self, node):
        node.parent = self
        self.children.append(node)

    def __str__(self):
        return str(self.board)

class GameTree(object):

    def __init__(self,root):
        self.root=root

    def is_empty(self):

        return self.root is None

