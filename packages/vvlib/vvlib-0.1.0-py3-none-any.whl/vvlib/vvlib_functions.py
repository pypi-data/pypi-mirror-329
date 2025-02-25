import random
from random import randint, choice

def goofitize(text: str):
    text = list(text)
    n_text = []
    for i in text:
        goof_coeff = randint(0,1)
        if goof_coeff == 1:
            n_text.append(i.upper())
        else:
            n_text.append(i.lower())
    return "".join(n_text)

def vv_shuffle(ts : str or list):
    was = type(ts)
    ts = list(ts)
    for i in range(random.randint(len(ts), len(ts)+5)):
        fnum = random.randint(0,len(ts)-1)
        snum = random.randint(0, len(ts)-1)

        frng = ts[fnum]
        srng = ts[snum]

        ts[fnum] = srng
        ts[snum] = frng
    if was == list:
        pass
    elif was == str:
        ts = "".join(ts)

    return ts

list_of_goof = [
    "( ͡° ͜ʖ ͡°)",
    "¯\_(ツ)_/¯",
    "ʕ•ᴥ•ʔ",
    "ಠ_ಠ",
    "(͡ ͡° ͜ つ ͡͡°)",
    "(ง'̀-'́)ง",
    "(ಥ﹏ಥ)",
    "(◕‿◕✿)"
]

def vv_append(your_list: list, appendage):
    goof_coeff = random.randint(1,3)
    if goof_coeff == 1:
        your_list.append(random.choice(list_of_goof))
    else:
        your_list.append(appendage)

    return your_list

print(vv_append([1,2], 5))