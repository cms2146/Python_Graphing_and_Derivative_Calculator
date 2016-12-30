import cmath
import numpy.ma
import sys
import matplotlib.pyplot as plt
from objs import *
import math
import copy
"""
This is the utility file for the calculator, nearly all features are kept and maintained here. it includes:
tokenizer(expression)
findNeg(token list)
fixmult(token list)
check(token list)
toReversePolish(token list)
getPrecedence(token data)
calculate(token list, value)
get_function(token)
graph(token_list, xmin,xmax)
isnum(number)
treeify(token list)
infix_traversal(postfix tree)
expression(token list)
collapse(token list)
list_to_string(token list)
derivative(postfix tree)
"""
def tokenizer(expression, lst = [],flag = True):
    """
    Recursive algorithm that takes a input string and converts it into a list of tokens, thus making processing easier.
    :param expression: Input string
    :param lst: keeps track of current list of tokens produced
    :param flag: Solution to scope issues do to default arguments being global, there may be a more elegant solution to
    be found later.
    :return: List of tokens
    """
    if lst !=[] and flag:
        lst = [SOF()]
    elif lst == []:
        lst = [SOF()]
    if expression[:1].isdigit() or expression[:1] == ".":
        i = 0
        while len(expression) !=i and (expression[i].isdigit() or expression[i] == "."):
            i += 1
        if i == 0:
            i = 1
        if len(expression) !=i:
            try:
                tok = num(float(expression[:i]))
            except ValueError:
                print(expression[:1] + " is not a number, quitting now...")
                sys.exit()
        else:
            try:
                tok = num(float(expression))
            except ValueError:
                print(expression + " is not a number, quitting now...")
                sys.exit()
        lst.append(tok)
        return tokenizer(expression[i:],lst,False)

    elif expression[:1] in ["+","-","*","/","^"]:
        tok = oper(expression[0])
        lst.append(tok)
        return tokenizer(expression[1:],lst,False)

    elif expression[:1] == "(":
        lst.append(leftparen())
        return tokenizer(expression[1:],lst,False)

    elif expression[:1] == ")":
        lst.append(rightparen())
        return tokenizer(expression[1:], lst,False)

    elif expression[:1] == 'x':
        lst.append(var())
        return tokenizer(expression[1:],lst,False)

    elif expression[:1].isalpha():
        i = 1
        while expression[i].isalpha():
            i += 1
        tok = expr(expression[:i])
        lst.append(tok)
        return tokenizer(expression[i:],lst,False)
    elif expression[:1] == "":
        lst.append(EOF())
        return lst
def findNeg(toks):
    """
    Due to my processing, a negative symbol looks the same as a minus sign. This converts any oper("-") into
    [leftparen(),num(-l),oper("*"),num(NUMBER TO BE MADE NEGATIVE),rightparen()] so long as another oper preceeds in and
    a number or var follows it.
    :param toks: Token list
    :return: Adjusted token list
    """
    lst = []
    for i in range(len(toks)):

        if type(toks[i]) is oper:
            if toks[i].data == "-" and ((type(toks[i-1]) is SOF or type(toks[i-1]) is oper or type(toks[i-1]) is leftparen) and (type(toks[i+1]) is num or type(toks[i+1]) is var)):
                lst.append(i)
    lst.sort(reverse=True)
    for j in lst:
        toks.insert(j+1,leftparen())
        toks.insert(j+2,num(-1))
        toks.insert(j+3,oper("*"))
        toks.insert(j+5,rightparen())
        toks.pop(j)

    return toks[1:]
def fixmult(toks):
    """
    Adjusts the token list so that all instance of "Nx" where N is a number, is replaced with N*x
    :param toks: token list
    :return: adjusted token list
    """
    lst =[]
    for i in range(len(toks)):
        if type(toks[i]) is num and (type(toks[i+1]) is var or type(toks[i+1]) is expr or type(toks[i+1]) is leftparen):
            lst.append(i)
    lst.sort(reverse=True)
    for i in lst:
        toks.insert(i+1,oper("*"))
    return toks
