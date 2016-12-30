"""
This file supplies all the custom objects this program uses to function. It includes
node(data,next_node)
stack()
queue()
tree(node,left,right)
expr_tree(node,child)
token(data):
        Subclasses of token:
        num()
        oper()
        expr()
leftparen()
rightparen()
EOF()
SOF()
"""
class node():
    """
    Node object for stacks and queues
    """
    def __init__(self,data,next_node):
        self.data = data
        self.next_node = next_node
class stack():
    """
    Basic stack with pop and push functionality, along with a function to report on the emptyness of the stack.
    """
    top = None
    size = 0
    def push(self,data):
        """
        Puts a value on the top of the stack
        :param data: Data to be added
        :return: None
        """
        if self.size == 0:
            new_node = node(data,None)
            self.top = new_node
            self.size +=1
        else:
            new_node = node(data,self.top)
            self.top = new_node
            self.size +=1
    def pop(self):
        """
        Removes the top of the stack
        :return: None
        """
        if self.is_empty():
            raise IndexError("Tried to remove the top of an empty stack")
        self.top = self.top.next_node
        self.size -=1
    def is_empty(self):
        """
        :return: True if the stack is empty
        """
        return self.size ==0
class queue():
    """
    Basic stack, with functions to add, remove, and report the emptiness of the queue
    """
    front = None
    back = None
    size = 0
    def enqueue(self,data):
        """
        Adds an item to the back of the queue
        :param data: Node to add
        :return: None
        """
        new_node = node(data, None)
        if self.size ==0:
            self.front = new_node
        else:
            self.back.next_node = new_node
        self.back = new_node
        self.size +=1
    def dequeue(self):
        """
        Removes front of queue
        :return: None
        """
        if self.is_empty():
            raise IndexError("Tried to dequeue an empty queue")
        self.front = self.front.next_node
        if self.is_empty():
            self.back = None
        self.size -=1
    def is_empty(self):
        """

        :return: True if the queue is empty
        """
        return self.front ==None
class tree():
    """
    Binary Tree, with functions to add items, remove items, and report the emptyness of the tree
    """
    def __init__(self,node,left = None,right = None):
        self.node =node
        self.left = left
        self.right = right
    def add(self,node):
        """
        Adds items to the tree is right to left order
        :param node: data to be added
        :return: None
        """
        if self.right is None:
            self.right = node
        else:
            self.left = node
    def remove(self,branch):
        """
        Removes the data from a specified brance
        :param branch: Branch to be removed
        :return: None
        """
        branch = None
    def is_empty(self):
        """

        :return: True if both the left and right branceds are None
        """
        return self.left is None and self.right is None
class expr_tree():
    """
    Tree for expr tokens, only has oe child, and has functions for adding, removing.
    """
    def __init__(self,node,child = None):
        self.node = node
        self.child = child
    def add(self,node):
        """
        Sets the vlue of the child node
        :param node: Data to be added
        :return: None
        """
        self.child = node
    def remove(self):
        """
        Sets the child node to None
        :return: None
        """
        self.child = None
class token:
    """
    Superclass for objects below, primarily these related tokens are used to wrap data to assist in processing.
    """
    def __init__(self,data):
        self.data = data
class num(token):
    """
    Tokens to be used for number values
    """
    pass
class expr(token):
    """
    Token to be used for functions like sin, cos, and sqrt
    """
    pass
class leftparen():
    """T
    Token to represent left parenthesis
    """
    pass
class rightparen():
    """
    Token to represent the right parenthesis
    """
    pass
class var:
    """
    Token to wrap vriables, and hold their values.
    """
    def __init__(self,data=None):
        self.data = data
class oper(token):
    """Wrapper tokens for operations"""
    pass
class EOF:
    """Token signifying the end of a file"""
    pass
class SOF:
    """
    Token signifying the start of file
    """
    pass