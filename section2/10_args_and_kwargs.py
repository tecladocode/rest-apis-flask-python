def my_method(arg1, arg2):
    return arg1 + arg2

def my_really_long_addition(arg1, arg2, arg3, arg4, arg5):
    return arg1 + arg2 + arg3 + arg4 + arg5

my_really_long_addition(13, 45, 66, 3, 4)

def adding_simplified(arg_list):
    return sum(arg_list)

adding_simplified([13, 45, 66, 3, 4])

# But you need a list :(

def what_are_args(*args):
    print(args)

what_are_args(12, 35, 64, 'hello')

def adding_more_simplified(*args):
    return sum(args)  # args is a tuple of arguments passed

adding_more_simplified(13, 45, 66, 3, 4)

###

# As well as a tuple of args, we can pass kwargs

def what_are_kwargs(*args, **kwargs):
    print(args)
    print(kwargs)

what_are_kwargs(name='Jose', location='UK')
what_are_kwargs(12, 35, 66, name='Jose', location='UK')

# args are a tuple
# kwargs is a dictionary
# This will come in handy!