def check(toks):
    """
    Validates input to make sure it is mathematically valid, will throw an error if the input is invalid
    :param toks: token list
    :return: None
    """
    if not type(toks[-1]) is EOF:
        raise TypeError("EOF not at end.")
    for i in range(len(toks)):
        if type(toks[i]) is num:
            tempbool = type(toks[i+1]) is EOF or type(toks[i+1]) is rightparen or type(toks[i+1]) is oper
            if not tempbool:
                raise NameError("Invalid Syntax, num must be followed by EOF, right parenthesis, or an operation")
            if i!=0:
                tempbool = type(toks[i-1]) is oper or type(toks[i-1]) is leftparen
            if not tempbool:
                raise NameError("Invalid Syntax, num must be preceeded by operation or left parenthesis or Start of File")
        elif type(toks[i]) is oper:

            tempbool = type(toks[i+1]) is num or type(toks[1+i]) or type(toks[i+1]) is leftparen or type(toks[i+1]) is var
            if not tempbool:
                raise NameError("Invalid Syntax, operation must be followed by number, expression, or a variable")
            if i == 0:
                raise NameError("Synatax Error, cannot start expression with operation")
            else:
                tempbool = type(toks[i-1]) is num or type(toks[i-1]) is rightparen or type(toks[i-1]) is var
            if not tempbool:
                raise NameError("Invalid Syntax, operation must be preceeded by number, expression, or variable")
        elif type(toks[i]) is var:
            tempbool = type(toks[i + 1]) is EOF or type(toks[i + 1]) is rightparen or type(toks[i + 1]) is oper
            if not tempbool:
                raise NameError("Invalid Syntax, variable must be followed by EOF, right parenthesis, or an operation")
            if i != 0:
                tempbool = type(toks[i - 1]) is oper or type(toks[i-1]) is leftparen
            if not tempbool:
                raise NameError("Invalid Syntax, variable must be preceeded by operation or left parenthesis Or Start of File")
        elif type(toks[i]) is expr:
            tempbool = type(toks[i + 1]) is leftparen
            if not tempbool:
                raise NameError("Invalid Syntax, expression must be followed by left parenthesis")
            if i!=0:
                tempbool = type(toks[i-1]) is oper or type(toks[i-1]) is leftparen
            if not tempbool:
                raise NameError("Invalid syntax, expression preceeded by operation or left parenthesis or Start of File")
        elif type(toks[i]) is leftparen:
            k = -1
            j = i+1
            while k !=0:
                if type(toks[j]) is EOF:
                    raise RuntimeError("Reached end of expression while parsing")
                if type(toks[j]) is leftparen:
                    k -=1
                if type(toks[j]) is rightparen:
                    k +=1
                j+=1
            tempbool = type(toks[i+1]) is num or type(toks[i+1]) is expr or type(toks[i+1]) is var or type(toks[i+1]) is leftparen
            if not tempbool:
                raise NameError(" Invalid syntax, Left Parenthesis cannot be followed by an operation or End Of File")
            if i !=0:
                tempbool = type(toks[i-1]) is oper or type(toks[i-1]) is expr or type(toks[i-1]) is leftparen
            if not tempbool:
                raise NameError("Invalid syntax, Left Parenthesis can only be preceeded by an operation, expression, or Start of File")
        elif type(toks[i]) is rightparen:
            k = -1
            j = i -1
            while k != 0:
                if j ==len(toks):
                    raise RuntimeError("No left parenthesis to pair")
                if type(toks[j]) is leftparen:
                    k += 1
                if type(toks[j]) is rightparen:
                    k -= 1
                j-=1
            tempbool = type(toks[i + 1]) is EOF or type(toks[i + 1]) is rightparen or type(toks[i + 1]) is oper
            if not tempbool:
                raise NameError("Invalid Syntax, right parenthesis must be followed by EOF, right parenthesis, or an operation")
            if i != 0:
                tempbool = type(toks[i - 1]) is num or type(toks[i-1]) is var or type(toks[i-1]) is rightparen
            if not tempbool:
                raise NameError("Invalid syntax, Right Parenthesis can only be preceeded by an operation, expression, or Start of File")
    return toks
