
"""
showcases, chooses, writes:
ssss
c
c
ssss
c
c
c
w
w
w
ssss
c
c
c
w
w
w
ta skupina se po prvnim opakuje dokud to dava smysl, dokud nemaj vsechny write na 0
"""


def get_uceni_data(index):
    if index == 0:
        print("show")
    elif index in [1, 2]:
        print("choose")
    else:
        rem = (index-3) % 7
        if rem == 0:
            print("show")
        elif rem in [1, 2, 3]:
            print("choose")
        else:
            print("write")
