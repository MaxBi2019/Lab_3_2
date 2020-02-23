"""
Module for work with JSON from https://api.twitter.com/1.1/friends/list.json
"""
import json
import inpchecker
from chatbot import to_end


def as_user(dct):
    """

    :param dct: dict()


    :return: dict()
    Shape JSON in an appropriate way
    --------------------------------
    >>> as_user({"users": [{"name": "Kate", "age": 3}, {"name": "Joe", "age": 5}]})
    {'users': {'Kate': {'age': 3}, 'Joe': {'age': 5}}}
    >>> as_user({"users": [{"name": "Kate", "age": 3}]})
    {'users': {'Kate': {'age': 3}}}
    >>> as_user({"users": [{"name": "Kate"}]})
    {'users': {'Kate': {}}}
    """
    if "users" in dct:
        length = len(dct["users"])
        dct["users"] = {dct["users"][elm].pop("name"): dct["users"][elm] for elm in range(length)}
    return dct


def js_reader(fl_name, func):
    """

    :param fl_name: str()
    :param func: function()


    :return: dict()
    ---------------
    Read JSON file
    """
    with open(fl_name, mode="r", encoding="utf-8") as file:
        loaded = json.load(file, object_hook=func)
    return loaded


LEAVES = {}     # Set where all information is stored
MAX = 5         # Supremum of columns number


def tb_maker(data, num, sep=3):
    """

    :param data: iterable
    :param num: int() # Number of columns
    :param sep: int() # Margins among columns


    :return: list
    Output a table and return sorted list
    --------------
    >>> tb_maker(["2", "11", "8"], 3)
    1) 2   2) 8   3) 11
    ['2', '8', '11']
    >>> tb_maker(["2", "11", "8"], 3, sep=2)
    1) 2  2) 8  3) 11
    ['2', '8', '11']
    >>> tb_maker(["2", "11", "8", "9"], 2, sep=2)
    1) 2  3) 9
    2) 8  4) 11
    ['2', '8', '9', '11']
    """
    catalogue = sorted(list(data), key=lambda arg: len(arg))
    lngth = len(catalogue)
    text = [str(indx + 1) + ") " + elm for indx, elm in enumerate(catalogue)]
    small = len(text) // num + 1 * bool(len(text) % num)
    form = [small * indx - 1 if num != indx else lngth - 1 for indx in range(1, num + 1)]
    lnght_lst = [len(text[elm]) + sep for elm in form[:-1]] + [0]
    text = [elm + " " * (lnght_lst[indx // small] - len(elm))
            for indx, elm in enumerate(text)]
    for elm_x in range(small):
        for elm_y in range(num):
            current = elm_y * small + elm_x
            if current <= lngth - 1:
                print(text[current], end="")
        print("")
    return catalogue


def userchoice(rng, msg="|||"):
    """

    :param rng: list() or int()
    :param msg: str()


    :return: False or int()
    -----------------------
    If rng is '0' or ['0'], return False
    If rng is not '0' or ['0'], return int
    """
    rng = len(rng) if isinstance(rng, list) else rng
    if not rng:
        print("Found NOTHING\n")
        return None
    while True:
        inp = input(f"\nPlease choose the number of {msg} you want to get information about\n" + \
                    f"You have to choose type an integer from 1 to {rng}\n>>> ").strip().split(" ")
        if len(inp) == 1:
            if inpchecker.is_int(inp, natural=True):
                inp = inp[0]
                if int(inp) <= rng:
                    print()
                    return int(inp) - 1
                print("Too, big a number")
        else:
            print("Too many arguments")
    return False


def column_num(lst, maxi=5):
    """

    :param lst: list()
    :param maxi: int() # Max number of columns


    :return: int()
    --------------
    Find the most appropriate column number
    >>> column_num([1, 2, 3, 4, 5], 2)
    1
    >>> column_num([1, 2, 3, 3, 3, 3, 3,3 ,3, 3, 3, 3, 4], 2)
    2
    >>> column_num([1, 2, 3, 4, 5], 3)
    1
    """
    num, raw = len(lst) // 10, len(lst)
    num = num + bool(raw % 10) or 1 if num < maxi else maxi
    return num


def output(pth, j_s):
    """

    :param pth: str()
    :param j_s: dict()


    :return: False or dict
    ----------------------
    If we got to the not nested key of dict, return False
    If the argument for key is iterable, return it
    """
    last = True
    pth = pth.split("|")
    if pth[-1].isdigit():
        if pth[-1] != "0":
            pth[-1] = userchoice(int(pth[-1]), msg=pth[-2])
            last = False
        else:
            print(f"There is no \"{pth[-2]}\"")
            pth[-1] = None
    if None in pth:
        return False
    dct = "j_s" + "".join([f"[pth[{indx}]]" for indx in range(len(pth))])
    result = eval(dct)
    if isinstance(result, (list, dict)) and result:
        return result
    result = None if result in [tuple(), dict(), set(), list(), ""] else result
    show = f"{pth[-1 * last or -2]}: {result}"
    print(show)
    print("-" * len(show))
    return False


def main(file_name, border=MAX):
    """

    :param border:


    :return: None
    -------------
    Main body
    """
    ahead = True
    while ahead:
        j_s, key = js_reader(file_name, as_user), None
        while j_s:
            data = {elm: elm for elm in j_s}
            choice = tb_maker(data.keys(), column_num(data, border))
            key = choice[userchoice(choice, msg="cell")]
            pth = data[key]
            j_s = output(pth, j_s)
            data.clear()
        ahead = not to_end()


if __name__ == "__main__":
    from doctest import testmod as test
    test()
    main("UCU_University.json")
