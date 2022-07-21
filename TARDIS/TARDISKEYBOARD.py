from keyboard import *
import time

listKeys = [""]
allowed = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def toString(listInput):
    output=""
    for c in listInput:
        output += c
    return output
def isThere(inputString, inputList):
    for x in inputList:
        if inputString == x:
            return True
    return False

def returnKeypress():
    global listKeys
    global allowed

    proposed = read_key()

    if proposed == "backspace":
        del listKeys[-1]
        return toString(listKeys)
    if proposed == "space":
        listKeys.append(" ")
        return toString(listKeys)

    if isThere(proposed, allowed) == False:
        return toString(listKeys)
    elif isThere(proposed, allowed) == True:
        listKeys.append(proposed)
        return toString(listKeys)