def toReversePolish(toks):
    """
    Uses the Shunting Yard algorithm to covert a infix list of tokens into a postfix string of tokens.
    :param toks: infix token list
    :return: postfix token list
    """
    Queue = queue()
    Stack = stack()
    lst = []
    for tok in toks:
        if type(tok) is num or type(tok) is var:
            Queue.enqueue(tok)
        elif type(tok) is expr:
            Stack.push(tok)
        elif type(tok) is oper:
            if not Stack.top is None:
                while type(Stack.top.data) is oper:
                    if (tok.data in ["-","+","*","/"] and getPrecedence(tok.data) <= getPrecedence(Stack.top.data.data)) or (tok.data == "^" and getPrecedence(tok.data) < getPrecedence(Stack.top.data.data)):
                        Queue.enqueue(Stack.top.data)
                        Stack.pop()
                        if Stack.is_empty():
                            break
                    else:
                        break
            Stack.push(tok)
        elif type(tok) is leftparen:
            Stack.push(tok)
        elif type(tok) is rightparen:
            if not Stack.is_empty():
                while not type(Stack.top.data) is leftparen:
                    Queue.enqueue(Stack.top.data)
                    Stack.pop()
                    if Stack.is_empty():
                        break
            Stack.pop()
            if not Stack.is_empty():
                if type(Stack.top.data) is expr:
                    Queue.enqueue(Stack.top.data)
                    Stack.pop()

        elif type(tok) is EOF:
            if not Stack.top is None:
                while type(Stack.top.data) is oper:
                    Queue.enqueue(Stack.top.data)
                    Stack.pop()
                    if Stack.top is None:
                        break
    while not Queue.is_empty():
        lst.append(Queue.front.data)
        Queue.dequeue()
    return lst
def getPrecedence(operator):
    """
    Returns the precedence for operators for use in toReversePolish(), where high numbers represent greater precedence
    :param operator: operator token data
    :return: number representing the precedence of the given operator
    """
    if operator == "^":
        return 3
    elif operator in ["*","/"]:
        return 2
    elif operator in ["+","-"]:
        return 1
def calculate(toks,val=0):
    """
    Calculates an inputted value of a postfix formatted list of tokens.
    :param toks: Postfix token list
    :param val: Input for token list
    :return: Result
    """
    for tok in toks:
        if type(tok) is var:
            tok.data = val
    my_stack = stack()
    for tok in toks:
        if type(tok) is num or type(tok) is var:
            my_stack.push(tok)
        elif type(tok) is oper:
            if tok.data == '+':
                num1 = my_stack.top.data.data
                my_stack.pop()
                num2 = my_stack.top.data.data
                my_stack.pop()
                my_stack.push(num(num1+num2))
            if tok.data == '-':
                num1 = my_stack.top.data.data
                my_stack.pop()
                num2 = my_stack.top.data.data
                my_stack.pop()
                my_stack.push(num(num2-num1))
            if tok.data == '*':
                num1 = my_stack.top.data.data
                my_stack.pop()
                num2 = my_stack.top.data.data
                my_stack.pop()
                my_stack.push(num(num1*num2))
            if tok.data == '/':
                num1 = my_stack.top.data.data
                my_stack.pop()
                num2 = my_stack.top.data.data
                my_stack.pop()
                try:
                    my_stack.push(num(num2/num1))
                except ZeroDivisionError:
                    return numpy.ma.masked
            if tok.data == '^':
                num1 = my_stack.top.data.data
                my_stack.pop()
                num2 = my_stack.top.data.data
                my_stack.pop()
                my_stack.push(num(num2**num1))
        elif type(tok) is expr:
            num1 = my_stack.top.data.data
            my_stack.pop()
            my_stack.push(num(get_function(tok,num1)))
    return my_stack.top.data.data
