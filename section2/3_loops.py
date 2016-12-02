my_string = "hello"

for character in my_string:
    print(character)

for asdf in my_string:
    print(asdf)

my_list = [1, 2, 5, 3, 67]

for number in my_list:
    print(number)

for number in my_list:
    print(number ** 2)

should_continue = True
while should_continue:
    print("I'm continuing!")

    user_input = input("Should we continue? (y/n)")
    if user_input == 'n':
        should_continue = False
