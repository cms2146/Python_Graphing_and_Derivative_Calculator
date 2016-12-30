import pip
try:
    from Interpreter import *
except ImportError:
    print(
        "Hello! In order to function, this program needs to ensure two external modules are installed, numpy and matplotlib")
    print("As such, if they are not installed, this program will install them")
    ans = input("If you are ok with this, enter 'y':")
    if ans == 'y':
        pip.main(["install", "ez_setup"])
        pip.main(["install", "setuptools"])
        pip.main(["install", "numpy"])
from Interpreter import *
GUI()