def get_function(tok,val):
    """
    Lookup and calculation function for different possible functions.
    :param tok: expr token
    :param val: input value to tok
    :return: result
    """
    if tok.data == "sin":
        if type(val) is float or type(val) is int:
            return round(math.sin(float(val)),4)
        elif type(val) is complex:
            return cmath.sin(val)
    if tok.data == "cos":
        if type(val) is float or type(val) is int:
            return round(math.cos(float(val)),4)
        elif type(val) is complex:
            return cmath.cos(val)
    if tok.data == "tan":
        if type(val) is float or type(val) is int:
            return round(math.tan(float(val)),4)
        elif type(val) is complex:
            return cmath.tan(val)
    if tok.data == "sec":
        if type(val) is float or type(val) is int:
            return round(1/(math.cos(float(val))),4)
        elif type(val) is complex:
            return 1/(cmath.cos(val))
    if tok.data == "csc":
        if type(val) is float or type(val) is int:
            return round(1/(math.sin(float(val))),4)
        elif type(val) is complex:
            return 1/(cmath.sin(val))
    if tok.data == "cot":
        if type(val) is float or type(val) is int:
            return round(1/(math.tan(float(val))),4)
        elif type(val) is complex:
            return 1/(cmath.tan(val))
    if tok.data == "arccos":
        if type(val) is float or type(val) is int:
            return round(math.acos(float(val)),4)
        elif type(val) is complex:
            return cmath.acos(val)
    if tok.data == "arcsin":
        if type(val) is float or type(val) is int:
            return round(math.asin(float(val)),4)
        elif type(val) is complex:
            return cmath.asin(val)
    if tok.data == "arctan":
        if type(val) is float or type(val) is int:
            return round(math.atan(float(val)),4)
        elif type(val) is complex:
            return cmath.atan(val)
    if tok.data == "ln":
        if (type(val) is float or type(val) is int) and val > 0:
            return round(math.log(float(val)),4)
        elif type(val) is complex or val <=0:
            return cmath.log(val)
    if tok.data == "sqrt":
        if (type(val) is float or type(val) is int) and val > 0:
            return round(math.sqrt(float(val)),4)
        elif type(val) is complex or val<=0:
            return cmath.sqrt(val)
    else:
        raise NameError("Function does not exist in lookup table, please add for functionality")

def graph(func,minimum,maximum):
    """
    Graphs a function represented by a postfix list of tokens
    :param func: Function to graph
    :param minimum: x minimum
    :param maximum: y maximum
    :return: None
    """
    count = minimum
    y = []
    while count <= maximum:
        y.append(count)
        count+=.001
    count = minimum
    x = []
    while count <= maximum:
        try:
            x.append(calculate(func,count))
        except ValueError or TypeError:
            x.append(numpy.ma.masked)
        count+=.001
    y = numpy.ma.array(y)
    x = numpy.ma.array(x)
    plt.plot(y,x)
    plt.axhline(0, color='black')
    plt.axvline(0, color='black')
    plt.show()
def isnum(num):
    """
    Returns true if the inputted argument can be converted into a float or int
    :param num:
    :return: Boolean value
    """
    try:
        float(num)
    except ValueError:
        return False
    return True

def treeify(toks,count = 0):
    """
    Turns a postfix list of tokens into a tree, POSTFIX LIST MUST BE REVERSED FOR PROCESSING
    :param toks: Token list to be turned into a tree
    :param count: Keeps track of where to make the next branch of the tree.
    :return: Postfix Tree
    """
    if type(toks[0]) is num or type(toks[0]) is var:
        return tree(toks[0]),count
    if type(toks[0]) is expr:
        temp = expr_tree(toks[0])
        child,count =treeify(toks[1:],count)
        temp.add(child)
        count+=1
        return temp,count
    temp = tree(toks[0])
    right,count = treeify(toks[1+count:])
    left,count = treeify(toks[2+count:])
    count+=2
    temp.add(right)
    temp.add(left)
    return temp,count
