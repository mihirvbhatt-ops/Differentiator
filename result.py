import simplification as rs
import differentiator as diff
function=input("enter a function")
node=diff.nodemaker(function)
derivative=(diff.differentiate(node))
ans=rs.prune(derivative)
def simplify(ans):
    #converts the simplified tree into a string which the derivative of the function
    #param-simplified ast
    #output-string
    opsD = {
    '+': [1, 'L'],
    '*': [2, 'L'],
    '/': [2, 'L'],
    '^': [3, 'R'],
    'sin': [4, 'R'],
    'cos': [4, 'R'],
    'tan': [4, 'R'],
    'sec': [4, 'R'],
    'csc': [4, 'R'],
    'cot': [4, 'R'],
    'ln':  [4, 'R'],
    'log': [4, 'R'],
     '-': [4, 'R'] 


    }

    if not isinstance(ans, dict):
        return str(ans), 99, None

    op = list(ans.keys())[0]
    prec, asc = opsD[op]
    val=ans[op]
    if op in ('+'):
        parts = [simplify(c)[0] for c in val]
        for c in parts:
            return ' + '.join(parts), prec, asc
    if op in ('*'):
        parts = [simplify(c)[0] for c in val]
        for i in range(len(parts)):
             return ' * '.join(parts), prec, asc

    elif isinstance(val, list) and len(val) == 2:
        left, right = val
        ltext, lprec, _ = simplify(left)
        rtext, rprec, _ = simplify(right)
    elif isinstance(val, list) and len(val) == 1:
    
        left = val[0]
        ltext, lprec, _ = simplify(left)
        rtext, rprec = "", 99  
    else:
    
        left = val
        ltext, lprec, _ = simplify(left)
        rtext, rprec = "", 99

    

    lstr = f"({ltext})" if prec > lprec else ltext
    rstr = f"({rtext})" if prec > rprec else rtext

    if prec == lprec and (asc == "R" or op in ("-", "/")):
        lstr = f"({ltext})"

    if prec == rprec and (asc == "R" or op in ("-", "/")):
        rstr = f"({rtext})"

    if rstr == "":
        return f"{op}({lstr})", prec, asc
    
    else:
        
        return f"{lstr} {op} {rstr}", prec, asc
    

def tokenizer(function): #tokenizer to convert function into list which can be converted int rpn
    tokens=[]
    ntokens=[]
    token=""
    def flushtoken(token,tokens):
        if len(token)>0:
                    tokens.append(token)
                   
                    


        return ""
    for i in range(len(function)):
            
            if role(function[i])=="space": #flush at whitespace characters and ignore them
                   token=flushtoken(token,tokens)
                   continue
                
            token=token + function[i]
            
            if i==len(function)-1: #flush at end of function
                token=flushtoken(token,tokens)
                    
            elif role(function[i]) in ["operator","lparen","rparen"]:
                token=flushtoken(token,tokens)
                    
            elif role(function[i]) != role(function[i+1]): #flush when token type changes (var to num, function to num etc)
                token=flushtoken(token,tokens)
            
    if len(token)>0:
            tokens.append(token)
            
            
    
    return tokens

    
def role(c): #decides token type
    if c.isdigit():
        return "num"
    elif c.isalpha():
        if c in ["sin","cos","tan","csc","sec","cot","log","ln"]:
            return "function"
        else:
            return "var"
    elif c in "(":
        return "lparen"
    elif c in ")":
        return "rparen"
    elif c in ["+","*","/","^","-"]:
        return "operator"
    
    else:
        return "space"

from collections import defaultdict


def simplify_tokens(tokens):
    """
    Algebraic simplifier over a token list.
    - Evaluates numeric-only * and / chains
    - Combines like symbolic terms
    - Handles + and -
    - Outputs clean strings like 7x instead of 7*x
    """

    # -----------------------------------------
    # 1. Collapse numeric-only expressions
    # -----------------------------------------
    def collapse_numeric(tokens):
        out = []
        i = 0
        while i < len(tokens):
            if (
                i + 2 < len(tokens)
                and tokens[i].isdigit()
                and tokens[i+1] in ('*','/')
                and tokens[i+2].isdigit()
            ):
                a = int(tokens[i])
                b = int(tokens[i+2])
                if tokens[i+1] == '*':
                    out.append(str(a * b))
                else:
                    # integer division is safe here because
                    # symbolic division will be handled later
                    out.append(str(a // b))
                i += 3
            else:
                out.append(tokens[i])
                i += 1
        return out

    # Keep collapsing until nothing changes
    prev = None
    while prev != tokens:
        prev = tokens
        tokens = collapse_numeric(tokens)

    if '/' in tokens:
        return ''.join(tokens)

    # -----------------------------------------
    # 2. Collect like terms
    # -----------------------------------------
    terms = {}   # key -> coefficient
    i = 0
    sign = 1

    while i < len(tokens):
        t = tokens[i]

        if t == '+':
            sign = 1
            i += 1
            continue

        if t == '-':
            sign = -1
            i += 1
            continue

        # number * symbolic
        if (
            i + 2 < len(tokens)
            and tokens[i].isdigit()
            and tokens[i+1] == '*'
        ):
            coef = sign * int(tokens[i])
            sym = []
            j = i + 2
            while j < len(tokens) and tokens[j] not in ('+','-'):
                sym.append(tokens[j])
                j += 1
            key = ''.join(sym)
            terms[key] = terms.get(key, 0) + coef
            i = j
            sign = 1
            continue

        # symbolic alone
        if t.isalpha() or t in ('sin','cos','tan','ln','log'):
            sym = []
            j = i
            while j < len(tokens) and tokens[j] not in ('+','-'):
                sym.append(tokens[j])
                j += 1
            key = ''.join(sym)
            terms[key] = terms.get(key, 0) + sign
            i = j
            sign = 1
            continue

        # numeric constant
        if t.isdigit():
            terms[''] = terms.get('', 0) + sign * int(t)
            i += 1
            sign = 1
            continue

        i += 1

    # -----------------------------------------
    # 3. Rebuild final string
    # -----------------------------------------
    parts = []

    for sym, coef in terms.items():
        if coef == 0:
            continue

        if sym == '':
            parts.append(str(coef))
        elif coef == 1:
            parts.append(sym)
        elif coef == -1:
            parts.append(f"-{sym}")
        else:
            parts.append(f"{coef}{sym}")

    result = ""
    for p in parts:
        if p.startswith('-'):
            result += p
        else:
            if result:
                result += "+"
            result += p

    return result

                 
            
print("The derivative of the function is ",simplify_tokens(tokenizer(simplify(ans)[0])))
'''print(derivative)
print(ans)
tests = [
    "-x", "--x", "-(-x)", "-x^2", "(-x)^2",
    "2x", "(x)(x)", "3sin(2x)", "sin(x)cos(x)",
    "sin(sin(x))", "-sin(cos(-x))",
    "-3x^2 + 4x - 7",
    "((x+1)*(x-1))",
]

for t in tests:
    try:
        print(t)
        print(diff.nodemaker(t))
        print(diff.differentiate(diff.nodemaker(t)))
        print(rs.prune((diff.differentiate(diff.nodemaker(t)))))
        print(simplify(rs.prune((diff.differentiate(diff.nodemaker(t)))))[0],"\n")
    except Exception as e:
        print("ERROR:", e)'''

