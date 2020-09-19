# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 10:52:55 2020

@author: tgoral
"""
# OBJECT ORIENTED PROGRAM
print("OBJECT ORIENTED PROGRAMMING")

class Student:
    def __init__(self, name, grades):
        self.name = name
        self.grades = grades
    def average_grades (self):
        return sum(self.grades) / len(self.grades)
        
        
        
        
        
        
        
student = Student('Bob',(100,100,93,78,90))
print(student.name)
print(student.grades)
print(student.average_grades())


print()
student2 = Student('Rolf',(100,80,73,88,90))
print(student2.name)
print(student2.grades)
print(student2.average_grades())


# MAGIC METHODS

print("\nMAGIC METHOD")

class Person:
    def __init__(self,name, age):
        self.name = name
        self.age = age
    
    #def __str__(self):
        #return f"{self.name}, {self.age}"
    
    def __repr__(self):
        return f"<{self.name}, {self.age}>"
        
bob = Person('Bob',35)
print(bob)


class Store:
    def __init__(self,name):
        # You'll need 'name' as an argument to this method.
        # Then, initialise 'self.name' to be the argument, and 'self.items' to be an empty list.
        self.name  = name
        self.items = []
    
    def add_item(self, name, price):
        # Create a dictionary with keys name and price, and append that to self.items.
        item = {'name': name, 'price': price}
        self.items.append(item)

    def stock_price(self):
        # Add together all item prices in self.items and return the total.
        total = 0
        for each in self.items:
            total += each['price']
        return total