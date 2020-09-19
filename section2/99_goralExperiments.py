# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 10:52:55 2020

@author: tgoral
"""


numbers = [1,3,5]
doubled = [num*2 for num in numbers]
print (numbers)
print(doubled)



friends =['Rolf','Sam','Sally']
starts_s=[friend for friend in friends if friend.startswith("S")]
print(friends)
print(starts_s)


test ={'a': 1, 'b':2}
for k, v in test.items():
    print(k,v)

print ('a' in test)

mytuple = 1,3,4,5

print(mytuple)


# destructuring

x,y = 5, 11
t = 1,3
a,b = t

print(a,b)


people = [('Bob',42, 'Mechanic'),('James',24,'Artist'),('Harry',32,'Lecturer')]

for name, age, profession in people:
    print(name, age, profession)



head, *tail = [1,2,3,4,5]
print(head)
print(tail)

*head, tail = [1,2,3,4,5]
print(head)
print(tail)


# DICTIONARY COMPREHENSIONS

print('\nDICTIONARY COMPREHENSIONS: \n')


users = [
    (0,'Bob','password'),
    (1,'Rolf','xyz'),
    (2, 'Jose','abc'),
    (3, 'username'), '1234']

print('USER LIST:')
print(users)

username_mapping = {user[1]: user for user in users}

print('\nMAPPING DICTIONARY:')
print(username_mapping)



student = {'name':'Jose',
    'school': 'Computing',
    'grades': (66, 77,88)}


for k,v in student.items():
    print(k,v)
    
    
print( student['grades'])



# UNPACKING ARGUMENTS

print('\nUNPACKING ARGUMENTS: \n')


def printer(*args):
    print(args)
printer(1,3,5)


def multiply(*args):
    total = 1
    for arg in args:
        total = total * arg
        
    return total


print(multiply(1,3,5))


def add(x,y):
    return x + y

nums = [3,5]

print (add(*nums))


nums_dict={'x':15,'y':25}
print(add(**nums_dict))




def apply(*args, operator):
    if operator =="*":
        return multiply(*args)
    elif operator == "+":
        return sum(args)
    else:
        return 'No valid operator'
    
    
print ('\nUNPACKER')   
print (apply(1,3,6,7, operator="*"))



# UNPACKING KEYWORD ARGUMENTS

print('\nUNPACKING KEYWORD ARGUMENTS')
def named(**kwargs):
    print (kwargs)


named(name='bob',age=25)

details = {'name':'Bob', 'age': 25}
named(**details)



def print_nicely(**kwargs):
    named(**kwargs)
    for arg, value in kwargs.items():
        print(f'{arg}: {value}')
        

print_nicely(name='Bob', age=25)



def both(*args, **kwargs):
    print(args)
    print(kwargs)
    
    
both (1,3,5,name='Bob',age=25)