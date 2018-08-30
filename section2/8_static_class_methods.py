
class Student:
    def __init__(self, name, school):
        self.name = name
        self.school = school
        self.marks = []

    def average(self):
        return sum(self.marks) / len(self.marks)

    def go_to_school(self):
        return "I'm going to {}".format(self.school)

anna = Student("Anna", "Oxford")
rolf = Student("Rolf", "Harvard")

print(anna.go_to_school())
print(rolf.go_to_school())

###

class Student:
    def __init__(self, name, school):
        self.name = name
        self.school = school
        self.marks = []

    def average(self):
        return sum(self.marks) / len(self.marks)

    def go_to_school(self):
        return "I'm going to school"

anna = Student("Anna", "Oxford")
rolf = Student("Rolf", "Harvard")

print(anna.go_to_school())
print(rolf.go_to_school())

###

class Student:
    def __init__(self, name, school):
        self.name = name
        self.school = school
        self.marks = []

    def average(self):
        return sum(self.marks) / len(self.marks)

    @staticmethod
    def go_to_school():
        return "I'm going to school"

anna = Student("Anna", "Oxford")
rolf = Student("Rolf", "Harvard")

print(anna.go_to_school())
print(rolf.go_to_school())

###

class Student:
    def __init__(self, name, school):
        self.name = name
        self.school = school
        self.marks = []

    def average(self):
        return sum(self.marks) / len(self.marks)

    def friend(self, friend_name):
        return Student(friend_name, self.school)

anna = Student("Anna", "Oxford")

friend = anna.friend("Greg")
print(friend.name)
print(friend.school)

