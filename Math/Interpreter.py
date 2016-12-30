from util import *
from objs import *
from tkinter import *
"""
This holds the GUI function, which launches the program, and depends on util.py and objs.py to function
"""
def GUI():
    """
    Main function, can input a mathematical expression, and have a graph made, or individual values calculated
    :return: None
    """
    func = [var()]
    xmin = -10
    xmax = 10
    top = Tk()
    der = BooleanVar()
    result = StringVar()
    l = Label(top,text="Please enter a valid mathematical expression,\nwith x as the independent variable (ex. x^2 + 1):",justify = LEFT).grid(row=0)
    e= Entry(top)
    e.focus_set()
    l2 = Label(top, text="Input Value:", justify=LEFT).grid(row=1)
    e2 = Entry(top)
    def calc():
        """
        Executes upon pressing the calculate button, prints the calculated value of the current function to the screen
        :return:
        """
        nonlocal func
        func = e.get()
        func = func.replace(" ", "")
        func = toReversePolish(check(fixmult(findNeg(tokenizer(func)))))
        result.set(calculate(func, float(e2.get())))
    e.grid(row=0,column=1)
    e2.grid(row=1,column=1)
    b = Button(top, text="Calculate", width=10, command=calc).grid(row=2, column=1)
    l3 = Label(top, text="Result:",font=("Helvetica", 16)).grid(row=3, column=0)
    l4 = Label(top,textvar=result,font=("Helvetica", 16)).grid(row=3,column=1)
    Checkbutton(top, text="Graph Derivative?", variable=der,onvalue=True,offvalue=False).grid(row=2, column = 0)
    def graph_func():
        """
        Graphs the currently inputted function
        :return: None
        """
        nonlocal func
        func = e.get()
        if der.get():
            prime = e.get()
            prime = prime.replace(" ", "")
            prime = toReversePolish(fixmult(findNeg(tokenizer(prime))))
            prime.reverse()
            prime =treeify(prime)[0]
            prime = format_list(derivative(prime))
            graph(prime,xmin,xmax)
        else:
            func = func.replace(" ", "")
            func = toReversePolish(check(fixmult(findNeg(tokenizer(func)))))
            graph(func,xmin,xmax)
    def settings():
        """
        Opens a submenu to set custom xmin and xmax for graph
        :return: None
        """
        nonlocal xmin
        nonlocal xmax
        setting = Tk()
        xmin = Label(setting,text = "xmin (Defaults to -10):").grid(row=1)
        entr = Entry(setting)
        xmax = Label(setting, text="xmax (Defaults to 10):").grid(row=2)
        entr1 = Entry(setting)
        def submission():
            """
            Submits the values inputted in the settings submenu
            :return: None
            """
            nonlocal xmin
            nonlocal xmax
            val = entr.get()
            val2 = entr1.get()
            if val[:1] == "-":
                val = val[1:]
                if isnum(val):
                    xmin = -float(val)
            elif isnum(val):
                xmin = float(val)
            if val2[:1] == "-":
                val2 = val2[1:]
                if isnum(val2):
                    xmax = -float(val2)
            elif isnum(val2):
                xmax = float(val2)
            setting.destroy()
        entr.grid(row=1,column=2)
        entr1.grid(row=2,column=2)
        submit = Button(setting,text = "Submit",width=10,command =submission)
        submit.grid(row=3,column=2)
        setting.mainloop()
    b2 = Button(top,text = "Settings",width=10,command=settings).grid(row=4,column=0)
    b3 = Button(top,text = "Graph",width=10,command=graph_func).grid(row=4,column=1)
    top.mainloop()