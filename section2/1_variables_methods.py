a = 5
b = 10
my_variable = 56
any_variable_name = 100

string_variable = "hello"
single_quotes = 'strings can have single quotes'

print(string_variable)
print(my_variable)

# print is a method with one parameter—what we want to print

def my_print_method(my_parameter):
    print(my_parameter)

my_print_method(string_variable)

def my_multiplication_method(number_one, number_two):
    return number_one * number_two

result = my_multiplication_method(a, b)
print(result)

print(my_multiplication_method(56, 75))

my_print_method(my_multiplication_method('b', 5))  # What would this do?
