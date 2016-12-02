my_known_people = ["John", "Rolf", "Anne"]
user_name = input("Enter your name: ")
if user_name in my_known_people:
    print("Hello, I know you!")


if user_name in my_known_people:
    print("Hello {}, I know you!".format(user_name))


if user_name in my_known_people:
    print("Hello {name}, I know you!".format(name=user_name))

"Hello {name}, I know you {}!".format("well", name=user_name)
"Hello {}, I know you {}!".format("John", "well")

#### Exercise

def who_do_you_know():
    names = input("Enter the names of people you know, separated by commas: ")
    names_list = names.split(",")
    return names_list

def ask_user():
    # Ask user for their name
    # See if their name is in list of people
    # Print something if it is

    user_name = input("Enter your name: ")
    if user_name in who_do_you_know():
        print("Hello {}, I know you!".format(user_name))
