my_variable = 'hello'
my_list_variable = ['hello', 'hi', 'nice to meet you']
my_tuple_variable = ('hello', 'hi', 'nice to meet you')
my_set_variable = {'hello', 'hi', 'nice to meet you'}

print(my_list_variable)
print(my_tuple_variable)
print(my_set_variable)

my_short_tuple_variable = ("hello",)
another_short_tuple_variable = "hello",

print(my_list_variable[0])
print(my_tuple_variable[0])
print(my_set_variable[0])  # This won't work, because there is no order. Which one is element 0?

my_list_variable.append('another string')
print(my_list_variable)

my_tuple_variable.append('a string')  # This won't work, because a tuple is not a list.
my_tuple_variable = my_tuple_variable + ("a string",)
print(my_tuple_variable)
my_tuple_variable[0] = 'can I change this?'  # No, you can't

my_set_variable.add('hello')
print(my_set_variable)
my_set_variable.add('hello')
print(my_set_variable)


###### Set Operations

set_one = {1, 2, 3, 4, 5}
set_two = {1, 3, 5, 7, 9, 11}

print(set_one.intersection(set_two))  # {1, 3, 5}

print({1, 2}.union({2, 3}))  # {1, 2, 3}

print({1, 2, 3, 4}.difference({2, 4}))  # {1, 3}
