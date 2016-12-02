my_dict = {
    'name': 'Jose',
    'location': 'UK'
}

lottery_player = {
    'name': 'Rolf',
    'numbers': (13, 22, 3, 6, 9)
}

dict_in_dict = {
    'universities': [
        {
            'name': 'Oxford',
            'location': 'UK'
        },
        {
            'name': 'Harvard',
            'location': 'US'
        }
    ]
}

##

lottery_player = {
    'name': 'Rolf',
    'numbers': (13, 22, 3, 6, 9)
}

players = [
    {
        'name': 'Rolf',
        'numbers': (13, 22, 3, 6, 9)
    },
    {
        'name': 'John',
        'numbers': (22, 3, 5, 7, 9)
    }
]

# How could we select one of these?

player = players[0]

# How could we add all the numbers of a player?

sum(player['numbers'])

# We have a method that takes in a list—it does not have to be a list of numbers
# of a player. Indeed, we could do something like this:

sum([1, 2, 3, 4, 5])

# Wouldn't it be nice if the player itself (the dictionary) had a method
# that would give us the sum of its numbers? Something like this:

player.total()

# If the player had a method that gives us the sum of its numbers,
# it makes it more difficult to "game" the system—we can no longer pass in
# a different list of numbers.

# In addition, because what we are interested in is the sum of the players' numbers,
# it makes sense for the player itself to tell us that, and not some other method
# that is not a part of the player.
