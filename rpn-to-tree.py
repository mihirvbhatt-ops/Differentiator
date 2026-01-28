import lexer+shuntingyard as stp

hashm = {
    '+': 2,
    '*': 2,
    '/': 2,
    '^': 2,
    '-': 1,
    'sin': 1,
    'cos': 1,
    'tan': 1,
    'sec': 1,
    'cot': 1,
    'csc': 1,
    'log': 1,
    'ln': 1
}



def treemaker(function):
    postfix = stp.shuntingyard(stp.lexer(function))
    stk = []

    for ch in postfix:
        if ch in hashm or ch[0] == "~":
            if ch[0] == "~":
                op = ch[1:]
                if len(stk)>0:
                    a = stk.pop()
                else:
                    pass
                stk.append({op: a})
            elif hashm[ch] == 1:
                a = stk.pop()
                stk.append({ch: a})
            else:
                b = stk.pop()
                a = stk.pop()
                stk.append({ch: [a, b]})
        else:
            if stp.isnum(ch):
                stk.append(int(ch))
            else:
                stk.append(ch)

    return stk[0]

'''function=input("enter")
print(stp.lexer(function))
print(stp.shuntingyard(stp.lexer(function)))
print(treemaker(function))'''


