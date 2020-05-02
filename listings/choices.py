

def experience(_limit):
    exp = {}
    for i in range(1,_limit+1):
        exp[i]=i
    return exp


def min_experience():
    return experience(30)


def max_experience():
    return experience(60)

