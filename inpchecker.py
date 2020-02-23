"""
This module was made to process input
"""
def is_int(args, natural=False):
    """
    list(str, str, ...), [bool] -> list or bool
    ---
    Check whether number is an integer or natural on purpose.
    If all the conditions are satisfied, return a list
    Otherwise, return False and print prompts
    ---
    >>> is_int(["1", "0"])
    [1, 0]
    >>> is_int(["1", "01"])
    Integer numbers should not start with ZERO: 01
    False
    >>> is_int(["1", "-11","1","12"], natural = True)
    The integer numbers should be positive: -11
    False
    """
    wrong = []
    is_positive = lambda x: True if int(x) > 0 else (False, wrong.append(x))[0]
    unsigned = lambda x: x.strip("+").strip("-")
    begins_with_zero = lambda x: (True, wrong.append(x))[0]\
                       if len(unsigned(x)) > 1 and unsigned(x)[0] == "0" else False
    not_is_digit = lambda x: False if unsigned(x).isdigit() else (True, wrong.append(x))[0]
    zero = bool(sum(([begins_with_zero(elm) for elm in args])))
    if zero:
        print("Integer numbers should not start with ZERO: " + " ".join(wrong))
        return False
    not_integer = bool(sum([not_is_digit(elm) for elm in args]))
    if not_integer:
        print("Integer numbers should be neither floats nor expressions: " + " ".join(wrong))
        return False
    if natural:
        not_positive = bool(sum([not is_positive(elm) for elm in args]))
        if not_positive:
            print("The integer numbers should be positive: " + " ".join(wrong))
            return False
    return list(map(int, args))

def is_interval(args, natural=True):
    """
    list(str, str), [bool] -> list or bool
    ---
    Check whether interval of integer or natural numbers is correct .
    If all the conditions are satisfied, return a list
    Otherwise, return False and print prompts
    ---
    >>> is_interval(["1", "5"])
    (1, 5)
    >>> is_interval(["1", "-1"], natural=True)
    The integer numbers should be positive: -1
    False
    >>> is_interval(["1", "1"])
    If start is equal to finish, it is not an interval
    False
    """
    start, end = args[0], args[1]
    integers = is_int([start, end], natural)
    if not integers:
        return False
    start, end = is_int([start, end], natural)
    if start > end:
        print("Wrong interval, start should not be bigger than finish")
        return False
    if start == end:
        print("If start is equal to finish, it is not an interval")
        return False
    return int(start), int(end)

def inp_taker(check_funk, nmb_of_arg, natural=False):
    """
    function, int -> processed input
    ---
    Check input and repeat the cycle unless all the conditions are satified.
    Return checked and prosessed by function input.
    """
    good = False
    while not good:
        inp = input(">>> ").split()
        if len(inp) > nmb_of_arg:
            print(f"Too many arguments, should be {nmb_of_arg}")
        elif len(inp) < nmb_of_arg:
            print(f"Not enough arguments, should be {nmb_of_arg}")
        else:
            good = check_funk(inp, natural)
    return good

if __name__ == "__main__":
    from doctest import testmod as test
    test()
