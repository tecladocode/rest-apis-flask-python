class Student:
    def __init__(self, name, school):
        self.name = name
        self.school = school
        self.marks = []

    def average(self):
        return sum(marks) / len(marks)

    def friend(self, friend_name):
        return Student(friend_name, self.school)

anna = Student("Anna", "Oxford")

friend = anna.friend("Greg")
print(friend.name)
print(friend.school)

###

class WorkingStudent(Student):
    def __init__(self, name, school, salary):
        super().__init__(name, school)
        self.salary = salary

rolf = WorkingStudent("Rolf", "Harvard", 20.00)
sue = rolf.friend("Sue")
print(sue.salary)  # Error!

###

class Student:
    def __init__(self, name, school):
        self.name = name
        self.school = school
        self.marks = []

    def average(self):
        return sum(marks) / len(marks)

    @classmethod
    def friend(cls, origin, friend_name, *args):
        return cls(friend_name, origin.school, *args)

class WorkingStudent(Student):
    def __init__(self, name, school, salary):
        super().__init__(name, school)
        self.salary = salary

rolf = WorkingStudent("Rolf", "Harvard", 20.00)
sue = WorkingStudent.friend(rolf, "Sue", 15.00)
print(sue.salary)  # This works!