def infix_traversal(my_tree):
    """
    Performs an infix traversal of an postfix tree.
    :param my_tree: Postfix tree
    :return: Infix list of tokens
    """
    if type(my_tree) is tree:
        if my_tree.left is None:
            return expression([my_tree.node])
        temp = expression([infix_traversal(my_tree.left),my_tree.node,infix_traversal(my_tree.right)])
        temp1 = []
        for i in temp:
            if type(i) is list:
                temp1 += i
            else:
                temp1 +=[i]
        return temp1
    else:
        if my_tree.child is None:
            return
        temp = expression([my_tree.node,infix_traversal(my_tree.child)])
        return temp
def expression(lst):
    """
    Adds wrapping left and right parenthesis to a token list.
    :param lst: Input list
    :return: Wrapped list
    """
    temp = [leftparen()]
    temp1 = [rightparen()]
    return temp + lst + temp1
def collapse(lst):
    """
    Removes all sublists from a list while keeping their values
    :param lst: List to be collapsed.
    :return: List
    """
    temp = []
    for i in lst:
        if type(i) is list:
            temp +=collapse(i)
        else:
            temp +=[i]
    return temp
def list_to_string(lst):
    """
    Converts an infix token list into an infix string
    :param lst: token list
    :return: Infix string
    """
    temp = ""
    for i in lst:
        if type(i) is var:
            temp += "x"
        elif type(i) is num or type(i) is oper or type(i) is expr:
            temp += str(i.data)
        elif type(i) is leftparen:
            temp += "("
        elif type(i) is rightparen:
            temp += ")"
    return temp
