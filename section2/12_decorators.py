# A decorator is just a function that gets called before another function

import functools  # function tools

def my_decorator(f):
    @functools.wraps(f)
    def function_that_runs_f():
        print("Hello!")
        f()
        print("After!")
    return function_that_runs_f

@my_decorator
def my_function():
    print("I'm in the function.")

my_function()


###

def my_decorator(f):
    @functools.wraps(f)
    def function_that_runs_f(*args, **kwargs):
        print("Hello!")
        f(*args, **kwargs)
        print("After!")
    return function_that_runs_f

@my_decorator
def my_function(arg1, arg2):
    print(arg1 + arg2)

my_function(56, 89)

###

def decorator_arguments(number):
    def my_decorator(f):
        @functools.wraps(f)
        def function_that_runs_f(*args, **kwargs):
            print("Hello!")
            if number == 56:
                print("Not running!")
            else:
                f(*args, **kwargs)
            print("After")
        return function_that_runs_f
    return my_decorator

@decorator_arguments(56)
def my_function():
    print("Hello!")

my_function()
