def precedent():
    """
    Returns a dictionary defining operator precedence and associativity.

    Format:
        operator : [precedence, associativity]

    Precedence (higher binds tighter):
        +, - : 1
        *, / : 2
        ^    : 3

    Associativity:
        L = left associative
        R = right associative

    Used exclusively by the shunting yard algorithm.
    """s
    opsD = {
        '+': [1, 'L'], #hashmap to store relevant data for operators
        '-': [1, 'L'],
        '*': [2, 'L'], # used for postfix notation (precedence and associativity) and making tree nodes( arity)
        '/': [2, 'L'],
        '^': [3, 'R']
    }
    return opsD
def lexer(function): 
    """
    Converts a mathematical expression string into a list of tokens.

    Responsibilities:
    - Groups multi-character tokens (numbers, variables, functions)
    - Inserts implicit multiplication where required
    - Ignores whitespace

    Example:
        "6x + sin(x)" →
        ['6', '*', 'x', '+', 'sin', '(', 'x', ')']
    """
    tokens=[]
    ntokens=[]
    token=""
    def flushtoken(token,tokens,ntokens):
        """
        Pushes the current token into token lists and
        inserts implicit multiplication when required.

        Implicit multiplication rule:
            num/var/')' followed by num/var/function/'(' → insert '*'
        """
        if len(token)>0:
                    tokens.append(token)
                    ntokens.append(token)
                    if len(tokens)>1:
                        if role(tokens[-2]) in ["num","var","rparen"] and role(tokens[-1]) in ["num","var","function","lparen"]:
                            ntokens.insert(-1,"*")


        return ""
    for i in range(len(function)):
            
            if role(function[i])=="space": #flush at whitespace characters and ignore them
                   token=flushtoken(token,tokens,ntokens)
                   continue
                
            token=token + function[i]
            
            if i==len(function)-1: #flush at end of function
                token=flushtoken(token,tokens,ntokens)
                    
            elif role(function[i]) in ["operator","lparen","rparen"]:
                token=flushtoken(token,tokens,ntokens)
                    
            elif role(function[i]) != role(function[i+1]): #flush when token type changes (var to num, function to num etc)
                token=flushtoken(token,tokens,ntokens)
            
    if len(token)>0:
            tokens.append(token)
            ntokens.append(token)
            
    
    return ntokens
def isnum(function): #helper functions to decide token type
    return function.isnumeric()

def isiden(function):
    return function.isalpha()
def isop(function):
    return function in ["+","-","*","/","^"]

def isfunc(function):
    return function in ["sin", "cos", "tan", "sec", "cot", "csc", "ln", "log"]

def isytspc(function):
    return function.isspace()

def typ(function): #function to decide token type
    if isnum(function):
        return "num"
    elif isiden(function):
        return "var"
    elif isop(function):
        return "op"
    elif isytspc(function):
        return "space"
    
def role(c):
    """
    Classifies a character or token into a semantic role.

    Possible roles:
        num       → digit
        var       → variable name
        function  → sin, cos, ln, etc.
        operator  → + - * / ^
        lparen    → (
        rparen    → )
        space     → whitespace
    """
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

hashm = { #decides arity of the operator (unary or binary) can be removed later
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

def shuntingyard(tokens):
    """
    Converts an infix token list into postfix (RPN) notation.

    Handles:
    - operator precedence
    - associativity
    - functions
    - unary minus using '~'x
    """
    opsD = precedent()
    output = []
    opsQ = []
    prev_role = "start"

    def push_op(op):
        if op[0] == "~":
            op_prec, op_assoc = 4, "R"
        else:
            op_prec, op_assoc = opsD[op]

        while opsQ:
            top = opsQ[-1]
            if top[0] == "~":
                top_prec, top_assoc = 4, "R"
            elif top in opsD:
                top_prec, top_assoc = opsD[top]
            else:
                break

            if (top_prec > op_prec) or (top_prec == op_prec and op_assoc == "L"):
                output.append(opsQ.pop())
            else:
                break
        opsQ.append(op)

    i = 0
    while i < len(tokens):
        c = tokens[i]
        if i > 0:
            prev_role = role(tokens[i-1])

        if isnum(c) or (isiden(c) and not isfunc(c)):
            output.append(c)
            while opsQ and opsQ[-1][0] == "~":
                output.append(opsQ.pop())
            
        elif isfunc(c):
            opsQ.append(c)
                 
        
        elif c == "(":
            opsQ.append(c)

        elif c == ")":
            while opsQ and opsQ[-1] != "(":
                output.append(opsQ.pop())
            opsQ.pop()  # remove "("
            if opsQ and isfunc(opsQ[-1]):
                output.append(opsQ.pop())
            while opsQ and opsQ[-1][0] == "~":
                output.append(opsQ.pop())

        elif c in opsD:
            if c =='-' or prev_role == "function":
                if prev_role in ["start", "operator", "lparen", "function"]:
                    push_op("~"+c)
            
                else:
                   
                    push_op('+')
                    push_op("~"+c)  
            else:
                     
                    push_op(c)

        i += 1
        prev_role = role(c)

    while opsQ:
        output.append(opsQ.pop())

    return output

