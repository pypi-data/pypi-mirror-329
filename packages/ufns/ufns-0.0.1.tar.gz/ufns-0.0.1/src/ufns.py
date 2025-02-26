from random import randint

def gen(length, *args): # Generates lists of randomized values
    output = []
    
    if type(args[0]) == type(0):
        for i in range(length):
            output.append(randint(args[0], args[1]))    
    else:
        source = args[0]

        if len(args) == 2:
            dupes = args[1]
        else:
            dupes = False

        for i in range(length):
            index = randint(0, len(source) - 1)
            output.append(source[index])
            if dupes == True:
                source.remove(source[index])

    return output

def linspace(start, end, elements = 0, precision = -1): # returns a list of linearly spaced values
    # Variable Creation
    list = []
    result = []
    n = start

    # Undefined Length Handling
    if elements == 0:
        elements = end - start + 1
        if elements % 1 != 0:
            elements = 100
    
    # Zero Zero Handling
    if elements - 1 != 0:
        increment = (end - start) / (elements - 1)
    else:
        increment = 0
        elements = 100

    # List Population
    while len(list) < elements:
        list.append(n)
        n += increment
    
    # Rounding
    if precision == -1:
        result = list
        result[-1] = end
    else:
        for i in list:
            result.append(round(i, precision))
    
    return result

def lininc(start, end, increment): # Creates a list of numbers between start and end with a difference of increment between each number i.e. when the input is expressed in scientific notation, this function returns the power that 10 is raised to
    li = []
    roundfactor = abs(ordmag(increment))
    print(roundfactor)
    element = start
    while element <= end:
        li.append(element)
        element += increment
        # print(ordmag(element))
        element = round(element, roundfactor)
    return li

def ordmag(number): # Returns the order of magnitude of a number
    n = 0

    if number < 1 and number > -1:
        divisor = 0.1
        sign = -1
    elif number >= 10 or number <= -10:
        divisor = 10
        sign = 1
    else:
        return n
    
    while (number < 1 and number > -1) or number >= 10 or number <= -10:
        n += sign
        number /= divisor
     
    return n