def derivative(my_tree):
    """
    Recursive algorithm to calculate the analytical derivative of a function from a postfix tree. A simplifying algorithm
    still needs to be written to make the output more fit for human use, but is effective for the computational uses
    within this program. This feature is still in development, but it's mostly bug free.
    :param my_tree: Postfix tree
    :return: Infix list of tokens representing the derivative of the function.
    """
    if type(my_tree.node) is num:
        temp = num(0)
        return expression([temp])
    elif type(my_tree.node) is var:
        temp = num(1)
        return expression([temp])
    elif type(my_tree.node) is oper:
        if my_tree.node.data == "+":
            temp = [oper("+")]
            return expression([derivative(my_tree.left)] + temp +[derivative(my_tree.right)])
        elif my_tree.node.data == "-":
            temp = [oper("-")]
            return expression([derivative(my_tree.left)] + temp + [derivative(my_tree.right)])
        elif my_tree.node.data == "*":
            temp = [oper("*")]
            temp1 = [oper("+")]
            return expression(expression(expression([derivative(my_tree.left)]) + temp + expression([infix_traversal(my_tree.right)]))) + temp1 + expression(expression(expression([derivative(my_tree.right)]) + temp + expression([infix_traversal(my_tree.left)])))
        elif my_tree.node.data == "/":
            temp = [oper("*")]
            temp1 = [oper("-")]
            temp2 = [oper("/")]
            temp3 = [oper("^")] + [num(2)]
            return expression(expression(expression(expression([derivative(my_tree.left)]) + temp + expression([infix_traversal(my_tree.right)])) + temp1 + expression(expression([derivative(my_tree.right)]) + temp + expression([infix_traversal(my_tree.left)]))) + temp2 + expression([infix_traversal(my_tree.right)]) + temp3)
        elif my_tree.node.data == "^":
            temp = [oper("*")]
            temp1 = [oper("+")]
            temp2 = [oper("/")]
            return infix_traversal(my_tree) + temp + expression(expression(expression(expression([derivative(my_tree.left)])+ temp2 + expression(infix_traversal(my_tree.left))) + temp + infix_traversal(my_tree.right)) + temp1 + expression([expr("ln")] + infix_traversal(my_tree.left) + temp + [derivative(my_tree.right)]))
    elif type(my_tree.node) is expr:
        if my_tree.node.data == "sin":
            temp = [oper("*")]
            temp1 = [expr("cos")]
            return expression(expression([derivative(my_tree.child)]) + temp + expression(temp1 + expression([infix_traversal(my_tree.child)])) )
    if my_tree.node.data == "cos":
        temp = [oper("*")]
        temp1 = [num(-1),oper("*")]
        temp2 = [expr("sin")]
        return expression(temp1 + [derivative(my_tree.child)]) + temp + temp2 + expression(infix_traversal(my_tree.child))
    if my_tree.node.data == "tan":
        temp = [oper("*")]
        temp1 = [expr("sec")]
        temp2 = [oper("^")] + [num(2)]
        return expression([derivative(my_tree.child)]) + temp + expression(expression([temp1 + expression([infix_traversal(my_tree.child)])])+temp2)
    if my_tree.node.data == "sec":
        temp = [oper("*")]
        temp1 = [expr("sec")]
        temp2 = [expr("tan")]
        return expression([derivative(my_tree.child)]) + temp + expression(expression([temp1 + expression([infix_traversal(my_tree.child)])])+ temp +expression(temp2 + expression([infix_traversal(my_tree.child)])))
    if my_tree.node.data == "csc":
        temp = [oper("*")]
        temp1 = [expr("cot")]
        temp2 = [expr("csc")]
        temp3 = [num(-1),oper("*")]
        return expression([derivative(my_tree.child)]) + temp + expression(temp3 +expression([temp1 + expression([infix_traversal(my_tree.child)])])+ temp +expression(temp2 + expression([infix_traversal(my_tree.child)])))
    if my_tree.node.data == "cot":
        temp = [oper("*")]
        temp1 = [expr("csc")]
        temp2 = [oper("^")] + [num(2)]
        temp3 = [num(-1),oper("*")]
        return expression([derivative(my_tree.child)]) + temp + expression(temp3 +expression(expression([temp1 + expression([infix_traversal(my_tree.child)])])+temp2))
    if my_tree.node.data == "arcsin":
        temp = [oper("/")]
        temp1 = [expr("sqrt")]
        temp2 = [num(1),oper("-")]
        temp3 = [oper("^"),num(2)]
        return [derivative(my_tree.child)] + temp + expression(temp1 + expression(temp2 + expression([infix_traversal(my_tree.child)] + temp3)))
    if my_tree.node.data == "arccos":
        temp = [oper("/")]
        temp1 = [expr("sqrt")]
        temp2 = [num(1),oper("-")]
        temp3 = [oper("^"),num(2)]
        temp4 = [num(-1),oper("*")]
        return temp4 + expression([derivative(my_tree.child)] + temp + expression(temp1 + expression(temp2 + expression([infix_traversal(my_tree.child)] + temp3))))
    if my_tree.node.data == "arctan":
        temp = [oper("/")]
        temp1 = [num(1),oper("+")]
        temp2 = [oper("^"),num(2)]
        return [derivative(my_tree.child)] + temp + expression(temp1 + expression([infix_traversal(my_tree.child)] + temp2))
    if my_tree.node.data == "ln":
        temp = [oper("/")]
        return derivative(my_tree.child) + temp + infix_traversal(my_tree.child)
    if my_tree.node.data == "sqrt":
        temp = [num(.5),oper("*")]
        temp1 = [oper("*")]
        temp2 = [oper("^"),num("-.5")]
        return temp + expression(derivative(my_tree.child)) + temp1 + expression(infix_traversal(my_tree.child)+temp2)
def format_list(toks):
    """
    Coverts a list of tokens from derivative into a useable list for calculations
    :param toks: token list
    :return: Postfix formatted derivative
    """
    toks = collapse(toks)
    toks = list_to_string(toks)
    print(toks)
    toks = findNeg(tokenizer(toks))
    toks = toReversePolish(toks)
    return toks
